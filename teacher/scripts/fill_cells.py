#!/usr/bin/env python3
"""HWPX 표 셀 채우기 도구.

기존 HWPX 양식의 표 셀을 셀 주소(table, col, row) 기준으로 채운다.
빈 셀(<hp:run .../>)과 이미 텍스트가 있는 셀(치환) 모두 처리하며,
원본의 셀 크기·병합·테두리·문단/run 속성을 그대로 보존한다.
mimetype은 ZIP_STORED, ZIP 엔트리 순서는 원본 그대로 유지한다.

사용법:
  셀 목록:  python fill_cells.py "양식.hwpx" --list
  채우기:   python fill_cells.py "양식.hwpx" "결과.hwpx" --map "cells.json"
  재검증:   python fill_cells.py "결과.hwpx" --verify "cells.json"

cells.json 형식:
  {
    "table": 1,                                        // 선택: 기본 표 인덱스(문서 등장 순, 0부터)
    "cells": [
      {"col": 0, "row": 2, "text": "5"},
      {"col": 3, "row": 2, "text": "첫 줄\n둘째 줄"},   // \n = 문단 분리
      {"table": 0, "col": 0, "row": 0, "text": "제목"}  // 셀별 table 지정이 기본값보다 우선
    ]
  }
  최상위가 바로 배열이어도 된다. "text": "" 는 셀 내용 비우기.

동작 규칙:
  - 같은 (col,row)가 여러 표에 있는데 table 지정이 없으면 쓰지 않고 오류로 알린다.
  - 대상 셀 안에 중첩 표가 있으면 채우지 않는다(내부 표 셀을 --list로 확인해 지정).
  - 여러 줄 텍스트는 셀의 마지막 문단을 복제해 문단 수를 맞춘다.
  - --map은 저장 직후 구조 비교(표/셀 개수, cellAddr/cellSpan/cellSz 동일 여부)와
    대상 셀 값 PASS/FAIL 리포트를 자동 출력한다. 별도 검증 명령이 필요 없다.
"""

import argparse
import json
import os
import re
import sys
import zipfile

TOKEN_RE = re.compile(r"<hp:tbl\b|</hp:tbl>|<hp:tc\b|</hp:tc>")
TBL_TAG_RE = re.compile(r"<hp:tbl\b[^>]*>")
P_RE = re.compile(r"<hp:p\b.*?</hp:p>", re.S)
RUN_RE = re.compile(r"<hp:run\b[^>]*?(?:/>|>.*?</hp:run>)", re.S)
T_RE = re.compile(r"<hp:t\b[^>]*/>|<hp:t\b[^>]*(?<!/)>.*?</hp:t>", re.S)


def _utf8_console():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def unesc(text):
    return text.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&amp;", "&")


def t_inner(t_block):
    """<hp:t ...>내용</hp:t> 에서 내용을 꺼낸다. 자기닫힘이면 빈 문자열."""
    if t_block.endswith("/>"):
        return ""
    i = t_block.find(">")
    j = t_block.rfind("<")
    return t_block[i + 1 : j]


def scan_cells(xml):
    """모든 <hp:tc>를 스캔해 셀 레코드 목록을 만든다.

    Returns:
        list[dict]: {start, end, table, col, row, nested} (start 오름차순)
        table은 해당 셀을 직접 감싸는 <hp:tbl>의 문서 등장 순 인덱스(0부터).
        nested는 셀 내부에 중첩 표가 있는지 여부.
    """
    table_stack, tc_stack, cells = [], [], []
    next_table = 0
    for m in TOKEN_RE.finditer(xml):
        tok = m.group(0)
        if tok == "<hp:tbl":
            table_stack.append(next_table)
            next_table += 1
        elif tok == "</hp:tbl>":
            if table_stack:
                table_stack.pop()
        elif tok == "<hp:tc":
            tc_stack.append((m.start(), table_stack[-1] if table_stack else -1))
        else:  # </hp:tc>
            if not tc_stack:
                continue
            start, tbl = tc_stack.pop()
            end = m.end()
            block = xml[start:end]
            # 셀 자신의 cellAddr는 subList(중첩 내용 포함) 뒤에 오므로 마지막 일치를 쓴다
            cols = re.findall(r'colAddr="(\d+)"', block)
            rows = re.findall(r'rowAddr="(\d+)"', block)
            if not cols or not rows:
                continue
            cells.append({
                "start": start,
                "end": end,
                "table": tbl,
                "col": int(cols[-1]),
                "row": int(rows[-1]),
                "nested": "<hp:tbl" in block,
            })
    cells.sort(key=lambda c: c["start"])
    return cells


def cell_text(xml, cell):
    """셀의 문단별 텍스트를 \n으로 이어 돌려준다(끝쪽 빈 문단 제거)."""
    block = xml[cell["start"]:cell["end"]]
    lines = []
    for p in P_RE.findall(block):
        lines.append(unesc("".join(t_inner(t.group(0)) for t in T_RE.finditer(p))))
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def _fill_run(run, text_escaped):
    """run 하나에 텍스트를 넣는다. 기존 <hp:t>가 여러 개면 첫 개만 남기고 비운다."""
    if run.endswith("/>"):
        return run[:-2] + "><hp:t>" + text_escaped + "</hp:t></hp:run>"
    ts = list(T_RE.finditer(run))
    if not ts:
        return run[: -len("</hp:run>")] + "<hp:t>" + text_escaped + "</hp:t></hp:run>"
    parts, last, first = [], 0, True
    for t in ts:
        parts.append(run[last:t.start()])
        parts.append("<hp:t>" + text_escaped + "</hp:t>" if first else "<hp:t/>")
        first = False
        last = t.end()
    parts.append(run[last:])
    return "".join(parts)


def _clear_run(run):
    if run.endswith("/>"):
        return run
    return T_RE.sub("<hp:t/>", run)


def set_para_text(p_block, line):
    """문단의 첫 유효 run에 line을 넣고 나머지 run의 텍스트를 비운다.

    line이 빈 문자열이면 모든 run의 텍스트를 비운다.
    run 개수와 속성(charPrIDRef 등)은 유지한다.
    """
    runs = list(RUN_RE.finditer(p_block))
    target = None
    if line != "":
        for idx, r in enumerate(runs):
            rb = r.group(0)
            if "<hp:pic" in rb or "<hp:tbl" in rb:
                continue
            target = idx
            break
    parts, last = [], 0
    for idx, r in enumerate(runs):
        parts.append(p_block[last:r.start()])
        if idx == target:
            parts.append(_fill_run(r.group(0), esc(line)))
        else:
            parts.append(_clear_run(r.group(0)))
        last = r.end()
    parts.append(p_block[last:])
    result = "".join(parts)
    if line != "" and target is None:
        # 텍스트를 담을 run이 없는 문단(그림 전용 등): 문단 끝에 최소 run 추가
        insert = "<hp:run><hp:t>" + esc(line) + "</hp:t></hp:run>"
        anchor = result.find("<hp:linesegarray")
        if anchor == -1:
            anchor = result.rfind("</hp:p>")
        result = result[:anchor] + insert + result[anchor:]
    return result


def fill_cell_block(block, text):
    """셀 블록(<hp:tc>...</hp:tc>)의 문단들에 text를 채운다.

    text의 \n은 문단 분리. 줄 수가 문단 수보다 많으면 마지막 문단을 복제한다.
    """
    lines = text.split("\n") if text != "" else [""]
    pms = list(P_RE.finditer(block))
    if not pms:
        raise ValueError("셀 안에 문단이 없음")
    paras = [m.group(0) for m in pms]
    if len(lines) > len(paras):
        template = set_para_text(paras[-1], "")
        paras = paras + [template] * (len(lines) - len(paras))
    new_paras = []
    for i, p in enumerate(paras):
        new_paras.append(set_para_text(p, lines[i] if i < len(lines) else ""))
    return block[: pms[0].start()] + "".join(new_paras) + block[pms[-1].end():]


STRUCT_RE = re.compile(r"<hp:cellAddr[^>]*/>|<hp:cellSpan[^>]*/>|<hp:cellSz[^>]*/>")


def struct_sig(xml):
    return (
        len(re.findall(r"<hp:tbl\b", xml)),
        len(re.findall(r"<hp:tc\b", xml)),
        sorted(STRUCT_RE.findall(xml)),
    )


def read_section(hwpx_path, section):
    name = f"Contents/section{section}.xml"
    with zipfile.ZipFile(hwpx_path) as z:
        return z.read(name).decode("utf-8"), name


def write_hwpx(src_path, out_path, section_name, new_xml):
    """원본 ZIP 엔트리 순서를 유지하며 section만 교체해 저장한다."""
    with zipfile.ZipFile(src_path) as z:
        names = z.namelist()
        data = {n: z.read(n) for n in names}
    data[section_name] = new_xml.encode("utf-8")
    tmp = out_path + ".tmp"
    with zipfile.ZipFile(tmp, "w") as z:
        for n in names:
            comp = zipfile.ZIP_STORED if n == "mimetype" else zipfile.ZIP_DEFLATED
            z.writestr(zipfile.ZipInfo(n), data[n], comp)
    if os.path.exists(out_path):
        os.remove(out_path)
    os.replace(tmp, out_path)


def load_targets(map_path):
    with open(map_path, encoding="utf-8-sig") as f:
        data = json.load(f)
    if isinstance(data, list):
        default_table, entries = None, data
    else:
        default_table, entries = data.get("table"), data.get("cells", [])
    targets = []
    for e in entries:
        if "col" not in e or "row" not in e or "text" not in e:
            raise ValueError(f"cells 항목에 col/row/text가 모두 필요: {e}")
        tbl = e.get("table", default_table)
        targets.append({
            "table": int(tbl) if tbl is not None else None,
            "col": int(e["col"]),
            "row": int(e["row"]),
            "text": str(e["text"]),
        })
    if not targets:
        raise ValueError("채울 셀이 없음 (cells 배열이 비었음)")
    return targets


def _label(t):
    base = f'r{t["row"]}c{t["col"]}'
    return base + (f'(table {t["table"]})' if t["table"] is not None else "")


def resolve_targets(cells, targets):
    """각 target을 셀 레코드 1개로 확정한다. 실패 사유는 errors로 모은다."""
    resolved, errors, seen = [], [], set()
    for t in targets:
        matches = [
            c for c in cells
            if c["col"] == t["col"] and c["row"] == t["row"]
            and (t["table"] is None or c["table"] == t["table"])
        ]
        if not matches:
            errors.append(f"{_label(t)}: 해당 주소의 셀 없음 (--list로 확인)")
        elif len(matches) > 1:
            tbls = sorted({c["table"] for c in matches})
            errors.append(f'{_label(t)}: 표 {tbls}에 같은 주소가 있음 — "table" 지정 필요')
        elif matches[0]["nested"]:
            errors.append(f"{_label(t)}: 셀 안에 중첩 표가 있음 — 내부 표의 셀을 지정 (--list 참고)")
        elif matches[0]["start"] in seen:
            errors.append(f"{_label(t)}: 같은 셀을 두 번 지정함")
        else:
            seen.add(matches[0]["start"])
            resolved.append((matches[0], t))
    return resolved, errors


def report_targets(xml, targets):
    """대상 셀들의 현재 값을 기대값과 비교해 PASS/FAIL을 출력한다."""
    cells = scan_cells(xml)
    all_ok = True
    for t in targets:
        matches = [
            c for c in cells
            if c["col"] == t["col"] and c["row"] == t["row"]
            and (t["table"] is None or c["table"] == t["table"])
        ]
        if len(matches) != 1:
            print(f"FAIL {_label(t)}: 대상 셀을 하나로 확정할 수 없음")
            all_ok = False
            continue
        actual = cell_text(xml, matches[0])
        expected = t["text"].rstrip("\n")
        ok = actual == expected
        all_ok = all_ok and ok
        disp = actual.replace("\n", "⏎")
        line = f'{"PASS" if ok else "FAIL"} {_label(t)}: "{disp}"'
        if not ok:
            line += f' (기대: "{expected.replace(chr(10), "⏎")}")'
        print(line)
    return all_ok


def do_list(xml):
    cells = scan_cells(xml)
    tags = TBL_TAG_RE.findall(xml)
    print(f"표 {len(tags)}개")
    for i, tag in enumerate(tags):
        rc = re.search(r'rowCnt="(\d+)"', tag)
        cc = re.search(r'colCnt="(\d+)"', tag)
        dims = f"{rc.group(1)}행 x {cc.group(1)}열" if rc and cc else "크기 미상"
        print(f"[table {i}] {dims}")
        for c in sorted((c for c in cells if c["table"] == i), key=lambda c: (c["row"], c["col"])):
            txt = cell_text(xml, c).replace("\n", "⏎")
            if len(txt) > 40:
                txt = txt[:40] + "…"
            mark = " [중첩표]" if c["nested"] else ""
            print(f'  r{c["row"]}c{c["col"]}{mark}: "{txt}"')


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description="HWPX 표 셀 채우기 (셀 주소 기반, 양식 구조 보존)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("사용법:", 1)[-1],
    )
    ap.add_argument("input", help="입력 .hwpx")
    ap.add_argument("output", nargs="?", help="출력 .hwpx (--map일 때 필수)")
    ap.add_argument("--list", action="store_true", dest="do_list", help="표/셀 주소와 현재 텍스트 출력")
    ap.add_argument("--map", dest="map_path", help="cells.json 경로 (채우기)")
    ap.add_argument("--verify", dest="verify_path", help="cells.json 경로 (값 확인만)")
    ap.add_argument("--section", type=int, default=0, help="섹션 번호 (기본 0)")
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        print(f"FAIL: 입력 파일 없음: {args.input}", file=sys.stderr)
        return 1
    xml, section_name = read_section(args.input, args.section)

    if args.do_list:
        do_list(xml)
        return 0

    if args.verify_path:
        targets = load_targets(args.verify_path)
        return 0 if report_targets(xml, targets) else 1

    if not args.map_path:
        print("FAIL: --list, --map, --verify 중 하나가 필요", file=sys.stderr)
        return 1
    if not args.output:
        print("FAIL: --map에는 출력 경로가 필요", file=sys.stderr)
        return 1
    if os.path.abspath(args.output).lower() == os.path.abspath(args.input).lower():
        print("FAIL: INPUT=OUTPUT 저장 금지 — 다른 출력 경로를 지정", file=sys.stderr)
        return 1

    targets = load_targets(args.map_path)
    cells = scan_cells(xml)
    resolved, errors = resolve_targets(cells, targets)
    if errors:
        for e in errors:
            print("FAIL " + e, file=sys.stderr)
        print(f"채우기 중단: {len(errors)}건 오류, 파일을 쓰지 않음", file=sys.stderr)
        return 1

    new_xml = xml
    for cell, t in sorted(resolved, key=lambda x: -x[0]["start"]):
        block = new_xml[cell["start"]:cell["end"]]
        new_xml = new_xml[: cell["start"]] + fill_cell_block(block, t["text"]) + new_xml[cell["end"]:]

    before, after = struct_sig(xml), struct_sig(new_xml)
    struct_ok = before == after
    write_hwpx(args.input, args.output, section_name, new_xml)
    print(f"저장: {args.output} ({os.path.getsize(args.output):,} bytes, 셀 {len(resolved)}개)")
    print(f'구조 비교: {"PASS" if struct_ok else "FAIL"} (표 {after[0]}개, 셀 {after[1]}개, cellAddr/Span/Sz {"동일" if struct_ok else "변경됨!"})')

    out_xml, _ = read_section(args.output, args.section)
    values_ok = report_targets(out_xml, targets)
    return 0 if (struct_ok and values_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
