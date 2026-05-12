# HTML Template — My Slides

이 파일의 CSS와 JS를 생성되는 HTML에 그대로 포함한다.
슬라이드 본문(HTML)과 콘텐츠에 맞게 조합한다.

---

## 헤드 구조

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><!-- 발표 제목 --></title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        /* === 아래 CSS 전체 붙여넣기 === */
    </style>
</head>
```

---

## 전체 CSS

```css
/* === CSS CUSTOM PROPERTIES === */
:root {
    --bg: #c8d9e6;
    --card: #faf9f7;
    --dark: #1a1a1a;
    --mid: #444;
    --light: #888;
    --pink: #f0b4d4;
    --mint: #a8d4c4;
    --sage: #5a7c6a;
    --lav: #9b8dc4;
    --vio: #7c6aad;
    --font: 'Plus Jakarta Sans', sans-serif;
    --pad: clamp(2rem, 5vw, 4.5rem);
    --t1: clamp(2.4rem, 6vw, 5rem);
    --t2: clamp(1.2rem, 2.8vw, 2rem);
    --t3: clamp(1rem, 2vw, 1.4rem);
    --tb: clamp(1rem, 1.8vw, 1.45rem);
    --ts: clamp(0.8rem, 1.2vw, 1.05rem);
    --ease: cubic-bezier(0.16, 1, 0.3, 1);
}

*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
body { -webkit-user-select: none; user-select: none; }

html {
    scroll-snap-type: x mandatory;
    scroll-behavior: smooth;
    height: 100%;
    overflow-x: scroll;
    overflow-y: hidden;
}

body {
    font-family: var(--font);
    background: var(--bg);
    color: var(--dark);
    height: 100%;
    overflow: hidden;
    display: flex;
    flex-direction: row;
}

/* === SLIDE BASE === */
.slide {
    width: 100vw;
    height: 100vh;
    height: 100dvh;
    overflow: hidden;
    scroll-snap-align: start;
    display: flex;
    flex-shrink: 0;
    position: relative;
    background: var(--bg);
}

/* === CARD === */
.card {
    background: var(--card);
    border-radius: 28px;
    box-shadow: 0 15px 70px rgba(0,0,0,0.1);
    padding: var(--pad);
    flex: 1;
    margin: clamp(0.5rem, 1.2vh, 1rem);
    display: flex;
    flex-direction: column;
    justify-content: center;
    overflow: hidden;
}

/* === ANIMATION === */
.r {
    opacity: 0;
    transform: translateY(22px);
    transition: opacity 0.55s var(--ease), transform 0.55s var(--ease);
}
.slide.vis .r { opacity: 1; transform: none; }
.slide.vis .r:nth-child(1) { transition-delay: 0.05s; }
.slide.vis .r:nth-child(2) { transition-delay: 0.14s; }
.slide.vis .r:nth-child(3) { transition-delay: 0.23s; }
.slide.vis .r:nth-child(4) { transition-delay: 0.32s; }
.slide.vis .r:nth-child(5) { transition-delay: 0.41s; }
.slide.vis .r:nth-child(6) { transition-delay: 0.50s; }

/* === GLOBAL CONTROLS === */
.progress-bar {
    position: fixed; top: 0; left: 0;
    height: 3px; background: var(--vio);
    transition: width 0.35s ease; z-index: 2000;
}

.nav-dots {
    position: fixed; bottom: 14px; left: 50%;
    transform: translateX(-50%);
    display: flex; flex-direction: row; gap: 7px; z-index: 500;
}

.dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: rgba(0,0,0,0.18); cursor: pointer;
    transition: all 0.3s;
}
.dot.active { background: var(--vio); transform: scale(1.5); }

.slide-num { display: none; }

/* === INLINE EDIT (검은 점 토글) === */
.edit-toggle {
    position: fixed; top: 30px; right: 30px;
    width: 10px; height: 10px; border-radius: 50%;
    background: #000; cursor: pointer; z-index: 5000;
    transition: all 0.2s; border: none;
}
.edit-toggle.editing {
    background: var(--vio); transform: scale(1.4);
    box-shadow: 0 0 0 3px rgba(124,106,173,0.25);
}
body.editing [data-edit] {
    outline: 1.5px dashed rgba(124,106,173,0.4);
    outline-offset: 3px; cursor: text; border-radius: 4px;
}
body.editing [data-edit]:focus {
    outline: 2px solid var(--vio);
    background: rgba(124,106,173,0.06);
}

/* === TYPOGRAPHY HELPERS === */
.tag {
    display: inline-block;
    background: var(--mint); color: var(--dark);
    font-size: var(--ts); font-weight: 700;
    padding: 4px 13px; border-radius: 20px;
    margin-bottom: clamp(0.5rem, 1.2vh, 0.9rem);
}

.t-main {
    font-size: var(--t1); font-weight: 800;
    line-height: 1.2; color: var(--dark);
    margin-bottom: clamp(0.4rem, 1vh, 0.8rem);
}
.t-main em { color: var(--vio); font-style: normal; }

.t-sub {
    font-size: var(--t2); font-weight: 500;
    color: var(--mid);
    margin-bottom: clamp(1rem, 3vh, 2rem);
}

.sec-label {
    font-size: var(--ts); font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: var(--sage); margin-bottom: 5px;
}

.sec-title {
    font-size: clamp(1.3rem, 3vw, 2.2rem); font-weight: 800;
    color: var(--dark); line-height: 1.3;
    margin-bottom: clamp(0.6rem, 1.5vh, 1.1rem);
}
.sec-title em { color: var(--vio); font-style: normal; }

.hr { width: 38px; height: 3px; background: var(--vio); border-radius: 2px; margin-bottom: clamp(0.7rem, 1.5vh, 1.1rem); }

/* === LAYOUT HELPERS === */
.two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: clamp(0.8rem, 1.5vw, 1.3rem);
    flex: 1; min-height: 0;
}

.three-col {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: clamp(0.6rem, 1.2vw, 1rem);
}

.col { display: flex; flex-direction: column; gap: clamp(0.5rem, 1vh, 0.9rem); min-height: 0; overflow: hidden; }

/* === COMPONENT: stats row === */
.stats { display: flex; gap: clamp(0.7rem, 1.5vw, 1.2rem); flex-wrap: wrap; }
.stat {
    background: var(--bg); border-radius: 12px;
    padding: 10px 16px; text-align: center; flex: 1; min-width: 80px;
}
.stat-n { font-size: clamp(1.3rem, 2.5vw, 1.9rem); font-weight: 800; color: var(--vio); }
.stat-l { font-size: var(--ts); color: var(--mid); font-weight: 500; }

/* === BIG STAT === */
.big-stat { font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 800; color: var(--vio); }

/* === COMPONENT: info chip === */
.chip {
    background: var(--bg); border-radius: 11px;
    padding: clamp(0.5rem, 1vh, 0.8rem) clamp(0.7rem, 1.2vw, 1rem);
}
.chip-l { font-size: var(--ts); font-weight: 700; color: var(--light); margin-bottom: 3px; }
.chip-v { font-size: clamp(0.8rem, 1.4vw, 1rem); font-weight: 700; color: var(--dark); }
.chip-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }

/* === COMPONENT: highlight box === */
.hl {
    background: linear-gradient(135deg, var(--lav), var(--vio));
    color: #fff; border-radius: 14px;
    padding: clamp(0.7rem, 1.3vh, 1rem) clamp(0.8rem, 1.4vw, 1.1rem);
    flex-shrink: 0;
}
.hl-l { font-size: var(--ts); opacity: 0.85; margin-bottom: 4px; }
.hl-v { font-size: var(--tb); font-weight: 700; line-height: 1.45; }

/* === COMPONENT: bullet list === */
.blist { list-style: none; display: flex; flex-direction: column; gap: clamp(0.5rem, 1vh, 0.8rem); overflow: hidden; }
.blist li {
    display: flex; align-items: flex-start; gap: 8px;
    font-size: var(--tb); line-height: 1.65; color: var(--mid);
}
.blist li::before {
    content: '';
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--vio); margin-top: 0.42em; flex-shrink: 0;
}

/* === COMPONENT: platform card (horizontal) === */
.pcard {
    background: var(--bg); border-radius: 12px;
    padding: clamp(0.8rem, 1.4vh, 1.1rem) clamp(0.9rem, 1.4vw, 1.2rem);
    display: flex; flex-direction: column; gap: 4px;
}
.pcard-row { flex-direction: row; align-items: center; gap: 12px; }
.pcard-region { font-size: var(--ts); font-weight: 600; color: var(--light); }
.pcard-name { font-size: var(--tb); font-weight: 800; color: var(--dark); }
.pcard-desc { font-size: var(--ts); color: var(--mid); line-height: 1.5; }

/* === COMPONENT: badge === */
.badge {
    display: inline-block; padding: 3px 10px;
    border-radius: 20px; font-size: var(--ts); font-weight: 600;
}
.b-mint  { background: var(--mint); color: var(--dark); }
.b-pink  { background: var(--pink); color: var(--dark); }
.b-lav   { background: var(--lav);  color: #fff; }
.b-vio   { background: var(--vio);  color: #fff; }
.b-sage  { background: var(--sage); color: #fff; }

/* === COMPONENT: group box === */
.grp { border-radius: 13px; padding: clamp(0.7rem, 1.2vh, 1rem); }
.grp-mint  { background: #e8f5f0; }
.grp-vio   { background: #f0edf8; }
.grp-title { font-size: var(--tb); font-weight: 700; margin-bottom: 9px; }
.grp-mint .grp-title  { color: #2d7a5a; }
.grp-vio  .grp-title  { color: #5a3d9a; }
.grp-desc  { font-size: var(--tb); line-height: 1.65; margin-top: 7px; }
.grp-mint .grp-desc   { color: #2d7a5a; }
.grp-vio  .grp-desc   { color: #5a3d9a; }
.badge-row { display: flex; flex-wrap: wrap; gap: 5px; }

/* === COMPONENT: tooltip === */
.tooltip {
    background: var(--card); border-radius: 12px;
    padding: 11px 14px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    font-size: var(--ts); min-height: 78px; transition: all 0.25s;
}
.tt-name { font-weight: 800; font-size: var(--t3); color: var(--dark); margin-bottom: 3px; }
.tt-plat { font-weight: 600; margin-bottom: 3px; }
.tt-desc { color: var(--mid); line-height: 1.55; }

/* === BIG STATS DISPLAY === */
.big-stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: clamp(0.8rem, 1.5vw, 1.4rem);
    margin-bottom: clamp(0.8rem, 1.5vh, 1.2rem);
}
.big-stat-box {
    background: var(--bg); border-radius: 16px;
    padding: clamp(1rem, 2vh, 1.6rem) clamp(0.8rem, 1.5vw, 1.2rem);
    text-align: center;
}
.big-stat-n { font-size: clamp(1.8rem, 4vw, 3rem); font-weight: 800; color: var(--vio); line-height: 1.1; }
.big-stat-l { font-size: var(--ts); color: var(--mid); font-weight: 500; margin-top: 4px; }

/* === 4-STAT GRID === */
.four-stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: clamp(0.6rem, 1.2vw, 1rem);
    margin-bottom: clamp(0.8rem, 1.5vh, 1.2rem);
}

/* === MODULE CARDS === */
.module-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: clamp(0.5rem, 1vw, 0.85rem);
    flex: 1; min-height: 0;
}
.module-card {
    background: var(--bg); border-radius: 12px;
    padding: clamp(0.6rem, 1.1vh, 0.9rem) clamp(0.7rem, 1.1vw, 1rem);
    display: flex; flex-direction: column; gap: 3px;
}
.module-name { font-size: var(--tb); font-weight: 800; color: var(--dark); }
.module-desc { font-size: var(--ts); color: var(--mid); line-height: 1.45; }

/* === COMPARE TABLE === */
.ctable { width: 100%; border-collapse: collapse; font-size: var(--ts); }
.ctable th { background: var(--bg); padding: 7px 10px; text-align: left; font-weight: 700; }
.ctable td { padding: 6px 10px; border-bottom: 1px solid rgba(0,0,0,0.05); color: var(--mid); }
.ctable tr:last-child td { border-bottom: none; }

/* === FLOW DIAGRAM === */
.flow-row {
    display: flex; align-items: stretch;
    gap: clamp(1.5rem, 3vw, 2.5rem);
    flex: 1; min-height: 0; margin-top: 1rem;
}
.flow-node {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center; background: var(--bg);
    border-radius: 20px;
    padding: clamp(1.5rem, 3.5vh, 2.5rem) clamp(1.2rem, 3vw, 2.2rem);
    flex: 1 1 0; min-width: 0; gap: 0.6rem; position: relative;
}
.flow-all  { border: 2px solid rgba(0,0,0,0.1); }
.flow-aiep { border: 2px solid var(--mint); }
.flow-indep { border: 2px solid var(--vio); background: linear-gradient(135deg, rgba(124,106,173,0.08), rgba(240,180,212,0.12)); }
.flow-num {
    font-size: clamp(2.5rem, 6vw, 5rem); font-weight: 800; line-height: 1; color: var(--dark);
}
.flow-all .flow-num {
    background: linear-gradient(135deg, #666, #aaa);
    -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
}
.flow-aiep .flow-num {
    background: linear-gradient(135deg, var(--sage), var(--mint));
    -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
}
.flow-indep .flow-num {
    background: linear-gradient(135deg, var(--vio), var(--lav));
    -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
}
.flow-title { font-size: var(--t3); font-weight: 700; color: var(--dark); }
.flow-names { font-size: var(--tb); color: var(--mid); line-height: 1.6; }
.flow-arrow { font-size: clamp(1.2rem, 3vw, 2rem); color: var(--vio); opacity: 0.4; flex-shrink: 0; font-weight: 300; align-self: center; }
.flow-focus-badge {
    position: absolute; top: -12px; left: 50%; transform: translateX(-50%);
    background: var(--vio); color: #fff;
    font-size: 0.58rem; font-weight: 700;
    padding: 3px 10px; border-radius: 20px; white-space: nowrap;
}

/* === INSIGHT CARDS (이미지+설명) === */
.insight-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: clamp(0.7rem, 1.5vw, 1.2rem);
    flex: 1; min-height: 0;
}
.insight-card {
    background: #fff; border-radius: 20px; padding: 0;
    display: flex; flex-direction: column;
    box-shadow: 0 4px 15px rgba(0,0,0,0.04);
    border: 1px solid rgba(0,0,0,0.06);
    transition: transform 0.3s var(--ease), box-shadow 0.3s var(--ease);
    overflow: hidden;
}
.insight-card:hover { transform: translateY(-8px); box-shadow: 0 15px 45px rgba(0,0,0,0.12); }
.insight-icon {
    width: 100%; height: clamp(250px, 50vh, 480px);
    display: flex; align-items: center; justify-content: center;
    overflow: hidden; background: #fff;
}
.insight-icon img {
    width: 100%; height: 100%; object-fit: contain; padding: 10px;
    transition: transform 0.6s var(--ease);
}
.insight-card:hover .insight-icon img { transform: scale(1.06); }
.insight-kw {
    font-size: clamp(0.9rem, 1.7vw, 1.1rem); font-weight: 800; color: var(--dark);
    line-height: 1.25; padding: 1.2rem 1.4rem 0.3rem;
    display: flex; align-items: center; gap: 6px;
}
.insight-desc {
    font-size: var(--ts); color: #555; line-height: 1.5;
    padding: 0 1.4rem 1.4rem; flex: 1;
}

/* === PLATFORM BADGE === */
.platform-badge {
    display: inline-flex; align-items: center; gap: 6px;
    color: #fff; font-size: var(--ts); font-weight: 700;
    padding: 4px 14px; border-radius: 20px;
    margin-bottom: clamp(0.4rem, 0.8vh, 0.7rem); width: fit-content;
}
/* 색상은 필요에 따라 추가 — 예시: */
/* .pb-primary { background: #7c3aed; } */

/* === PREVIEW BUTTON + MODAL === */
.preview-btn {
    display: inline-flex; align-items: center; justify-content: center;
    background: rgba(0,0,0,0.07); border: none; border-radius: 50%;
    width: 28px; height: 28px; cursor: pointer;
    font-size: 0.8rem; line-height: 1;
    transition: all 0.25s var(--ease); flex-shrink: 0;
}
.preview-btn:hover { background: rgba(0,0,0,0.14); transform: scale(1.15); }
.preview-btn::before { content: '🔍'; }

.img-modal-overlay {
    position: fixed; inset: 0; z-index: 9000;
    background: rgba(0,0,0,0.7); backdrop-filter: blur(6px);
    display: flex; align-items: center; justify-content: center;
    opacity: 0; pointer-events: none; transition: opacity 0.3s var(--ease);
}
.img-modal-overlay.open { opacity: 1; pointer-events: auto; }
.img-modal-overlay.open .img-modal-content,
.img-modal-overlay.open .indep-modal-inner { transform: scale(1); opacity: 1; }
.img-modal-content {
    max-width: 90vw; max-height: 85vh;
    border-radius: 16px; overflow: hidden;
    box-shadow: 0 25px 80px rgba(0,0,0,0.4);
    transform: scale(0.85); opacity: 0;
    transition: transform 0.35s var(--ease), opacity 0.35s var(--ease);
}
.img-modal-content img { width: 100%; height: 100%; object-fit: contain; display: block; }

/* === INDEP DETAIL MODAL === */
.indep-modal-inner {
    display: flex; gap: clamp(1.5rem, 3vw, 2.5rem);
    align-items: center; max-width: 90vw; max-height: 85vh;
    transform: scale(0.85); opacity: 0;
    transition: transform 0.35s var(--ease), opacity 0.35s var(--ease);
}
.indep-modal-info {
    flex: 0 0 240px; color: #fff;
    display: flex; flex-direction: column; gap: 0.6rem;
}
.indep-modal-region { font-size: var(--t1); font-weight: 800; }
.indep-modal-plat { font-size: var(--t3); font-weight: 600; opacity: 0.85; }
.indep-modal-kw {
    display: inline-block; background: rgba(255,255,255,0.2);
    padding: 4px 12px; border-radius: 20px;
    font-size: var(--ts); font-weight: 700; width: fit-content;
}
.indep-modal-desc { font-size: var(--tb); line-height: 1.6; opacity: 0.9; }
.indep-modal-img {
    flex: 1; max-height: 80vh;
    border-radius: 16px; overflow: hidden;
    box-shadow: 0 25px 80px rgba(0,0,0,0.4);
}
.indep-modal-img img { width: 100%; height: 100%; object-fit: contain; display: block; background: #fff; }

/* === INTERACTIVE FEATURE EXPLORER === */
.feat-tabs {
    display: flex; gap: 6px; flex-wrap: wrap;
    margin-bottom: clamp(0.7rem, 1.3vh, 1rem);
}
.feat-tab {
    padding: 7px 14px; border-radius: 20px; border: 2px solid transparent;
    font: 600 var(--ts) var(--font); cursor: pointer;
    background: var(--bg); color: var(--mid);
    transition: all 0.25s var(--ease);
}
.feat-tab:hover { transform: translateY(-1px); box-shadow: 0 3px 10px rgba(0,0,0,0.1); }
/* 탭 활성 색상은 콘텐츠에 맞게 추가: .tab-[id].active { background: ...; } */

.feat-panel { display: none; flex: 1; min-height: 0; overflow: hidden; }
.feat-panel.active { display: flex; flex-direction: column; gap: clamp(0.5rem, 1vh, 0.8rem); }

.feat-grid {
    display: grid; grid-template-columns: repeat(5, 1fr);
    gap: clamp(0.5rem, 1vw, 0.9rem); flex: 1; min-height: 0;
}
.feat-card {
    background: var(--bg); border-radius: 14px;
    padding: clamp(0.7rem, 1.2vh, 1rem) clamp(0.6rem, 1vw, 0.9rem);
    display: flex; flex-direction: column; gap: 6px;
    border-top: 3px solid transparent;
    transition: transform 0.2s var(--ease), box-shadow 0.2s;
    animation: cardIn 0.35s var(--ease) both;
}
.feat-card:nth-child(1) { animation-delay: 0.03s; }
.feat-card:nth-child(2) { animation-delay: 0.08s; }
.feat-card:nth-child(3) { animation-delay: 0.13s; }
.feat-card:nth-child(4) { animation-delay: 0.18s; }
.feat-card:nth-child(5) { animation-delay: 0.23s; }
@keyframes cardIn { from { opacity:0; transform:translateY(16px); } to { opacity:1; transform:none; } }
.feat-card:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.1); }
.feat-icon { font-size: clamp(1.3rem, 2.5vh, 1.8rem); }
.feat-name { font-size: var(--ts); font-weight: 800; color: var(--dark); line-height: 1.3; }
.feat-desc { font-size: clamp(0.58rem, 0.9vw, 0.72rem); color: var(--mid); line-height: 1.5; flex: 1; }
.feat-tag  { font-size: clamp(0.52rem, 0.8vw, 0.65rem); font-weight: 700; padding: 2px 8px; border-radius: 10px; align-self: flex-start; }

.c-vio  { border-color: var(--vio); }  .c-vio  .feat-tag { background: var(--vio); color:#fff; }
.c-lav  { border-color: var(--lav); }  .c-lav  .feat-tag { background: var(--lav); color:#fff; }
.c-mint { border-color: var(--sage); } .c-mint .feat-tag { background: var(--mint); color:var(--dark); }
.c-pink { border-color: #d06; }        .c-pink .feat-tag { background: var(--pink); color:var(--dark); }
.c-sage { border-color: var(--sage); } .c-sage .feat-tag { background: var(--sage); color:#fff; }

/* === AIEP CHIPS === */
.aiep-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 1rem; }
.aiep-chip {
    background: var(--mint); border-radius: 10px;
    padding: 6px 14px; font-size: var(--ts); font-weight: 700; color: var(--dark);
}

/* === REGION GRID MAP === */
.rect-map { display: flex; gap: clamp(0.8rem, 1.5vw, 1.3rem); flex: 1.5; min-height: 0; overflow: hidden; align-items: stretch; }
.rect-group { display: flex; flex-direction: column; gap: 7px; }
.rg-label {
    font-size: var(--ts); font-weight: 700; text-align: center;
    padding: 5px 10px; border-radius: 8px; flex-shrink: 0;
}
.rg-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px; }
.rg-box {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    border-radius: 9px; cursor: pointer;
    font-size: var(--ts); font-weight: 700;
    padding: 5px 3px; text-align: center;
    transition: filter 0.18s, transform 0.15s; line-height: 1.25;
}
.rg-box:hover { filter: brightness(0.88); transform: scale(0.96); }
.aiep-box { background: #a8d4c4; color: #1a4030; }
.indep-box {
    background: #fff; border: 1px solid rgba(0,0,0,0.02);
    border-radius: 20px;
    padding: clamp(1.2rem, 2.5vh, 1.8rem) clamp(1rem, 2vw, 1.5rem);
    box-shadow: 0 10px 30px rgba(0,0,0,0.03);
    transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    position: relative; cursor: pointer;
}
.indep-box::before {
    content: ''; position: absolute; top: 20px; right: 20px;
    width: 8px; height: 8px; border-radius: 50%;
    background: #cbd5e1; transition: transform 0.3s, background 0.3s;
}
.indep-box:hover { transform: translateY(-8px); box-shadow: 0 25px 60px rgba(0,0,0,0.08); border-color: rgba(0,0,0,0.05); }
.indep-box:hover::before { transform: scale(1.5); }
.indep-box .rg-plat { font-size: 0.72em; font-weight: 600; color: #94a3b8; margin-top: 6px; letter-spacing: -0.02em; }

/* === MYSTERY REVEAL === */
.mystery-q {
    cursor: pointer; color: var(--vio);
    filter: blur(4px); opacity: 0.5;
    transition: all 0.5s var(--ease);
}
.mystery-q:hover { filter: blur(2px); opacity: 0.7; }
.mystery-revealed .mystery-q { filter: blur(0); opacity: 1; }

/* === ISC CARDS (showcase grid) === */
.indep-showcase {
    display: grid; grid-template-columns: repeat(5, 1fr);
    gap: clamp(1rem, 2vw, 1.8rem); flex: 1; min-height: 0;
}
.isc-card {
    background: var(--bg); border-radius: 16px;
    padding: clamp(0.6rem, 1.5vh, 1.1rem) clamp(0.5rem, 1vw, 0.8rem);
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center; gap: 0.3rem; transition: transform 0.2s;
}
.isc-card:hover { transform: translateY(-3px); }
.isc-region { font-size: var(--ts); font-weight: 700; letter-spacing: 0.05em; }
.isc-name { font-size: clamp(0.85rem, 1.6vw, 1.1rem); font-weight: 800; color: var(--dark); line-height: 1.2; }
.isc-kw { font-size: 0.65rem; color: var(--mid); background: rgba(0,0,0,0.05); border-radius: 8px; padding: 2px 6px; font-weight: 600; }
.isc-desc { font-size: 0.65rem; color: var(--mid); line-height: 1.4; margin-top: 4px; }

/* === RESPONSIVE === */
@media (max-height: 680px) {
    :root { --pad: clamp(0.6rem, 2vw, 1.4rem); --t1: clamp(1.2rem,3vw,1.9rem); --t2: clamp(0.95rem,2vw,1.4rem); }
}
@media (max-width: 600px) {
    .two-col, .three-col, .module-grid, .insight-grid, .feat-grid { grid-template-columns: 1fr; }
    .big-stats-grid, .four-stat-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.15ms !important; }
    html { scroll-behavior: auto; }
}
```

---

## Body 구조

```html
<body>

<canvas id="drawCanvas"></canvas>
<button class="edit-toggle" id="editDot" aria-label="편집 모드"></button>
<div class="progress-bar" id="pb"></div>
<nav class="nav-dots" id="nd"></nav>

<!-- ==============================
     SLIDE 01 · 타이틀
============================== -->
<section class="slide" id="s1">
    <div class="card">
        <div class="tag r">발표 카테고리</div>
        <h1 class="t-main r">제목 <em>강조 부분</em></h1>
        <p class="t-sub r">부제목 — 한 줄 설명</p>
        <div class="hr r"></div>
        <div style="position:absolute; bottom:clamp(1rem,2.5vh,2rem); right:clamp(1rem,3vw,2.5rem); font-size:clamp(0.75rem,1.3vw,1rem); font-weight:600; color:var(--light);">발표자 정보</div>
    </div>
</section>

<!-- ==============================
     SLIDE 02 · 콘텐츠 예시
============================== -->
<section class="slide" id="s2">
    <div class="card">
        <div class="sec-label r">섹션 라벨</div>
        <h2 class="sec-title r">슬라이드 제목 <em>포인트</em></h2>
        <div class="hr r"></div>
        <!-- 내용 컴포넌트 조합 -->
    </div>
</section>

<!-- 이미지 모달 예시 -->
<div class="img-modal-overlay" id="exModal" onclick="this.classList.remove('open')">
    <div class="img-modal-content">
        <img src="images/example.png" alt="예시">
    </div>
</div>

<!-- 슬라이드별 테마 오버라이드 (선택사항) -->
<!-- <style>
#s3 { background: linear-gradient(135deg, #색1, #색2); }
#s3 .hr { background: #포인트색; }
#s3 .hl { background: linear-gradient(135deg, #색1, #색2); }
#s3 .sec-title em { color: #포인트색; }
</style> -->

</body>
```

---

## 전체 JS

```javascript
<script>
    /* === CONTROLLER === */
    const slides = Array.from(document.querySelectorAll('.slide'));
    const TOTAL = slides.length;
    const pb = document.getElementById('pb');
    const nd = document.getElementById('nd');
    let cur = 0;

    /* Build nav dots */
    slides.forEach((_, i) => {
        const d = document.createElement('div');
        d.className = 'dot' + (i === 0 ? ' active' : '');
        d.onclick = () => go(i);
        nd.appendChild(d);
    });

    /* Count-up animation */
    function countUp(el, target, duration) {
        const start = performance.now();
        const step = (now) => {
            const t = Math.min((now - start) / duration, 1);
            const ease = 1 - Math.pow(1 - t, 3);
            el.textContent = Math.round(target * ease);
            if (t < 1) requestAnimationFrame(step);
            else el.textContent = target;
        };
        el.textContent = '0';
        requestAnimationFrame(step);
    }

    let lastAnimatedSlide = -1;
    function animateNumbers(slide) {
        const idx = slides.indexOf(slide);
        if (idx === lastAnimatedSlide) return;
        lastAnimatedSlide = idx;
        setTimeout(() => {
            slide.querySelectorAll('.flow-num').forEach(el => {
                if (el.querySelector('.count-target')) return;
                const raw = el.dataset.original || el.textContent.trim();
                el.dataset.original = raw;
                if (/^\d+$/.test(raw)) countUp(el, parseInt(raw), 1800);
            });
            slide.querySelectorAll('.count-target').forEach(el => {
                countUp(el, parseInt(el.dataset.count), 1800);
            });
        }, 400);
    }

    function updateUI() {
        slides.forEach((s, i) => s.classList.toggle('vis', i === cur));
        document.querySelectorAll('.dot').forEach((d, i) => d.classList.toggle('active', i === cur));
        pb.style.width = ((cur + 1) / TOTAL * 100) + '%';
        animateNumbers(slides[cur]);
    }

    function go(idx) {
        if (idx < 0) idx = 0;
        if (idx >= TOTAL) idx = TOTAL - 1;
        cur = idx;
        clearCanvas();
        slides[cur].scrollIntoView({ behavior: 'smooth' });
        updateUI();
    }

    /* Keyboard */
    document.addEventListener('keydown', e => {
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') { e.preventDefault(); go(cur + 1); }
        if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')                     { e.preventDefault(); go(cur - 1); }
        if (e.key === 'Home') { e.preventDefault(); go(0); }
        if (e.key === 'End')  { e.preventDefault(); go(TOTAL - 1); }
        if (e.key === 'Escape') {
            document.querySelectorAll('.img-modal-overlay.open').forEach(m => m.classList.remove('open'));
            clearCanvas();
        }
    });

    /* Touch */
    let tx = 0, ty = 0;
    document.addEventListener('touchstart', e => { tx = e.touches[0].clientX; ty = e.touches[0].clientY; }, { passive: true });
    document.addEventListener('touchend', e => {
        const dx = e.changedTouches[0].clientX - tx;
        const dy = e.changedTouches[0].clientY - ty;
        if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 40) go(dx < 0 ? cur + 1 : cur - 1);
    });

    /* Wheel */
    let wt = 0;
    document.addEventListener('wheel', e => {
        const now = Date.now();
        if (now - wt < 600) return;
        wt = now;
        go(e.deltaY > 0 ? cur + 1 : cur - 1);
    }, { passive: true });

    /* Intersection Observer */
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const idx = slides.indexOf(entry.target);
                if (idx !== cur) { cur = idx; updateUI(); }
            }
        });
    }, { threshold: 0.55 });
    slides.forEach(s => observer.observe(s));

    /* === HIGHLIGHTER DRAWING === */
    const canvas = document.getElementById('drawCanvas');
    const ctx = canvas.getContext('2d');
    let drawing = false, hasMoved = false, startX, startY;
    let fadeTimer = null;

    function resizeCanvas() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    canvas.style.cssText = 'position:fixed;inset:0;z-index:10000;pointer-events:none;';

    function clearCanvas() {
        if (fadeTimer) clearTimeout(fadeTimer);
        canvas.style.transition = 'opacity 0.4s';
        canvas.style.opacity = '0';
        setTimeout(() => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            canvas.style.transition = '';
            canvas.style.opacity = '1';
        }, 400);
    }

    document.addEventListener('mousedown', e => {
        if (e.button !== 0) return;
        drawing = true; hasMoved = false;
        startX = e.clientX; startY = e.clientY;
    });

    document.addEventListener('mousemove', e => {
        if (!drawing) return;
        const dx = e.clientX - startX, dy = e.clientY - startY;
        if (!hasMoved && Math.abs(dx) + Math.abs(dy) < 6) return;
        if (!hasMoved) {
            hasMoved = true;
            if (fadeTimer) clearTimeout(fadeTimer);
            canvas.style.pointerEvents = 'auto';
            ctx.beginPath();
            ctx.moveTo(startX, startY);
            ctx.lineWidth = 20; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
            ctx.strokeStyle = 'rgba(240,180,60,0.3)';
            ctx.globalCompositeOperation = 'source-over';
        }
        ctx.lineTo(e.clientX, e.clientY);
        ctx.stroke();
    });

    document.addEventListener('mouseup', () => {
        if (hasMoved) {
            canvas.style.pointerEvents = 'none';
            fadeTimer = setTimeout(clearCanvas, 3000);
        }
        drawing = false; hasMoved = false;
    });

    /* === INTERACTIVE FEATURE EXPLORER === */
    function showFeat(id) {
        document.querySelectorAll('.feat-panel').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.feat-tab').forEach(t => t.classList.remove('active'));
        const panel = document.getElementById('feat-' + id);
        if (panel) panel.classList.add('active');
        document.querySelector('.tab-' + id)?.classList.add('active');
    }

    /* === 상세 모달 (data 속성 기반) === */
    function openDetailModal(el) {
        document.getElementById('imRegion').textContent = el.dataset.n;
        document.getElementById('imPlat').textContent = el.dataset.p;
        document.getElementById('imKw').textContent = el.dataset.kw;
        document.getElementById('imDesc').textContent = el.dataset.desc;
        document.getElementById('imImg').src = el.dataset.img;
        document.getElementById('detailModal').classList.add('open');
    }

    /* === MYSTERY REVEAL (선택사항) === */
    let mysteryRevealed = false;
    function revealMystery() {
        mysteryRevealed = !mysteryRevealed;
        document.getElementById('s-mystery')?.classList.toggle('mystery-revealed', mysteryRevealed);
    }

    /* === INLINE EDIT (검은 점 토글) — 고유 ID 기반 localStorage === */
    const editBtn = document.getElementById('editDot');
    const EDIT_KEY = 'slides_edits_v1';
    const editables = document.querySelectorAll('[data-edit]');

    /* 각 editable 요소에 안정된 ID 부여: 사용자 지정 값 > 자동생성(slideId-eN) */
    editables.forEach(el => {
        const v = el.getAttribute('data-edit');
        if (v && v !== '') { el.dataset.editId = v; return; }
        const slide = el.closest('.slide');
        const slideId = slide ? slide.id : 'g';
        const siblings = slide ? slide.querySelectorAll('[data-edit]') : [];
        let pos = 0;
        for (const s of siblings) { if (s === el) break; pos++; }
        el.dataset.editId = slideId + '-e' + pos;
    });

    function loadEdits() {
        try {
            const raw = localStorage.getItem(EDIT_KEY);
            if (!raw) return;
            const data = JSON.parse(raw);
            editables.forEach(el => {
                const id = el.dataset.editId;
                if (data[id] !== undefined) el.innerHTML = data[id];
            });
        } catch(e) {}
    }
    function saveEdits() {
        const data = {};
        editables.forEach(el => { data[el.dataset.editId] = el.innerHTML; });
        try { localStorage.setItem(EDIT_KEY, JSON.stringify(data)); } catch(e) {}
    }

    editBtn?.addEventListener('click', () => {
        const isEditing = document.body.classList.toggle('editing');
        editBtn.classList.toggle('editing', isEditing);
        editables.forEach(el => { el.contentEditable = isEditing ? 'true' : 'false'; });
        if (!isEditing) saveEdits();
    });

    loadEdits();

    /* Init */
    updateUI();
</script>
```

---

## 추가 CSS — 놓치면 안 되는 컴포넌트

```css
/* === MAP SLIDE 레이아웃 === */
.map-wrap {
    display: flex; gap: clamp(0.8rem, 1.5vw, 1.3rem);
    align-items: center; flex: 1; min-height: 0; overflow: hidden;
}
.map-svg-wrap { display: none; }
.map-panel { flex: 1; display: flex; flex-direction: column; gap: 0.7rem; min-height: 0; overflow: hidden; }
.legend { display: flex; flex-direction: column; gap: 5px; }
.leg-item { display: flex; align-items: center; gap: 8px; font-size: var(--ts); font-weight: 500; }
.leg-dot { width: 13px; height: 13px; border-radius: 4px; flex-shrink: 0; }

/* === RECT MAP 추가 클래스 === */
.region { cursor: pointer; font-family: var(--font); font-weight: 800; font-size: 1.15rem; }
.rect-group.rg-aiep  { flex: 1.8; }
.rect-group.rg-indep { flex: 1; }
.aiep-bg   { background: #a8d4c4; color: #1a4030; }
.indep-bg  { background: var(--vio); color: #fff; }
.rg-indep-grid { grid-template-columns: repeat(3, 1fr); gap: clamp(0.5rem, 1vw, 0.8rem); }

/* 지역별 indep-box 색상 (필요에 따라 추가) */
/* .rg-[지역]::before { background: #색상; }
   .rg-[지역].region { color: #색상; }
   .rg-[지역]:hover { box-shadow: 0 25px 60px rgba(r,g,b,0.1); } */

/* === UNCLEAR BOX === */
.rg-unclear {
    background: rgba(0,0,0,0.04); color: var(--light); font-size: var(--ts);
    font-weight: 600; text-align: center; padding: 10px 5px;
    border-radius: 14px; cursor: pointer; transition: all 0.2s; margin-top: 5px;
}
.rg-unclear:hover { background: rgba(0,0,0,0.07); }

/* === MYSTERY REVEAL 전체 === */
.mystery-num { font-size: inherit; }
.mystery-box { transition: all 0.6s var(--ease); }
.mystery-box .rg-plat { font-size: 0.72em; font-weight: 500; margin-top: 2px; transition: all 0.6s var(--ease); }

/* reveal 시 mystery-box 강조 (예: 대구 방식) */
.mystery-revealed .mystery-box {
    background: rgba(200,60,60,0.12) !important; color: #c0392b !important;
    box-shadow: 0 0 24px rgba(200,60,60,0.2);
    animation: mysteryShake 0.5s var(--ease);
}
.mystery-revealed .mystery-box .rg-plat { color: #c0392b; opacity: 1; }
@keyframes mysteryShake {
    0%, 100% { transform: translateX(0); }
    20% { transform: translateX(-6px); }
    40% { transform: translateX(6px); }
    60% { transform: translateX(-4px); }
    80% { transform: translateX(4px); }
}

/* === ISC-REGION 커스텀 색상 === */
/* .isc-card { --c: #색상; } → .isc-region { color: var(--c, var(--vio)); } */

/* === RESPONSIVE: map-wrap 모바일 === */
@media (max-width: 600px) {
    .map-wrap { flex-direction: column; }
    .map-svg-wrap { width: 100%; max-height: 35vh; }
}
```

---

## 추가 안전장치 — viewport / 접근성 (보강)

기존 `## 전체 CSS` 블록의 RESPONSIVE 섹션(line 598~609)에 이미 `@media (max-height: 680px)`, `(max-width: 600px)`, `prefers-reduced-motion` 기본판이 있다. 아래는 frontend-slides의 `viewport-base.css`에서 가져온 **보강분만** — 더 세밀한 viewport 단계와 카드 max-size 안전장치. 기존 RESPONSIVE 섹션 바로 뒤에 추가한다.

```css
/* === SHORT VIEWPORT 세부 단계 (600px / 500px) — 기존 680px 보강 === */
@media (max-height: 600px) {
    :root {
        --pad: clamp(0.5rem, 1.8vw, 1.2rem);
        --t1: clamp(1rem, 2.6vw, 1.6rem);
        --tb: clamp(0.8rem, 1.4vw, 1.05rem);
    }
    /* 짧은 화면에서 장식 요소 숨김 */
    .nav-dots, .progress-bar { display: none; }
}

@media (max-height: 500px) {
    :root {
        --pad: clamp(0.4rem, 1.5vw, 1rem);
        --t1: clamp(0.9rem, 2.2vw, 1.3rem);
        --tb: clamp(0.7rem, 1.2vw, 0.95rem);
    }
}

/* === CARD 최대 크기 안전장치 === */
/* 4K·울트라와이드 모니터 전체화면에서 카드가 무한정 커지는 것 방지 */
.card {
    max-width: min(96vw, 1600px);
    max-height: min(96vh, 1000px);
    margin-inline: auto;
}
```

### 적용 가이드

- `prefers-reduced-motion`은 기존 line 606에 이미 있으므로 중복 추가하지 않는다.
- 600px / 500px 단계는 태블릿 가로·랩탑 도킹 환경에서 글자가 카드 밖으로 흘러넘치는 문제 예방용.
- 카드 max-size는 27인치+ 모니터 풀스크린 발표에서 카드가 어색하게 커지지 않게 잡아준다.

추가 애니메이션 패턴은 [animation-patterns.md](animation-patterns.md) 참조 (분위기별 진입 효과, 배경 효과, Tilt 인터랙션, Troubleshooting).

---

## JS 개선사항 — 두 파일 비교에서 발견

```javascript
// 1. canvas z-index: 모달(9000)보다 낮게 4000으로 설정
canvas.style.cssText = 'position:fixed;inset:0;z-index:4000;pointer-events:none;';

// 2. 모달 열려있을 때 그리기 차단 (mousedown에 추가)
document.addEventListener('mousedown', e => {
    if (e.button !== 0) return;
    if (document.querySelector('.img-modal-overlay.open')) return; // ← 이 줄 추가
    drawing = true;
    // ...
});

// 3. ESC 키: 모달 닫기 + 캔버스 초기화 (index.html 방식)
document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.img-modal-overlay.open').forEach(m => m.classList.remove('open'));
        clearCanvas(); // ← 추가 (ai-edu-platform.html에는 없지만 index.html에 있음)
    }
});
```

---

## 슬라이드 타입 예시

### 타이틀 슬라이드
```html
<section class="slide" id="s1">
    <div class="card">
        <div class="tag r">카테고리</div>
        <h1 class="t-main r">제목 <em>강조</em></h1>
        <p class="t-sub r">부제목</p>
        <div class="hr r"></div>
    </div>
</section>
```

### 통계 슬라이드
```html
<section class="slide" id="sN">
    <div class="card">
        <div class="sec-label r">섹션</div>
        <h2 class="sec-title r">제목 <em>강조</em></h2>
        <div class="hr r"></div>
        <div class="big-stats-grid r">
            <div class="big-stat-box">
                <div class="big-stat-n" data-count="42">42</div>
                <div class="big-stat-l">설명</div>
            </div>
        </div>
        <div class="hl r">
            <div class="hl-l">핵심</div>
            <div class="hl-v">내용</div>
        </div>
    </div>
</section>
```

### 이미지 인사이트 슬라이드
```html
<section class="slide" id="sN">
    <div class="card">
        <div class="platform-badge" style="background:#색상;" class="r">섹션명</div>
        <h2 class="sec-title r"><em>슬라이드 핵심 메시지</em></h2>
        <div class="hr r"></div>
        <div class="insight-grid r">
            <div class="insight-card">
                <div class="insight-icon"><img src="images/사진.png" alt="설명"></div>
                <div class="insight-kw">키워드 <button class="preview-btn" onclick="event.stopPropagation();document.getElementById('photoModal').classList.add('open')"></button></div>
                <div class="insight-desc">상세 설명</div>
            </div>
        </div>
        <div class="hl r">
            <div class="hl-l">특징</div>
            <div class="hl-v">핵심 요약 문장</div>
        </div>
    </div>
</section>
```

### Feature Explorer 슬라이드
```html
<section class="slide" id="sN">
    <div class="card">
        <div class="sec-label r">섹션</div>
        <h2 class="sec-title r">제목</h2>
        <div class="hr r"></div>
        <div class="feat-tabs r">
            <button class="feat-tab tab-a active" onclick="showFeat('a')">탭1</button>
            <button class="feat-tab tab-b" onclick="showFeat('b')">탭2</button>
        </div>
        <div class="feat-panel active" id="feat-a">
            <div class="feat-grid">
                <div class="feat-card c-vio">
                    <div class="feat-icon">🎯</div>
                    <div class="feat-name">기능명</div>
                    <div class="feat-desc">설명</div>
                    <div class="feat-tag">태그</div>
                </div>
            </div>
        </div>
    </div>
</section>
```
