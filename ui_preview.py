"""LifeCity 比赛展示级 UI 原型。

本文件只负责静态视觉预览，不导入业务模型，也不会修改 app.py 的任何状态。
运行方式：streamlit run ui_preview.py
"""

from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="生命之城 LifeCity · UI Preview",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def image_data_uri(path: Path) -> str:
    """把本地图片转换为浏览器可直接显示的数据 URI。"""
    if not path.exists():
        return ""
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


ROOT = Path(__file__).resolve().parent
CELL_CITY = image_data_uri(ROOT / "assets" / "cell_city.png")


CSS = r"""
<style>
:root {
  --deep: #020c18;
  --panel: rgba(4, 27, 47, .78);
  --panel-strong: rgba(5, 34, 56, .92);
  --line: rgba(55, 199, 238, .34);
  --cyan: #35dcff;
  --mint: #42f0b2;
  --blue: #4b8cff;
  --gold: #ffd05a;
  --red: #ff5f78;
  --text: #eefbff;
  --muted: #7ca6ba;
}

* { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], .stApp {
  height: 100%;
  overflow: hidden !important;
}
body { margin: 0; }
[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], #MainMenu, footer { display: none !important; }
[data-testid="stAppViewContainer"] {
  background:
    radial-gradient(circle at 50% 28%, rgba(17, 100, 139, .22), transparent 36%),
    radial-gradient(circle at 82% 72%, rgba(20, 130, 106, .11), transparent 28%),
    linear-gradient(rgba(33, 103, 138, .065) 1px, transparent 1px),
    linear-gradient(90deg, rgba(33, 103, 138, .065) 1px, transparent 1px),
    var(--deep);
  background-size: auto, auto, 2.8rem 2.8rem, 2.8rem 2.8rem, auto;
  color: var(--text);
}
[data-testid="stMainBlockContainer"] {
  max-width: none !important;
  width: 100vw !important;
  height: 100vh !important;
  padding: .8vh .8vw !important;
}
[data-testid="stMainBlockContainer"] > div,
[data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] {
  height: 100%;
  gap: 0 !important;
}

.lifecity-preview {
  position: relative;
  width: 100%;
  height: 98.4vh;
  display: grid;
  grid-template-rows: 9.5vh 63.2vh 24.1vh;
  gap: .8vh;
  font-family: "Microsoft YaHei", "PingFang SC", "Segoe UI", sans-serif;
  color: var(--text);
  overflow: hidden;
}
.lifecity-preview::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: linear-gradient(105deg, transparent 42%, rgba(62, 225, 255, .025) 50%, transparent 58%);
  transform: translateX(-100%);
  animation: global-scan 9s linear infinite;
  z-index: 8;
}

.glass {
  position: relative;
  min-width: 0;
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: .72rem;
  background: linear-gradient(145deg, rgba(8, 43, 69, .82), rgba(2, 18, 34, .72));
  box-shadow: inset 0 0 1.8rem rgba(35, 166, 210, .045), 0 0 1.2rem rgba(14, 158, 210, .06);
  backdrop-filter: blur(.7rem);
}
.glass::before, .glass::after {
  content: "";
  position: absolute;
  width: 1.8rem;
  height: 1.8rem;
  pointer-events: none;
}
.glass::before { top: -.05rem; left: -.05rem; border-top: 2px solid var(--cyan); border-left: 2px solid var(--cyan); border-radius: .72rem 0 0 0; }
.glass::after { right: -.05rem; bottom: -.05rem; border-right: 2px solid rgba(66, 240, 178, .7); border-bottom: 2px solid rgba(66, 240, 178, .7); border-radius: 0 0 .72rem 0; }

/* 顶部舞台 */
.topbar {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  align-items: center;
  padding: 0 1.15vw;
  border-color: rgba(49, 200, 240, .4);
  background: linear-gradient(90deg, rgba(3, 25, 44, .93), rgba(4, 47, 70, .82), rgba(3, 25, 44, .93));
}
.topbar::after { width: 32%; height: 2px; right: 34%; bottom: 0; border: 0; background: linear-gradient(90deg, transparent, var(--cyan), transparent); box-shadow: 0 0 .8rem var(--cyan); }
.mission-mark { display: flex; align-items: center; gap: .7vw; color: #a3c7d7; font-size: clamp(.9rem, .88vw, 1.1rem); letter-spacing: .08em; }
.mission-mark i { width: .55rem; height: .55rem; border-radius: 50%; background: var(--mint); box-shadow: 0 0 .8rem var(--mint); animation: breathe 2.5s ease-in-out infinite; }
.mission-mark small { display: block; margin-top: .25vh; color: #537d92; font-size: .66rem; letter-spacing: .16em; }
.brand { text-align: center; line-height: 1; }
.brand h1 { margin: 0; font-size: clamp(2.15rem, 2.25vw, 2.75rem); font-weight: 800; letter-spacing: .035em; text-shadow: 0 0 1rem rgba(53, 220, 255, .56), 0 0 2.4rem rgba(34, 171, 218, .24); }
.brand h1 span { color: var(--mint); }
.brand p { margin: .65vh 0 0; color: #86bdd0; font-size: clamp(.9rem, .95vw, 1.15rem); letter-spacing: .36em; }
.top-signals { display: flex; align-items: center; justify-content: flex-end; gap: .7vw; }
.signal { display: flex; align-items: center; gap: .4rem; color: #a8ccdb; font-size: clamp(.74rem, .72vw, .9rem); white-space: nowrap; }
.signal i { display: grid; place-items: center; width: 1.9rem; height: 1.9rem; border: 1px solid rgba(53, 220, 255, .38); border-radius: 50%; color: var(--cyan); background: rgba(16, 89, 117, .25); font-style: normal; box-shadow: inset 0 0 .8rem rgba(53, 220, 255, .11); }

/* 三栏主体 */
.cockpit { display: grid; grid-template-columns: 20fr 55fr 25fr; gap: .7vw; min-height: 0; }
.side { display: grid; gap: .8vh; min-height: 0; }
.left-side { grid-template-rows: 34.2vh 12.4vh 15vh; }
.right-side { grid-template-rows: 21.5vh 20.7vh 19.4vh; }
.center-stage { display: grid; grid-template-rows: 48.2vh 14.2vh; gap: .8vh; min-width: 0; min-height: 0; }
.panel { padding: 1.05vh .9vw; }
.panel-title {
  height: 3.3vh;
  display: flex;
  align-items: center;
  gap: .55rem;
  margin-bottom: .65vh;
  border-bottom: 1px solid rgba(61, 179, 219, .2);
  font-size: clamp(1.05rem, 1.15vw, 1.38rem);
  font-weight: 760;
  color: #f4fdff;
}
.panel-title i { width: .55rem; height: .55rem; border: 2px solid var(--cyan); transform: rotate(45deg); box-shadow: 0 0 .55rem rgba(53, 220, 255, .6); }

/* 左栏 */
.parameters { display: grid; gap: .6vh; }
.parameter { padding: .2vh .2vw .35vh; }
.parameter-head { display: grid; grid-template-columns: 1fr auto; align-items: end; gap: .5rem; }
.parameter-name { font-size: clamp(.95rem, .92vw, 1.1rem); font-weight: 680; color: #d9f3fb; }
.parameter-name span { color: var(--cyan); margin-right: .4rem; }
.parameter-value { font-size: clamp(1.35rem, 1.65vw, 2rem); line-height: 1; font-weight: 800; color: #effeff; text-shadow: 0 0 .7rem rgba(53, 220, 255, .38); }
.track { position: relative; height: .42rem; margin-top: .65vh; border-radius: 1rem; background: rgba(26, 70, 91, .67); overflow: hidden; }
.track b { display: block; height: 100%; border-radius: inherit; background: linear-gradient(90deg, #1eb9f0, var(--mint)); box-shadow: 0 0 .8rem rgba(66, 240, 178, .56); }
.track.gold b { background: linear-gradient(90deg, #df9f2d, var(--gold)); box-shadow: 0 0 .8rem rgba(255, 208, 90, .5); }
.track.violet b { background: linear-gradient(90deg, #7859df, #c08bff); box-shadow: 0 0 .8rem rgba(178, 125, 255, .45); }
.mode-buttons { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .48vw; }
.mode-btn { height: 6.2vh; display: grid; place-items: center; border: 1px solid rgba(45, 165, 213, .38); border-radius: .55rem; background: rgba(8, 49, 75, .72); color: #a8cada; font-family: inherit; font-size: clamp(.74rem, .76vw, .92rem); }
.mode-btn.active { border-color: var(--cyan); background: linear-gradient(145deg, rgba(28, 122, 163, .55), rgba(9, 58, 87, .85)); color: #fff; box-shadow: inset 0 0 1rem rgba(53, 220, 255, .12), 0 0 .75rem rgba(53, 220, 255, .14); }
.mode-btn span { display: block; color: var(--cyan); font-size: 1rem; line-height: 1; margin-bottom: .2vh; }
.key-list { display: grid; gap: .65vh; }
.key-row { display: grid; grid-template-columns: 1fr auto; gap: .25vh .5rem; align-items: center; }
.key-row span, .key-row b { font-size: clamp(.83rem, .82vw, .98rem); }
.key-row span { color: #b8d5e1; }
.key-row b { color: var(--mint); }
.key-row .track { grid-column: 1 / 3; margin: 0; height: .34rem; }

/* 中央细胞城市 */
.cell-stage { position: relative; background: #03111f; }
.cell-stage::before { content: ""; position: absolute; inset: 0; z-index: 1; background: radial-gradient(circle at 55% 54%, transparent 43%, rgba(1, 12, 24, .22) 70%, rgba(1, 10, 20, .72) 100%); pointer-events: none; }
.cell-stage img { width: 100%; height: 100%; display: block; object-fit: cover; object-position: center; filter: saturate(1.1) contrast(1.04) brightness(.92); }
.stage-corners { position: absolute; inset: .75rem; z-index: 3; border: 0; pointer-events: none; background: linear-gradient(var(--cyan),var(--cyan)) left top/2rem 2px no-repeat, linear-gradient(var(--cyan),var(--cyan)) left top/2px 2rem no-repeat, linear-gradient(var(--cyan),var(--cyan)) right top/2rem 2px no-repeat, linear-gradient(var(--cyan),var(--cyan)) right top/2px 2rem no-repeat, linear-gradient(var(--cyan),var(--cyan)) left bottom/2rem 2px no-repeat, linear-gradient(var(--cyan),var(--cyan)) left bottom/2px 2rem no-repeat, linear-gradient(var(--cyan),var(--cyan)) right bottom/2rem 2px no-repeat, linear-gradient(var(--cyan),var(--cyan)) right bottom/2px 2rem no-repeat; opacity: .85; }
.stage-label { position: absolute; z-index: 4; padding: .55vh .7vw; border: 1px solid rgba(53, 220, 255, .45); border-radius: .5rem; background: rgba(2, 22, 39, .82); box-shadow: 0 0 1rem rgba(31, 178, 222, .1); }
.stage-label b { display: block; color: #eafcff; font-size: clamp(.8rem, .86vw, 1rem); }
.stage-label small { color: #7da6b8; font-size: clamp(.62rem, .61vw, .76rem); }
.dna-label { top: 7%; left: 5%; }
.energy-label { top: 28%; right: 3%; border-color: rgba(255, 208, 90, .5); }
.factory-label { bottom: 17%; left: 5%; }
.transport-label { bottom: 9%; right: 5%; }
.state-tag, .online-tag { position: absolute; z-index: 4; display: flex; align-items: center; gap: .45rem; border-radius: 2rem; background: rgba(2, 20, 35, .82); color: #9ebfce; letter-spacing: .06em; }
.state-tag { top: 3%; right: 2%; padding: .55vh .8vw; border: 1px solid rgba(66, 240, 178, .38); font-size: clamp(.68rem, .65vw, .8rem); }
.state-tag b { color: var(--mint); }
.online-tag { left: 2%; bottom: 3%; padding: .55vh .75vw; border: 1px solid rgba(53, 220, 255, .35); font-size: clamp(.66rem, .63vw, .78rem); }
.online-tag i { width: .52rem; height: .52rem; border-radius: 50%; background: var(--mint); box-shadow: 0 0 .65rem var(--mint); animation: breathe 2s ease-in-out infinite; }

.metabolic-panel { padding: .8vh .8vw; }
.metabolic-head { height: 2.7vh; display: flex; align-items: center; justify-content: space-between; }
.metabolic-head h2 { margin: 0; font-size: clamp(1rem, 1.08vw, 1.3rem); }
.metabolic-head span { color: #648da0; font-size: .7rem; letter-spacing: .1em; }
.metabolic-flow { height: 9.4vh; display: grid; grid-template-columns: 1fr .26fr 1fr .26fr 1fr .26fr 1fr .26fr 1fr; align-items: center; gap: .25vw; }
.met-node { position: relative; height: 7.2vh; display: flex; flex-direction: column; align-items: center; justify-content: center; border-radius: .6rem; background: linear-gradient(145deg, rgba(12, 69, 89, .82), rgba(4, 35, 55, .9)); border: 1px solid rgba(66, 240, 178, .34); }
.met-node b { font-size: clamp(.78rem, .8vw, .96rem); white-space: nowrap; }
.met-node strong { margin-top: .4vh; color: var(--mint); font-size: clamp(.9rem, .92vw, 1.1rem); }
.met-node:last-child { border-color: rgba(255, 208, 90, .5); box-shadow: inset 0 0 1rem rgba(255, 208, 90, .08); }
.met-node:last-child strong { color: var(--gold); }
.flow-arrow { position: relative; height: 2px; background: linear-gradient(90deg, rgba(53, 220, 255, .15), var(--cyan)); box-shadow: 0 0 .55rem rgba(53, 220, 255, .4); }
.flow-arrow::after { content: ""; position: absolute; right: -.05rem; top: -.23rem; width: .45rem; height: .45rem; border-top: 2px solid var(--cyan); border-right: 2px solid var(--cyan); transform: rotate(45deg); }
.flow-arrow::before { content: ""; position: absolute; top: -.2rem; left: 0; width: .38rem; height: .38rem; border-radius: 50%; background: var(--mint); box-shadow: 0 0 .65rem var(--mint); animation: data-flow 2.5s linear infinite; }

/* 右栏 */
.diagnosis { display: grid; grid-template-columns: .8fr 1.2fr; gap: .75vw; height: 15.8vh; }
.diagnosis-state { display: flex; flex-direction: column; align-items: center; justify-content: center; border-radius: .65rem; background: radial-gradient(circle, rgba(36, 166, 132, .17), rgba(4, 31, 48, .68)); }
.diagnosis-state span { color: #81a8b9; font-size: clamp(.72rem, .7vw, .85rem); }
.diagnosis-state b { margin: .55vh 0; color: var(--mint); font-size: clamp(1.2rem, 1.4vw, 1.7rem); }
.diagnosis-state strong { font-size: clamp(1.5rem, 1.8vw, 2.2rem); }
.diagnosis-copy { display: flex; flex-direction: column; justify-content: center; min-width: 0; }
.diagnosis-copy b { color: var(--cyan); font-size: clamp(.76rem, .75vw, .9rem); margin-bottom: .55vh; }
.diagnosis-copy p { margin: 0; color: #c9e0ea; font-size: clamp(.8rem, .8vw, .98rem); line-height: 1.55; }
.organelle-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); grid-template-rows: repeat(2, 1fr); gap: .65vh .45vw; height: 15.1vh; }
.organelle { display: grid; grid-template-columns: 2rem 1fr; align-items: center; gap: .45rem; padding: .5vh .5vw; border-radius: .55rem; background: rgba(5, 37, 57, .72); border: 1px solid rgba(48, 141, 175, .22); min-width: 0; }
.organelle-icon { grid-row: 1 / 3; width: 1.85rem; height: 1.85rem; display: grid; place-items: center; border-radius: 50%; background: rgba(66, 240, 178, .1); color: var(--mint); font-size: .88rem; }
.organelle b { align-self: end; font-size: clamp(.78rem, .78vw, .94rem); }
.organelle span { align-self: start; color: var(--mint); font-size: clamp(.86rem, .84vw, 1rem); }
.causal-chain { height: 14vh; display: grid; grid-template-rows: repeat(7, auto); align-items: center; }
.cause-step { min-height: 2.45vh; display: flex; align-items: center; justify-content: space-between; padding: .25vh .55vw; border-left: .18rem solid var(--cyan); border-radius: .35rem; background: rgba(7, 52, 75, .64); }
.cause-step span { color: #6d9aae; font-size: .68rem; }
.cause-step b { font-size: clamp(.76rem, .78vw, .94rem); }
.cause-arrow { text-align: center; height: 1.35vh; color: var(--cyan); font-size: .8rem; line-height: 1.2vh; text-shadow: 0 0 .5rem var(--cyan); animation: arrow-pulse 1.8s ease-in-out infinite; }

/* 底部数据舞台 */
.data-deck { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: .7vw; min-height: 0; }
.data-card { padding: 1vh 1vw; }
.data-title { height: 3.2vh; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(54, 164, 201, .2); font-size: clamp(1rem, 1.08vw, 1.3rem); font-weight: 760; }
.data-title span { color: #577f92; font-size: .66rem; font-weight: 500; letter-spacing: .12em; }
.metric-body { height: 17.8vh; display: flex; align-items: center; justify-content: center; gap: 1.3vw; }
.health-ring { --value: 96%; position: relative; width: 8.2rem; aspect-ratio: 1; display: grid; place-items: center; border-radius: 50%; background: conic-gradient(var(--mint) var(--value), rgba(35, 76, 94, .55) 0); box-shadow: 0 0 1.4rem rgba(66, 240, 178, .17); }
.health-ring::after { content: ""; position: absolute; inset: .8rem; border-radius: 50%; background: #061a2a; box-shadow: inset 0 0 1rem rgba(28, 133, 166, .2); }
.health-ring b { position: relative; z-index: 2; font-size: clamp(2rem, 2.25vw, 2.75rem); }
.health-ring b small { color: #8fbdcd; font-size: .9rem; }
.metric-copy strong { display: block; color: var(--mint); font-size: clamp(1.1rem, 1.25vw, 1.5rem); }
.metric-copy span { display: block; margin-top: .55vh; color: #7197a8; font-size: clamp(.72rem, .7vw, .85rem); }
.atp-orb { width: 5.5rem; aspect-ratio: 1; display: grid; place-items: center; border-radius: 50%; color: #fff3bb; background: radial-gradient(circle at 35% 28%, #fff4af, #e7a919 47%, #8c5a00 100%); box-shadow: 0 0 1.8rem rgba(255, 196, 45, .42), inset -.5rem -.7rem 1rem rgba(84, 43, 0, .35); font-size: 1.35rem; font-weight: 800; }
.atp-number b { display: block; font-size: clamp(2rem, 2.25vw, 2.75rem); letter-spacing: .03em; }
.atp-number span { color: #83adbf; font-size: clamp(.75rem, .75vw, .9rem); }
.chart-body { position: relative; height: 17.8vh; padding-top: .9vh; }
.chart-value { position: absolute; top: 1vh; left: .15vw; z-index: 2; }
.chart-value b { font-size: clamp(1.1rem, 1.22vw, 1.48rem); }
.chart-value span { margin-left: .4rem; color: var(--mint); font-size: .72rem; }
.chart-body svg { width: 100%; height: 100%; overflow: visible; }
.chart-grid { stroke: rgba(91, 145, 166, .13); stroke-width: 1; }
.chart-line { fill: none; stroke: var(--gold); stroke-width: 3; filter: drop-shadow(0 0 5px rgba(255, 208, 90, .45)); }
.chart-area { fill: url(#atpGradient); }
.health-line { stroke: var(--mint); }
.health-area { fill: url(#healthGradient); }

@keyframes breathe { 0%,100% { opacity: .55; transform: scale(.85); } 50% { opacity: 1; transform: scale(1.08); } }
@keyframes data-flow { from { left: 0; } to { left: calc(100% - .35rem); } }
@keyframes arrow-pulse { 0%,100% { opacity: .45; transform: translateY(-1px); } 50% { opacity: 1; transform: translateY(1px); } }
@keyframes global-scan { from { transform: translateX(-100%); } to { transform: translateX(100%); } }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation: none !important; } }

@media (max-width: 1360px) {
  .top-signals .signal:nth-child(2) { display: none; }
  .panel { padding-left: .65vw; padding-right: .65vw; }
  .stage-label small { display: none; }
  .organelle { grid-template-columns: 1.55rem 1fr; }
  .organelle-icon { width: 1.5rem; height: 1.5rem; }
  .metric-copy span, .metabolic-head span { display: none; }
}
</style>
"""


HTML = r"""
<main class="lifecity-preview" aria-label="生命之城数字孪生展示界面">
  <header class="topbar glass">
    <div class="mission-mark"><i></i><div>探索微观生命<small>DIGITAL LIFE TWIN</small></div></div>
    <div class="brand"><h1>生命之城 <span>LifeCity</span></h1><p>细胞代谢数字孪生系统</p></div>
    <div class="top-signals">
      <div class="signal"><i>◉</i>细胞结构</div>
      <div class="signal"><i>⌁</i>代谢网络</div>
      <div class="signal"><i>ϟ</i>能量流动</div>
    </div>
  </header>

  <section class="cockpit">
    <aside class="side left-side" aria-label="环境与实验控制">
      <section class="glass panel">
        <div class="panel-title"><i></i>环境参数控制</div>
        <div class="parameters">
          <div class="parameter"><div class="parameter-head"><div class="parameter-name"><span>O₂</span>氧气浓度</div><div class="parameter-value">78%</div></div><div class="track"><b style="width:78%"></b></div></div>
          <div class="parameter"><div class="parameter-head"><div class="parameter-name"><span>⬡</span>葡萄糖供应</div><div class="parameter-value">82%</div></div><div class="track"><b style="width:82%"></b></div></div>
          <div class="parameter"><div class="parameter-head"><div class="parameter-name"><span>♨</span>温度</div><div class="parameter-value">37℃</div></div><div class="track gold"><b style="width:72%"></b></div></div>
          <div class="parameter"><div class="parameter-head"><div class="parameter-name"><span>☣</span>毒素浓度</div><div class="parameter-value">12%</div></div><div class="track violet"><b style="width:12%"></b></div></div>
        </div>
      </section>

      <section class="glass panel">
        <div class="panel-title"><i></i>实验模式</div>
        <div class="mode-buttons">
          <button class="mode-btn active" type="button"><span>●</span>正常细胞</button>
          <button class="mode-btn" type="button"><span>△</span>缺氧挑战</button>
          <button class="mode-btn" type="button"><span>◇</span>毒素攻击</button>
        </div>
      </section>

      <section class="glass panel">
        <div class="panel-title"><i></i>关键状态</div>
        <div class="key-list">
          <div class="key-row"><span>ATP效率</span><b>96%</b><div class="track"><b style="width:96%"></b></div></div>
          <div class="key-row"><span>ROS水平</span><b>16%</b><div class="track gold"><b style="width:16%"></b></div></div>
          <div class="key-row"><span>DNA稳定性</span><b>94%</b><div class="track"><b style="width:94%"></b></div></div>
        </div>
      </section>
    </aside>

    <section class="center-stage" aria-label="中央生命城市">
      <div class="cell-stage glass">
        <img src="__CELL_IMAGE__" alt="透明细胞膜包裹的生命城市，包含DNA、线粒体、核糖体与运输网络">
        <div class="stage-corners"></div>
        <div class="stage-label dna-label"><b>DNA数据库中心</b><small>遗传信息存储与调控</small></div>
        <div class="stage-label energy-label"><b>线粒体能源中心</b><small>有氧呼吸 · ATP生成</small></div>
        <div class="stage-label factory-label"><b>核糖体工厂</b><small>mRNA进入 · 蛋白质生成</small></div>
        <div class="stage-label transport-label"><b>运输网络</b><small>物质运输与信号传递</small></div>
        <div class="state-tag">CURRENT STATE <b>HEALTHY</b></div>
        <div class="online-tag"><i></i>DIGITAL TWIN ONLINE</div>
      </div>

      <section class="metabolic-panel glass">
        <div class="metabolic-head"><h2>代谢网络数字孪生</h2><span>METABOLIC FLUX · 实时映射</span></div>
        <div class="metabolic-flow">
          <div class="met-node"><b>葡萄糖输入</b><strong>82%</strong></div><div class="flow-arrow"></div>
          <div class="met-node"><b>糖酵解</b><strong>87%</strong></div><div class="flow-arrow"></div>
          <div class="met-node"><b>三羧酸循环</b><strong>84%</strong></div><div class="flow-arrow"></div>
          <div class="met-node"><b>电子传递链</b><strong>91%</strong></div><div class="flow-arrow"></div>
          <div class="met-node"><b>ATP输出</b><strong>96%</strong></div>
        </div>
      </section>
    </section>

    <aside class="side right-side" aria-label="智能诊断与机制解释">
      <section class="glass panel">
        <div class="panel-title"><i></i>AI生命助手</div>
        <div class="diagnosis">
          <div class="diagnosis-state"><span>当前状态</span><b>健康稳定</b><strong>96%</strong></div>
          <div class="diagnosis-copy"><b>机制解释</b><p>氧气和葡萄糖供应充足，线粒体氧化磷酸化正常，细胞处于高效稳态。</p></div>
        </div>
      </section>

      <section class="glass panel">
        <div class="panel-title"><i></i>细胞器健康</div>
        <div class="organelle-grid">
          <div class="organelle"><div class="organelle-icon">ϟ</div><b>线粒体</b><span>95%</span></div>
          <div class="organelle"><div class="organelle-icon">⌬</div><b>DNA</b><span>94%</span></div>
          <div class="organelle"><div class="organelle-icon">◌</div><b>核糖体</b><span>92%</span></div>
          <div class="organelle"><div class="organelle-icon">⬡</div><b>细胞膜</b><span>93%</span></div>
        </div>
      </section>

      <section class="glass panel">
        <div class="panel-title"><i></i>生命机制因果链</div>
        <div class="causal-chain">
          <div class="cause-step"><span>环境变化</span><b>氧气下降</b></div><div class="cause-arrow">↓</div>
          <div class="cause-step"><span>分子机制</span><b>电子传递链受阻</b></div><div class="cause-arrow">↓</div>
          <div class="cause-step"><span>能量响应</span><b>ATP减少</b></div><div class="cause-arrow">↓</div>
          <div class="cause-step"><span>细胞响应</span><b>细胞压力增加</b></div>
        </div>
      </section>
    </aside>
  </section>

  <section class="data-deck" aria-label="底部生命数据">
    <article class="data-card glass">
      <div class="data-title">细胞健康指数<span>CELL HEALTH</span></div>
      <div class="metric-body"><div class="health-ring"><b>96<small>%</small></b></div><div class="metric-copy"><strong>健康稳定</strong><span>系统综合生命状态</span></div></div>
    </article>
    <article class="data-card glass">
      <div class="data-title">ATP能量输出<span>ENERGY OUTPUT</span></div>
      <div class="metric-body"><div class="atp-orb">ATP</div><div class="atp-number"><b>2,783</b><span>molecules / s</span></div></div>
    </article>
    <article class="data-card glass">
      <div class="data-title">ATP变化趋势<span>ATP TREND</span></div>
      <div class="chart-body"><div class="chart-value"><b>稳定输出</b><span>+3.2%</span></div>
        <svg viewBox="0 0 400 150" role="img" aria-label="ATP能量输出保持稳定并轻微上升">
          <defs><linearGradient id="atpGradient" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd05a" stop-opacity=".25"/><stop offset="1" stop-color="#ffd05a" stop-opacity="0"/></linearGradient></defs>
          <path class="chart-grid" d="M0 45H400M0 90H400M0 135H400"/><path class="chart-area" d="M0 112 L28 102 L56 106 L84 88 L112 94 L140 75 L168 82 L196 61 L224 69 L252 52 L280 57 L308 42 L336 49 L366 34 L400 39 L400 150 L0 150Z"/><path class="chart-line" d="M0 112 L28 102 L56 106 L84 88 L112 94 L140 75 L168 82 L196 61 L224 69 L252 52 L280 57 L308 42 L336 49 L366 34 L400 39"/>
        </svg>
      </div>
    </article>
    <article class="data-card glass">
      <div class="data-title">健康状态变化<span>HEALTH TREND</span></div>
      <div class="chart-body"><div class="chart-value"><b>稳态维持</b><span>96%</span></div>
        <svg viewBox="0 0 400 150" role="img" aria-label="细胞健康指数稳定维持在高位">
          <defs><linearGradient id="healthGradient" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#42f0b2" stop-opacity=".24"/><stop offset="1" stop-color="#42f0b2" stop-opacity="0"/></linearGradient></defs>
          <path class="chart-grid" d="M0 45H400M0 90H400M0 135H400"/><path class="chart-area health-area" d="M0 55 L30 51 L60 54 L90 48 L120 53 L150 45 L180 50 L210 40 L240 45 L270 38 L300 43 L330 35 L365 40 L400 34 L400 150 L0 150Z"/><path class="chart-line health-line" d="M0 55 L30 51 L60 54 L90 48 L120 53 L150 45 L180 50 L210 40 L240 45 L270 38 L300 43 L330 35 L365 40 L400 34"/>
        </svg>
      </div>
    </article>
  </section>
</main>
"""


st.html(CSS + HTML.replace("__CELL_IMAGE__", CELL_CITY))

