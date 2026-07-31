# HWP/HWPX 양식 작성

HWPX는 ZIP 내부 XML이다. 양식의 표, 이미지, 스타일을 최대한 유지하고 텍스트만 채운다.

## 실행 셸

셸은 스킬이나 대화 세션 전체가 아니라 현재 작업 단위마다 선택한다. `.hwp`/`.hwpx`를 열기, 변환, 편집, 검증하거나 한컴 COM을 호출하는 모든 셸 명령은 PowerShell에서 실행한다. 현재 에이전트가 Bash를 사용 중이면 PowerShell 도구를 선택하고, PowerShell 문법을 Bash로 번역하지 않는다. PowerShell 도구를 직접 선택할 수 없는 환경에서는 단순 명령은 `powershell.exe -NoProfile -Command`, 여러 줄 로직은 파일 쓰기 도구로 만든 UTF-8 `.ps1`과 `powershell.exe -NoProfile -File`로 비대화식 실행한다. 인자 없이 `powershell.exe`를 실행해 대화형 셸을 열지 않는다.

XLSX, 일반 Python, HTML workflow를 수행한 뒤 이 workflow로 돌아오면 PowerShell UTF-8 초기화를 다시 실행한다. 셸 사이에서 현재 디렉터리, `$py`, 환경변수가 유지된다고 가정하지 말고 절대경로를 우선한다.

## 새 PC 최초 1회 셋업

이 스킬을 처음 쓰는 PC(다른 교사 컴퓨터 포함)에서는 첫 HWP 작업 전에 환경 점검 스크립트를 1회 실행한다:

```powershell
& $py "scripts/setup_env.py"
```

- pywin32, 한글 COM ProgID, HWP 자동화 보안모듈 등록 상태를 점검하고, 보안모듈이 없으면 스킬 동봉 `scripts/FilePathCheckerModule.dll`을 `%LOCALAPPDATA%\FilePathCheckerModule\`로 복사해 `HKCU\Software\HNC\HwpAutomation\Modules`(구버전 호환으로 `HwpUserAction\Modules`에도)에 등록한 뒤, 실제 한글 COM에서 `RegisterModule` 반환값 True까지 검증한다.
- 멱등이다. 이미 설정된 PC에서 다시 실행하면 아무것도 변경하지 않고 PASS만 출력하므로, 설정 여부가 불확실하면 그냥 실행한다.
- 보안모듈이 등록되지 않은 PC에서는 한글이 자동화의 파일 접근마다 보안 승인창("파일의 손상 또는 유출의 위험...")을 띄우고, 무인 실행은 그 창에서 멈춘다. `hwp_to_hwpx.py`가 `WARN: 보안모듈 등록 실패`를 출력하면 이 스크립트를 먼저 실행하고 변환을 다시 시도한다.
- pywin32 FAIL이면 `python -m pip install pywin32` 후 재실행. 한글 COM FAIL이면 한글(한컴오피스) 설치가 선행되어야 한다.

## 기본 흐름

최종 산출물이 HWPX일 때의 기본 경로:

원본 `.hwp` -> `hwp_to_hwpx.py`로 임시 `.hwpx` 변환 -> `fill_cells.py --list`로 셀 주소 확인 -> `cells.json` 작성 -> `fill_cells.py --map`으로 채우기(자동 검증 포함) -> `validate.py` 구조 검증 -> 최종 `*_완성본.hwpx` 저장 -> 임시 파일 삭제

1. `.hwp` 원본은 `scripts/hwp_to_hwpx.py`(한글 COM)로 임시 `.hwpx` 작업본을 1회 만든다. 원본이 이미 `.hwpx`이면 원본을 덮어쓰지 말고 복사본을 작업본으로 둔다.
2. `scripts/fill_cells.py --list 작업본.hwpx`로 표 인덱스, 셀 주소, 현재 텍스트를 확인한다. 문단·run 구조까지 봐야 하면 `scripts/clone_form.py --analyze`를 함께 쓴다.
3. 단순 기존 텍스트 치환이면 `clone_form.py --map map.json`을 사용한다.
4. 표 셀 채우기(빈 셀·치환 모두)는 `scripts/fill_cells.py --map cells.json`을 기본으로 사용한다. 스크립트가 표현하지 못하는 편집(한 셀 안 서식 혼합 등)만 `Contents/section0.xml`을 직접 수정한다.
5. 편집 결과는 최종 산출물로 `.hwpx`만 유지한다. 다시 `.hwp`로 저장하지 않는다.
6. `scripts/validate.py` 구조 검증과 `Contents/section0.xml` 직접 확인으로 주요 값이 유지되는지 확인한다.
7. 임시 변환본, 압축 해제 폴더, 임시 스크립트 산출물은 삭제한다.

기본으로 하지 않을 것:

- `_완성본.hwp` 생성
- 완성된 HWPX를 한컴 COM으로 재저장
- 검증용 HWPX 별도 생성
- PDF/이미지 렌더링 검증

## HWP를 임시 HWPX로 변환

한글 COM 자동화 객체는 항상 사용 가능하다고 전제한다. 사용 가능 여부를 사용자에게 묻거나 사전 점검 코드를 돌리지 말고 바로 변환을 시작한다. 이는 최종 HWP를 만드는 과정이 아니라, 원본 HWP를 편집 가능한 HWPX로 꺼내는 1회 변환이다.

표준 실행은 번들 스크립트다. 변환 코드를 손으로 다시 쓰지 않는다:

```powershell
& $py "scripts/hwp_to_hwpx.py" "원본.hwp" -o "임시작업본.hwpx"
```

성공 판정은 스크립트의 `OK`/`FAIL` 출력(출력 파일 존재 + 크기)으로 한다. COM 코드를 직접 써야 할 때는 `win32com.client.Dispatch("HWPFrame.HwpObject")`를 사용한다. `gencache.EnsureDispatch`는 첫 실행에서 캐시 재생성 중 `ImportError: cannot import name '_get_good_object_'` 같은 경고를 출력할 수 있는데, 변환 성공 여부와 무관한 무해한 메시지다. 이 경고만 보고 실패로 판단하거나 재시도하지 않는다.

수동 COM 변환 절차(참고):

1. 한글 COM 객체를 만들고 창을 숨긴다.
2. `RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")`를 먼저 호출한다.
3. `SetMessageBoxMode(0x00020000)`로 대화상자 때문에 멈추는 상황을 줄인다.
4. `Open(input, "", "forceopen:true")`로 원본 HWP를 연다.
5. `SaveAs(temp_work.hwpx, "HWPX", "")`로 임시 HWPX 작업본을 저장한다.
6. 저장된 임시 HWPX에 대해 `validate.py`, `clone_form.py --analyze`, 주요 텍스트 포함 여부를 확인한다.

주의:

- 스크립트가 `WARN: 보안모듈 등록 실패`를 출력하면 변환 중 한글 보안 승인창이 뜨거나 무인 실행이 멈출 수 있다. `scripts/setup_env.py`를 실행해 보안모듈을 등록한 뒤 다시 변환한다.
- HWPX 변환은 최대 1회만 표준 경로로 시도한다.
- 한글 COM은 이 준비 단계에만 사용한다. 최종 `*_완성본.hwpx`를 정리하려고 `Open` + `SaveAs(..., "HWPX")`를 다시 수행하지 않는다.
- `scripts/convert_hwp.py`처럼 외부 레포나 추가 설치에 의존하는 변환기는 COM 표준 경로 실패 뒤 구조 분석 보조용으로만 고려한다.
- COM 변환이 30초 이상 멈추면 한글 프로세스를 정리하고 같은 변환을 반복하지 않는다.
- HWPX 변환이 성공했어도 원본과 결과의 표 개수, 핵심 표의 `rowCnt`/`colCnt` 또는 이에 대응하는 구조가 달라지면 원본 표 보존 실패로 보고 자동 fallback하지 않는다. 사용자 승인이나 별도 지시를 받은 뒤 비기본 복구 경로를 선택한다.

## HWPX 변환 실패 시

기본 경로에서는 HWPX 변환 실패 뒤 자동 우회를 하지 않는다. 실패 사실, 멈춘 단계, 원본 보존 위험을 사용자에게 짧게 알리고 다음 지시를 받는다.

- 한글 COM `Open` 또는 `SaveAs(..., "HWPX")`가 30초 이상 멈추거나 보안/변환 문제로 실패하면 같은 시도를 반복하지 않는다.
- HWPML2X 추출, `SetTextFile`, 임시/최종 HWP 저장은 기본으로 사용하지 않는다.
- `md2hwpx.py`로 새 HWPX 표를 다시 그리는 방식도 사용하지 않는다. 사용자가 명시적으로 "새 양식으로 다시 만들어도 됨"이라고 한 경우를 제외하면 기존 표가 깨진 산출물이 된다.
- 가능한 선택지는 사용자가 변환된 HWPX를 제공하기, 비기본 HWPML2X 복구 경로를 승인하기, 새 HWPX 양식 재작성을 승인하기 중 하나로 정리해 제안한다.

## 텍스트 추출

- 빠른 확인: `Preview/PrvText.txt`
- 기본 확인: ZIP 안의 `Contents/section0.xml`을 열고 `<hp:t>` 텍스트, 표 셀 주소, 입력값 포함 여부를 직접 확인한다.
- `scripts/text_extract.py`는 선택 검증이다. 이 스크립트는 `python-hwpx`가 없으면 실패할 수 있으므로 기본 경로에 넣지 않는다.
- 이미 `python-hwpx`가 설치되어 있고 표 텍스트를 추가로 보고 싶을 때만 `& $py "scripts/text_extract.py" "결과.hwpx" --include-tables`를 사용한다.
- 사용자가 제공한 원본은 정상 문서로 간주한다. 콘솔의 한글 깨짐만으로 원본 손상이나 인코딩 오류를 판단하거나 원본을 재인코딩하지 않는다. 명시적 파싱이나 구조 검증도 함께 실패한 경우에만 raw bytes를 확인한다. `.hwp`는 바이너리이고 `.hwpx`는 ZIP 컨테이너이므로 파일 자체를 UTF-8 텍스트로 검사하지 않는다.

## PowerShell 실행과 UTF-8

PowerShell에서 여러 줄 Python 코드를 실행할 때는 Bash식 heredoc 또는 긴 `python -c "..."` 인자 전달을 피한다. BOM, 따옴표, 한글 경로 때문에 분석 단계가 실패하기 쉽다.

임시 `.py`/`.json` 파일을 PowerShell 리다이렉트(`>`, `Out-File`, `Set-Content`)로 만들지 않는다. 파일 앞에 BOM이 붙어 첫 글자에서 파싱이 실패한다. 에이전트의 파일 쓰기 도구 또는 Python `encoding="utf-8"` 쓰기로 만든다.

Codex 데스크톱에서는 먼저 `load_workspace_dependencies`로 번들 Python 경로를 확인하고 `$py`에 담아 실행한다. bare `python`을 기본 예시로 쓰지 않는다. HWP COM 변환 fast path에는 `pywin32`/`win32com`이 필요하고, XML 조작 도구에는 `lxml`이 필요할 수 있으므로 번들 Python 또는 해당 모듈이 있는 고정 Python을 사용한다.

Claude Code에는 `load_workspace_dependencies`가 없다. Windows에서 `(Get-Command python).Source`는 실행되지 않는 스토어 스텁(`...\WindowsApps\python.exe`)을 반환하는 경우가 많으므로 그 결과를 그대로 쓰지 않는다. 다음 순서로 실제 python.exe를 찾아 `$py`에 담고, `import win32com`으로 pywin32까지 확인한 뒤 진행한다. 존재하지 않는 도구를 찾느라 멈추지 않는다.

```powershell
$py = @(Get-ChildItem "$env:LOCALAPPDATA\Programs\Python\Python3*\python.exe", `
  "C:\Program Files\Python3*\python.exe" -ErrorAction SilentlyContinue) |
  Select-Object -First 1 -ExpandProperty FullName
if (-not $py) {
  $c = (Get-Command python -ErrorAction SilentlyContinue).Source
  if ($c -and $c -notlike '*WindowsApps*') { $py = $c }
}
& $py -c "import win32com; print('py ok')"
```

안정적인 실행 템플릿:

```powershell
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
$py = "<load_workspace_dependencies로 확인한 python.exe 경로>"
$code = @'
import sys
print("ok")
'@
$code | & $py -c "import sys; exec(sys.stdin.read().lstrip(chr(0xfeff)))"
```

같은 분석 코드를 반복할 때는 임시 인자 조립을 계속 고치지 말고 스크립트 파일 또는 기존 `scripts/` 도구로 옮긴다.

## 빈 셀 채우기

기본 경로는 `scripts/fill_cells.py`다. 셀 주소 확인, 채우기, 구조 비교, 값 검증을 한 번에 처리하므로 채우기 코드를 손으로 다시 쓰지 않는다:

```powershell
& $py "scripts/fill_cells.py" "작업본.hwpx" --list
& $py "scripts/fill_cells.py" "작업본.hwpx" "결과.hwpx" --map "cells.json"
```

`cells.json` 형식 — `text`의 `\n`은 문단 분리, `""`는 셀 비우기, 표 인덱스는 `--list` 출력의 `[table N]`:

```json
{
  "table": 1,
  "cells": [
    {"col": 0, "row": 2, "text": "5"},
    {"col": 3, "row": 2, "text": "첫 줄\n둘째 줄"},
    {"table": 0, "col": 0, "row": 0, "text": "제목 치환"}
  ]
}
```

같은 (col,row)가 여러 표에 있는데 `table` 지정이 없으면 스크립트가 파일을 쓰지 않고 오류로 알린다. 대상 셀 안에 중첩 표가 있으면 내부 표의 셀을 지정한다. `--map` 출력의 구조 비교와 셀 값이 모두 PASS면 그 검증을 신뢰하고 같은 확인을 반복하지 않는다.

아래 수동 편집 규칙은 `fill_cells.py`가 표현하지 못하는 편집(한 셀 안 서식 혼합, run 단위 스타일 변경 등)에만 사용한다.

빈 run의 일반 패턴:

```xml
<hp:run charPrIDRef="N"/>
```

채운 패턴:

```xml
<hp:run charPrIDRef="N"><hp:t>텍스트</hp:t></hp:run>
```

주의:

- 빈 문자열을 순차 replace로 skip하지 않는다. 같은 빈 run이 반복 매칭될 수 있으므로 위치 또는 셀 주소 기반으로 치환한다.
- 이미 문단과 run이 있는 표 셀은 새 문단을 재작성하기보다 원본 `<hp:p>`와 `<hp:run>` 개수를 유지하며 기존 run 내부 텍스트만 바꾼다.
- 한 문단에 run이 여러 개 있으면 첫 run에 새 텍스트를 넣고 나머지 run은 빈 run으로 정리한다. 그렇지 않으면 기존 텍스트가 뒤에 남아 중복될 수 있다.
- 새 줄 수가 원본 문단 수보다 많으면 셀 폭 기준으로 내용을 더 짧게 압축하거나 마지막 문단에 합친다. 검증 통과를 위해 임의 문단, 빈 run, XML 주석을 덧붙이지 않는다.
- 편집 전후 같은 셀의 `cellAddr`, `cellSpan`, `cellSz`, `cellMargin`, `subList` 속성, 문단 수, run 수가 유지되는지 비교한다. 값이 줄어들면 양식 보존 실패로 보고 다시 편집한다.
- `INPUT=OUTPUT` 저장은 금지한다. 임시 파일을 만들고 마지막에 이동한다.
- 한글 파일명/경로에서 이동 실패가 날 수 있으면 영문 임시 파일을 사용한 뒤 rename한다.
- 단순 텍스트 삽입은 보통 `fix_namespaces.py` 후처리가 필요 없다.

## 서명 이미지 삽입

개인정보 동의서, 확인서, 신청서처럼 하단에 `성명 : ... (인 또는 서명)` 문구가 있는 양식은 다음 순서가 안정적이다.

1. 원본 `.hwp`는 한글 COM `Open` + `SaveAs(..., "HWPX")`로 먼저 임시 HWPX 작업본을 만든다.
2. 텍스트와 서명 위치는 `clone_form.py --analyze`와 `Contents/section0.xml`의 실제 문단/run을 함께 확인한다.
3. 날짜, 생년월일, 성명 같은 단순 값은 해당 `<hp:t>` 또는 문단 단위로 치환한다.
4. 서명 이미지는 우선 `scripts/insert_signature_hwpx.py`로 넣는다. PowerShell에서 긴 XML 문자열을 `python -c`로 조립하지 않는다. 따옴표가 제거되어 XML이 깨지기 쉽다.
5. 기본 호출 예:

```powershell
$env:PYTHONIOENCODING='utf-8'
& $py "$SKILL_DIR\scripts\insert_signature_hwpx.py" "원본.hwpx" "서명.png" --name "홍길동"
```

6. `--name`으로 `성명 : 이름` 문단을 찾지 못하면 `--anchor "생년월일 : 1990.01.01          성명 : 홍길동"`처럼 실제 하단 문단의 고유 텍스트를 넘긴다. 동의서 안에는 표 헤더의 `성명`도 있으므로 기본 검색은 마지막 일치 문단을 사용한다.
7. 표시 크기는 기본 25mm 폭이다. 양식의 성명 줄이 좁으면 `--width-mm 20`, 넓으면 `--width-mm 30`처럼 조정한다.

### 배치 방식 (inline / overlay)

기본값 `inline`은 서명을 글자처럼(`treatAsChar="1"`) 줄 안에 넣는다. 위치는 정확하지만 **서명 높이가 글자 높이보다 크면 그 줄이 벌어진다**. 1쪽 고정 양식에서는 내용이 다음 쪽으로 밀릴 수 있다. 스크립트는 서명 높이가 글자 높이의 1.2배를 넘으면 `WARN`을 출력한다.

`--overlay`는 서명을 **글 뒤로** 띄운다(`treatAsChar="0"`, `textWrap="BEHIND_TEXT"`, `horzRelTo="COLUMN"`). 줄 높이가 변하지 않아 **원본 쪽수와 표 레이아웃이 보존되고**, 양식의 `(서명)` 표기와 이름이 서명 위에 그대로 읽힌다. 1쪽짜리 신청서·서약서·출품원서의 기본 선택으로 삼는다.

`IN_FRONT_OF_TEXT`(글 앞으로)를 쓰지 않는다. 서명이 `(서명)` 표기를 덮어버려 제출본으로 못 쓴다.

#### 권장 절차: 앵커 문단 + 절대 좌표

서명이 들어갈 그 줄에 앵커를 걸고 run을 쪼개는 방식은 쓰지 않는다. 원본 XML을 더 많이 건드리면서 위치는 더 부정확하다. 대신 한글이 실제로 하는 방식을 따른다 — **안정적인 문단에 앵커를 걸고 위치는 절대 좌표로 준다.**

```powershell
& $py "$SKILL_DIR\scripts\insert_signature_hwpx.py" "원본.hwpx" "서명.png" `
    --overlay --anchor-para "소    속 :" `
    --width-mm 26 --horz-offset-mm 41.8 --vert-offset-mm 16.8
```

- `--anchor-para`: 서명 블록의 **첫 줄**(예: `소    속 :`)을 준다. 이 문단의 run은 전혀 수정하지 않는다.
- `--horz-offset-mm`: **단(표 셀) 좌측**에서의 거리. 문단 들여쓰기에 영향받지 않는다.
- `--vert-offset-mm`: 앵커 문단 상단에서의 거리. **양수가 아래쪽**이다. 음수는 윗줄로 올라간다.

#### 반드시 지킬 것 세 가지

**1. `imgClip`은 원본 이미지 좌표계다.** HWPX는 크기를 셋으로 나눠 쓴다. 이걸 섞으면 이미지가 조용히 잘린다.

| 요소 | 좌표계 | 값 |
| --- | --- | --- |
| `orgSz`, `imgRect`, `imgClip` | **원본 이미지** (픽셀 x 75, 96dpi) | 212px 이미지 -> 15900 |
| `curSz`, `sz` | 페이지에 그릴 크기 | 20mm -> 5669 |
| `scaMatrix` e1/e5 | 둘의 비율 | 5669/15900 = 0.356541 |

`imgClip`에 표시 크기를 넣으면 원본에서 **그 크기만큼만 잘라내** 확대해 그린다. 212px 서명을 20mm로 넣으면 왼쪽 36%만 남아 첫 획만 보인다. 증상이 "서명이 다 잘려 일부만 보임"이면 여기다.

**2. 음수 `vertOffset`은 0으로 잘린다.** `vertRelTo="PARA"` + `vertAlign="TOP"`에서 그림은 앵커 문단 상단 위로 못 올라간다. 원하는 자리보다 **위에 있는 문단에 앵커를 걸고 양수 오프셋으로 내려야** 한다. 음수를 줘도 오류 없이 앵커 문단 상단에 붙어버리므로, XML만 봐서는 실패를 알 수 없다.

**3. 중첩표에서 문단을 정규식으로 자르지 않는다.** `<hp:p\b.*?</hp:p>`는 표를 품은 문단에서 **안쪽 문단의 닫는 태그**에 먼저 걸려 엉뚱한 문단을 반환한다. 어느 문단에 앵커가 걸렸는지 XML 파싱으로 판정하려 하지 말고 아래의 실측 보정을 쓴다.

#### 위치는 `place_signature.py`가 실측해서 맞춘다

오프셋의 원점(COLUMN이 쪽 여백인지 셀인지, PARA가 어느 문단인지)은 문서 구조마다 달라 XML만으로 확정할 수 없다. **좌표를 손으로 계산하지 말고 이 스크립트를 쓴다.** 탐침 1회 → 임시 PDF 렌더 → 실측 → 역산 → 재생성 → 검증을 자동으로 하고, 보통 오차 0.05mm 안에 들어온다.

먼저 양식이 어떻게 생겼는지 mm로 확인한다:

```powershell
& $py "$SKILL_DIR\scripts\place_signature.py" "작업본.hwpx" "서명.png" `
    --report --find "홍길동" --find "(서명)"
```

그다음 배치한다. 목표를 좌표로 주지 않고 **기준 글자로** 준다:

```powershell
& $py "$SKILL_DIR\scripts\place_signature.py" "작업본.hwpx" "서명.png" `
    --output "원본_완성본.hwpx" `
    --anchor-para "4. 위 사항을 준수하겠습니다" --after-text "홍길동" --width-mm 24
```

- `--after-text`: 서명이 **그 글자가 끝나는 지점**에서 시작하고 그 줄에 세로 중앙 정렬된다.
- 바로 아래에 다른 개체(다른 출품자의 도장·서명란)가 있으면 **자동으로 그 위까지만** 내린다. 남의 표시를 덮지 않는 것이 우선이다.
- `--anchor-para`는 목표보다 **위에 있는** 문단이어야 한다. 아래 문단을 주면 음수 오프셋이 필요해지고, 스크립트가 그 자리에서 막고 알려준다.
- 좌표를 이미 알면 `--target-left-mm` / `--target-bottom-mm`으로 직접 준다 (승인받은 배치를 재현할 때).

임시 PDF는 검증용이고 자동 삭제된다. 완성본 HWPX는 COM으로 재저장하지 않는다.

배치 기준값(사용자가 한글에서 직접 잡은 배치에서 역산):

- **가로**: 타이핑된 이름이 끝나는 x. 서명이 `(서명)` 표기를 덮는 것은 정상이다.
- **세로**: 이름 줄에 세로 중앙 정렬. 아래가 막혀 있으면 줄에서 위로 걸리게 한다.

#### 좌표는 추측하지 말고 원본에서 잰다

`Contents/section0.xml`의 `<hp:lineseg vertpos vertsize>`에는 한글이 계산해 둔 **실제 줄 위치**가 들어 있다. 이 값을 읽으면 서명이 어느 줄에 걸리는지 열어보지 않고 계산할 수 있다.

```python
seg = re.search(r"<hp:lineseg\b[^>]*/>", para)
vertpos, vertsize = ...   # 셀 상단 기준 줄의 위 끝 / 줄 높이 (HWPUNIT, 1mm ≈ 283)
```

배치 기준:

- **줄 아래에 여백이 있으면** 이름 줄 바로 아래에 놓는다. 서명이 이름 밑에 깔려 가장 자연스럽다.
- **줄 간격이 촘촘하면**(다음 출품자 줄이 바로 붙어 있는 등) 이름 줄에 겹쳐 놓는다. `BEHIND_TEXT`라 글자는 그대로 읽힌다. 서명 폭을 18mm 안팎으로 줄여 위아래 줄 침범을 줄인다.
- 그림을 찾을 때 `textWrap="BEHIND_TEXT"`로 거르지 않는다. 양식 원본의 로고·머리그림도 같은 값일 수 있다. **`binaryItemIDRef="signature"`로 특정한다.**

#### 그 밖의 옵션

- 줄 안에 반드시 들어가야 하면 `--fit-line`으로 글자 높이에 맞춰 축소한다. `--fit-line 1.4`는 글자 높이의 1.4배. 위치는 확실하지만 서명이 작아진다.
- `--anchor-para` 없이 `--anchor`만 주면 앵커 run 앞 텍스트 폭으로 가로 위치를 **추정**한다(한글 1em, ASCII 0.5em에 보정 1.1배). 편하지만 몇 mm 어긋날 수 있으니 좌표를 잴 수 있으면 `--anchor-para`를 쓴다.
- 서명 외에 **도장**을 함께 넣는 양식이 있다. 도장은 보통 이름 줄에 겹쳐 정사각형으로 들어간다(예: 8.9mm x 8.9mm). 서명과 별개 자산이므로 사용자에게 확인한다.
8. 스크립트는 ZIP에 `BinData/signature.png`를 추가하고, `Contents/content.hpf`의 `<opf:manifest>`에 이미지 항목을 등록하며, 서명 자리에는 완전한 `<hp:pic>` 구조와 뒤따르는 `<hp:t/>`를 넣는다.
9. 최종본은 한글 COM으로 `Open` + `SaveAs(..., "HWPX")` 재저장하지 않는다. `validate.py`, `Contents/section0.xml`, `Contents/content.hpf`, 주요 값 포함 여부로 검증한다.

주의:

- 서명 이미지는 원본 PNG의 투명 배경을 그대로 사용한다.
- `Preview/PrvText.txt`는 최신 내용이 아닐 수 있다. 최종 검증은 `Contents/section0.xml`과 주요 값 직접 확인을 우선한다.
- COM 재저장은 기본 금지이므로 `BinData/signature.png` 파일명을 정리하려고 다시 저장하지 않는다. 검증할 때 파일명보다 `content.hpf` 등록 여부, 이미지 개수, XML 참조를 확인한다.
- 원본 `.hwp`에는 쓰지 말고, 변환본과 최종본을 별도 경로로 만든다.
- 직접 ZIP을 다시 쓸 때 `mimetype` 엔트리는 `ZIP_STORED`로 유지한다.
- `scripts/insert_signature_hwpx.py`를 고쳐야 할 때도 텍스트/XML 파일은 `encoding="utf-8"` 또는 명시적 `.decode("utf-8")`/`.encode("utf-8")`로 처리한다.

## 표 구조 분석

- 겹표 여부: `re.findall(r'<hp:tbl\b', xml)` 개수 확인
- 각 셀의 주소: `<hp:cellAddr colAddr="C" rowAddr="R"/>`
- 각 셀의 크기: `<hp:cellSz width="W" height="H"/>`
- 각 셀의 텍스트: 해당 `<hp:tc>...</hp:tc>` 내부의 `<hp:t>`

열 헤더와 데이터 열은 반드시 실제 셀 주소로 매핑한다. 예를 들어 `연수기간(차시)`처럼 두 항목이 한 열에 합쳐진 양식은 기간과 시간을 같은 셀에 압축해 써야 한다.

## 셀 폭에 맞춘 작성

- 폰트 크기: `Contents/header.xml`의 `<hh:charPr id="N" height="H">`, `H/100 = pt`
- 유효 폭: `cellSz width - 좌우 margin`
- 한글 1글자 폭은 대략 `pt * 0.9~1.0 * 100` HWPUNIT 수준으로 보고 여유 있게 줄당 글자 수를 잡는다.
- 기본 원칙은 내용을 축약하지 않고 의미 단위로 강제 줄바꿈하는 것이다. 한 문단을 긴 한 줄로 넣지 말고 여러 문단 또는 여러 짧은 줄로 나눈다.
- 좁은 열이 많은 단계형·목록형 표는 짧은 제목 1줄과 짧은 불릿 3~4개로 나눈다. 예시 문장도 `예)`, 상황, 요청을 2~4줄로 분리한다.
- 행 높이가 낮은 1쪽 고정 양식은 페이지 수를 유지한다. 이때는 행 높이를 크게 늘리기보다 양식에 있는 작은 글자 스타일을 먼저 찾고, 셀 안에서 짧은 의미 줄로 나눈다.
- 내용이 물리적으로 들어가지 않는 경우에는 임의로 삭제하지 말고, 중요도가 낮은 항목을 `확인 필요` 또는 별도 첨부/추가자료 대상으로 남길지 판단한다.

줄당 글자 수의 보수적 기준:

| 셀 유효 폭 | 권장 줄 길이 | 작성 방식 |
| --- | --- | --- |
| 5,000~7,000 HWPUNIT | 한글 5~8자 | 명사구 중심, 2~3줄 |
| 7,000~11,000 HWPUNIT | 한글 8~12자 | 짧은 불릿, 긴 기관명은 줄바꿈 |
| 11,000~18,000 HWPUNIT | 한글 12~18자 | 제목 1줄 + 불릿 3~4개 |
| 18,000~30,000 HWPUNIT | 한글 20~30자 | 문장 1개를 2~3줄로 분할 |
| 30,000 HWPUNIT 이상 | 한글 35~55자 | 문단형 가능, 필요 시 작은 글자 스타일 사용 |

## 검증

기본 검증은 구조와 주요 입력값 확인으로 끝낸다. 검증용 HWPX를 별도로 만들거나, 완성본을 한컴 COM으로 재저장하거나, PDF/이미지 렌더링을 수행하지 않는다.

- `& $py "scripts/validate.py" "결과.hwpx"`
- `fill_cells.py --map`은 저장 직후 구조 비교(표/셀 개수, cellAddr/cellSpan/cellSz)와 대상 셀 값 PASS/FAIL 리포트를 자동 출력한다. 모두 PASS면 셀 값 재확인을 반복하지 않는다. 나중에 다시 확인할 일이 생기면 `& $py "scripts/fill_cells.py" "결과.hwpx" --verify "cells.json"`을 쓴다.
- ZIP 안의 `Contents/section0.xml`에서 주요 입력값, 표 셀 주소, 병합, 문단/run 구조를 직접 확인한다.
- 주요 값 count 확인
- 원본 대비 표 개수, 셀 주소, 병합, 셀 크기, 여백, 문단 수, run 수를 비교한다. 남은 기존 텍스트나 중복 텍스트는 직접 확인한다.
- `scripts/verify_hwpx.py`는 구조 차이가 의심될 때만 선택 검증으로 사용한다.
- `scripts/text_extract.py`는 `python-hwpx`가 이미 있을 때만 선택 검증으로 사용한다.
- 이전 양식의 고유 placeholder나 예시 문구가 남았는지 검색한다. 예: `(     분)`, `○○`, 원본 예시 문장.
- 검증 경고를 없애려고 section 크기 보정용 XML 주석, 의미 없는 빈 run, 임의 문단을 추가하지 않는다. 그런 보정은 통과처럼 보이지만 제출본 품질을 낮춘다.
- 사용자가 요청했거나 최종 제출본에서 글자 겹침·잘림 위험이 높다고 판단될 때만 시각 검증을 제안한다. 이 경우에도 먼저 사용자에게 말하고, HWPX를 열더라도 재저장하지 않는다.
- 검증 뒤 임시 변환본, 임시 압축 해제 폴더, 분석용 임시 파일을 삭제한다.
