# HWP/HWPX 양식 작성

HWPX는 ZIP 내부 XML이다. 양식의 표, 이미지, 스타일을 최대한 유지하고 텍스트만 채운다.

## 기본 흐름

1. `.hwp`는 먼저 HWPX로 변환한다. 한글 COM 사용이 가능하면 원본 HWP를 한글에서 직접 HWPX로 저장한 파일을 우선 사용한다. `scripts/convert_hwp.py` 변환본은 COM이 불가능할 때나 구조 분석 보조용으로 사용한다.
2. `scripts/clone_form.py --analyze 원본.hwpx`로 문단, 표, 텍스트 조각을 확인한다.
3. 단순 기존 텍스트 치환이면 `clone_form.py --map map.json`을 사용한다.
4. 빈 표 셀을 채워야 하면 `Contents/section0.xml`의 표/셀 구조를 분석하고 XML을 직접 수정한다.
5. 편집 결과는 최종 산출물로 `.hwpx`를 유지한다. 다시 `.hwp`로 저장하지 않는다. 최종 HWPX는 가능하면 한글에서 직접 열기 검증한다.
6. 결과 HWPX를 다시 열거나 텍스트 추출해서 주요 값이 유지되는지 검증한다.

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
