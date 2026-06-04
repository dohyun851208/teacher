# HWP/HWPX 양식 작성

HWPX는 ZIP 내부 XML이다. 양식의 표, 이미지, 스타일을 최대한 유지하고 텍스트만 채운다.

## 기본 흐름

1. `.hwp`는 먼저 원본 표 보존 가능성을 판단한다. 한글 COM 사용이 가능하고 HWPX 저장이 빠르게 성공하면 원본 HWP를 한글에서 직접 HWPX로 저장한 파일을 우선 사용한다. 표 기반 양식에서 HWPX 저장이 멈추거나 실패하면 즉시 아래 HWPML2X 우회로 전환한다.
2. `scripts/clone_form.py --analyze 원본.hwpx`로 문단, 표, 텍스트 조각을 확인한다.
3. 단순 기존 텍스트 치환이면 `clone_form.py --map map.json`을 사용한다.
4. 빈 표 셀을 채워야 하면 `Contents/section0.xml`의 표/셀 구조를 분석하고 XML을 직접 수정한다.
5. 편집 결과는 최종 산출물로 `.hwpx`를 유지한다. 다시 `.hwp`로 저장하지 않는다. 최종 HWPX는 가능하면 한글에서 직접 열기 검증한다.
6. 결과 HWPX를 다시 열거나 텍스트 추출해서 주요 값이 유지되는지 검증한다.

## HWPX 빠른 변환 표준 경로

대부분의 `.hwp` 양식은 한글 COM으로 HWPX 변환하는 것이 가장 좋은 1차 경로다. 변환 가능성을 길게 탐색하지 말고 아래 표준 시도를 한 번 수행한다.

1. 한글 COM 객체를 만들고 창을 숨긴다.
2. `RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")`를 먼저 호출한다.
3. `SetMessageBoxMode(0x00020000)`로 대화상자 때문에 멈추는 상황을 줄인다.
4. `Open(input, "", "forceopen:true")`로 원본 HWP를 연다.
5. `SaveAs(output.hwpx, "HWPX", "")`로 HWPX를 저장한다.
6. 저장된 HWPX에 대해 `validate.py`, `clone_form.py --analyze`, 주요 텍스트 포함 여부를 확인한다.

주의:

- HWPX 변환은 최대 1회만 표준 경로로 시도한다.
- `scripts/convert_hwp.py`처럼 외부 레포나 추가 설치에 의존하는 변환기는 COM 표준 경로 실패 뒤 구조 분석 보조용으로만 고려한다.
- COM 변환이 30초 이상 멈추면 한글 프로세스를 정리하고 같은 변환을 반복하지 않는다.
- HWPX 변환이 성공했어도 원본과 결과의 표 개수, 핵심 표의 `rowCnt`/`colCnt` 또는 이에 대응하는 구조가 달라지면 원본 표 보존 실패로 본다.

## HWPX 변환 실패 시 원본 표 보존 우회

기존 `.hwp` 양식의 표가 핵심이고 HWPX 변환 표준 경로가 실패했을 때만 HWPML2X 우회를 사용한다. 이 우회는 최우선 경로가 아니라 원본 표 보존 fallback이다.

- 한글 COM `Open` 또는 `SaveAs(..., "HWPX")`가 30초 이상 멈추거나 보안/변환 문제로 실패하면 같은 시도를 반복하지 않는다.
- 이때 `md2hwpx.py`로 새 HWPX 표를 다시 그리는 방식은 사용하지 않는다. 사용자가 명시적으로 "새 양식으로 다시 만들어도 됨"이라고 한 경우를 제외하면 기존 표가 깨진 산출물이 된다.
- 우선 한글 COM `GetTextFile("HWPML2X", "")`로 원본 HWPML2X를 추출한다.
- HWPML2X 안에서 `TABLE`의 `RowCount`, `ColCount`, `CELL`의 `RowAddr`, `ColAddr`, `ColSpan`, `RowSpan`을 기준으로 목표 셀을 찾고, 빈 `<TEXT CharShape="..."/>` 또는 기존 `<CHAR>`만 교체한다.
- 편집한 HWPML2X는 한글 COM `SetTextFile(hwpml, "HWPML2X", "")`로 다시 불러온 뒤 `.hwp`로 먼저 저장한다. 필요하면 그 `.hwp`를 다시 열어 `.hwpx`로 저장한다.
- 검증은 원본과 결과의 표 개수, 주요 `RowCount`/`ColCount`, 주요 텍스트 포함 여부를 함께 확인한다.
- 이 우회 경로로 만든 `.hwp`/`.hwpx`에는 파일명에 `_원본표_완성본`처럼 원본 표 보존 여부가 드러나게 붙인다.

## 텍스트 추출

- 빠른 확인: `Preview/PrvText.txt`
- 정확한 확인: `Contents/section0.xml`의 `<hp:t>` 텍스트

## 빈 셀 채우기

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
- `INPUT=OUTPUT` 저장은 금지한다. 임시 파일을 만들고 마지막에 이동한다.
- 한글 파일명/경로에서 이동 실패가 날 수 있으면 영문 임시 파일을 사용한 뒤 rename한다.
- 단순 텍스트 삽입은 보통 `fix_namespaces.py` 후처리가 필요 없다.

## 서명 이미지 삽입

개인정보 동의서, 확인서, 신청서처럼 하단에 `성명 : ... (인 또는 서명)` 문구가 있는 양식은 다음 순서가 안정적이다.

1. 원본 `.hwp`는 한글 COM `Open` + `SaveAs(..., "HWPX")`로 먼저 HWPX 작업본을 만든다.
2. 텍스트와 서명 위치는 `clone_form.py --analyze`와 `Contents/section0.xml`의 실제 문단/run을 함께 확인한다.
3. 날짜, 생년월일, 성명 같은 단순 값은 해당 `<hp:t>` 또는 문단 단위로 치환한다.
4. 서명 이미지는 우선 `scripts/insert_signature_hwpx.py`로 넣는다. PowerShell에서 긴 XML 문자열을 `python -c`로 조립하지 않는다. 따옴표가 제거되어 XML이 깨지기 쉽다.
5. 기본 호출 예:

```powershell
$env:PYTHONIOENCODING='utf-8'
python "$SKILL_DIR\scripts\insert_signature_hwpx.py" "원본.hwpx" "서명.png" --name "홍길동"
```

6. `--name`으로 `성명 : 이름` 문단을 찾지 못하면 `--anchor "생년월일 : 1990.01.01          성명 : 홍길동"`처럼 실제 하단 문단의 고유 텍스트를 넘긴다. 동의서 안에는 표 헤더의 `성명`도 있으므로 기본 검색은 마지막 일치 문단을 사용한다.
7. 표시 크기는 기본 25mm 폭이다. 양식의 성명 줄이 좁으면 `--width-mm 20`, 넓으면 `--width-mm 30`처럼 조정한다.
8. 스크립트는 ZIP에 `BinData/signature.png`를 추가하고, `Contents/content.hpf`의 `<opf:manifest>`에 이미지 항목을 등록하며, 서명 자리에는 완전한 `<hp:pic>` 구조와 뒤따르는 `<hp:t/>`를 넣는다.
9. 최종본은 가능하면 한글 COM으로 한 번 `Open` + `SaveAs(..., "HWPX")`를 수행해 미리보기와 내부 리소스명을 한글이 정리하게 한다. 단, COM 이미지 삽입 자체에는 의존하지 않는다.

주의:

- 서명 이미지는 원본 PNG의 투명 배경을 그대로 사용한다.
- `Preview/PrvText.txt`는 COM으로 다시 저장하기 전까지 최신 내용이 아닐 수 있다. 최종 검증은 `Contents/section0.xml`과 `clone_form.py --analyze` 결과를 우선한다.
- COM으로 다시 저장하면 `BinData/signature.png`가 `BinData/image1.png`처럼 바뀔 수 있다. 검증할 때 파일명보다 `content.hpf` 등록 여부, 이미지 개수, 문서 미리보기를 확인한다.
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
- 한글 1글자 폭은 대략 `pt * ratio/100 * 100` HWPUNIT 수준으로 보고 여유 있게 줄인다.
- 행 높이가 낮은 고정 행이면 줄바꿈보다 약칭을 우선한다.

압축 예:

- 연수명: `AIEP선도교사역량강화`, `에듀테크수업평가설계`
- 기간: `25.12.14~21`, `25.11~26.01`
- 기관: `인천광역시교육청AI융합교육원`이 너무 길면 `인천AI융합교육원`

## 검증

- `python scripts/validate.py 결과.hwpx`
- `clone_form.py --analyze 결과.hwpx`
- `python scripts/verify_hwpx.py --source 원본.hwpx --result 결과.hwpx`
- 주요 값 count 확인
- 가능하면 한글에서 PDF로 저장 후 첫 페이지를 이미지로 렌더링해 잘림과 겹침을 확인한다.
