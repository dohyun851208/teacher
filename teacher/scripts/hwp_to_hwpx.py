#!/usr/bin/env python3
"""HWP -> HWPX 1회 변환 (한글 COM 표준 경로).

원본 .hwp를 편집 가능한 임시 .hwpx 작업본으로 꺼내는 표준 스크립트다.
최종 완성본을 만들 때는 사용하지 않는다(완성본 COM 재저장 금지).

사용법:
    python hwp_to_hwpx.py "원본.hwp" -o "작업본.hwpx"
    python hwp_to_hwpx.py "원본.hwp"            # 원본 옆에 같은 이름 .hwpx 생성

주의:
    - win32com.client.Dispatch를 사용한다. gencache.EnsureDispatch는 첫 실행에서
      캐시 재생성 중 "ImportError: cannot import name '_get_good_object_'" 경고를
      출력할 수 있는데, 이는 변환 성공과 무관한 무해한 메시지다. 그 경고만 보고
      실패로 판단하거나 재시도하지 말 것. 성공 판정은 이 스크립트의 OK/FAIL
      출력(출력 파일 존재 + 크기)으로 한다.
    - 30초 이상 멈추면 셸 타임아웃으로 중단하고 Hwp 프로세스를 정리한다.
      같은 변환을 반복하지 않는다.
    - pywin32 필요: pip install pywin32
"""

import argparse
import os
import sys


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    ap = argparse.ArgumentParser(description="HWP -> HWPX 1회 변환 (한글 COM)")
    ap.add_argument("input", help="원본 .hwp 경로")
    ap.add_argument("-o", "--output", help="출력 .hwpx 경로 (기본: 원본과 같은 이름의 .hwpx)")
    args = ap.parse_args()

    src = os.path.abspath(args.input)
    if not os.path.isfile(src):
        print(f"FAIL: 원본 없음: {src}", file=sys.stderr)
        return 1
    dst = os.path.abspath(args.output) if args.output else os.path.splitext(src)[0] + ".hwpx"
    if dst.lower() == src.lower():
        print("FAIL: 출력 경로가 원본과 같음", file=sys.stderr)
        return 1
    if os.path.exists(dst):
        try:
            os.remove(dst)
        except OSError as e:
            print(f"FAIL: 기존 출력 파일 삭제 불가(사용 중?): {dst} ({e})", file=sys.stderr)
            return 1
    out_dir = os.path.dirname(dst)
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    try:
        import win32com.client as win32
    except ImportError:
        print("FAIL: pywin32 필요 (pip install pywin32)", file=sys.stderr)
        return 1

    hwp = None
    try:
        hwp = win32.Dispatch("HWPFrame.HwpObject")
        hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
        hwp.SetMessageBoxMode(0x00020000)
        try:
            hwp.XHwpWindows.Item(0).Visible = False
        except Exception:
            pass
        ok = hwp.Open(src, "", "forceopen:true")
        if ok is False:
            print(f"FAIL: Open 실패: {src}", file=sys.stderr)
            return 1
        ok = hwp.SaveAs(dst, "HWPX", "")
        if ok is False:
            print(f"FAIL: SaveAs(HWPX) 실패: {dst}", file=sys.stderr)
            return 1
    finally:
        if hwp is not None:
            try:
                hwp.Quit()
            except Exception:
                pass

    if os.path.isfile(dst) and os.path.getsize(dst) > 0:
        print(f"OK {dst} ({os.path.getsize(dst):,} bytes)")
        return 0
    print(f"FAIL: 출력 파일이 생성되지 않음: {dst}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
