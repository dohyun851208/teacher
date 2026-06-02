# HTML 슬라이드 디자인 소스

HTML 발표자료를 만들 때 사용자가 디자인 기준을 제공하면 그 기준을 우선 적용한다.

## 지원하는 디자인 소스

- `design.md`
- 스타일 프리셋 문서. 예: `references/html-slide-apple-style.md`
- 잘 만든 기존 발표자료 PDF
- 스크린샷 이미지
- 기존 `index.html`, CSS
- 학교/기관 브랜드 가이드
- 색상, 글꼴, 레이아웃 메모

## 우선순위

1. 현재 요청의 명시 지시
2. `design.md`
3. 사용자가 지정한 스타일 프리셋 문서
4. 제공된 PDF, 이미지, 기존 HTML/CSS
5. 프로젝트의 기존 스타일과 assets
6. 기본 HTML 슬라이드 스타일

## PDF를 디자인 레퍼런스로 사용할 때

1. 대표 페이지를 이미지로 렌더링한다.
2. 비율, 제목 위치, 글자 크기, 색상, 여백, 구획선, 페이지 번호, 활동 안내 패턴을 관찰한다.
3. 텍스트와 이미지를 그대로 복사하지 말고 디자인 원칙을 추출한다.
4. 추출한 원칙을 HTML/CSS로 재구현한다.
5. 사용자가 명시적으로 요청하지 않은 비공개 텍스트는 새 자료에 옮기지 않는다.

## 통계와 외부 자료를 사용할 때

1. 가격, 성능, 벤치마크, 점유율처럼 바뀔 수 있는 정보는 웹에서 최신 자료를 확인한다.
2. 가능하면 공식 문서, 벤치마크 원문, 신뢰 가능한 비교표를 우선한다.
3. 슬라이드에는 주장보다 수치를 먼저 보이게 한다.
4. 출처는 작은 글씨로 남기되, 모델명, 지표명, 날짜를 발표자가 확인할 수 있게 적는다.
5. 여러 벤치마크가 엇갈리면 한쪽이 절대적으로 우수하다고 쓰지 않는다.
6. 예: `GPT-5.5가 항상 앞선다`보다 `Terminal-Bench 2.0에서는 GPT-5.5 82.7, Opus 4.7 69.4`처럼 범위를 한정한다.

## design.md를 사용할 때

- 색상, 글꼴, 슬라이드 유형, 컴포넌트, 모션, 금지사항을 1차 디자인 시스템으로 본다.
- 사용자 요청과 충돌하면 사용자 요청을 우선한다.
- 가독성이나 접근성을 해치면 가독성을 우선하고 조정 사실을 알린다.

## 스타일 프리셋을 사용할 때

- 공통 발표자료 원칙은 `references/workflows/html-slides.md`를 우선한다.
- 특정 스타일의 시각 언어는 별도 프리셋 문서에 둔다.
- Apple 스타일은 `references/html-slide-apple-style.md`를 따른다.
- 공통 원칙과 프리셋이 충돌하면 발표 가독성, 의미 단위 줄바꿈, 1920x1080 검증을 우선한다.

## design.md 예시 항목

```markdown
# Design System

## Format
- 16:9 widescreen
- Browser fullscreen first
- Print-to-PDF friendly

## Typography
- Title: Pretendard ExtraBold, 48-64px
- Body: Pretendard, 28-36px

## Colors
- Primary: #2563EB
- Accent: #F97316
- Background: #F8FAFC
- Text: #111827

## Slide Types
- Title
- Section divider
- Concept
- Activity instruction
- Step-by-step demo
- Reflection
```
