"""生命之城 LifeCity —— 生命科学数字孪生展示平台。"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from modules.ai_assistant import answer_question, generate_analysis
from modules.cell_model import (
    ensure_placeholder,
    render_causal_chain_html,
    render_cell_city_html,
    render_life_events_html,
    render_metabolic_network_html,
    render_organelle_cards_html,
)
from modules.experiment import EXPERIMENTS, apply_preset
from modules.life_events import detect_life_events, primary_causal_chain
from modules.metabolism import calculate_metabolism


BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="生命之城 LifeCity",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_resource(show_spinner=False)
def resolve_assets_dir(project_root: str) -> Path:
    """缓存部署环境中的资源目录解析，兼容 Windows 与 Linux。"""

    return Path(project_root).resolve() / "assets"


@st.cache_data(show_spinner=False, max_entries=8)
def load_text_asset(path_text: str, modified_ns: int) -> str:
    """按文件修改时间缓存 CSS 等文本资源。"""

    del modified_ns  # 作为缓存失效键使用，无需参与文件读取。
    return Path(path_text).read_text(encoding="utf-8")


ASSETS_DIR = resolve_assets_dir(str(BASE_DIR))


def inject_css() -> None:
    """加载比赛展示级驾驶舱视觉样式。"""

    css_path = ASSETS_DIR / "style.css"
    css = load_text_asset(str(css_path), css_path.stat().st_mtime_ns)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def panel_header(icon: str, title: str, english: str) -> None:
    """输出统一模块标题。"""

    st.markdown(
        f'<div class="panel-head"><b><span>{icon}</span>{title}</b><small>{english}</small></div>',
        unsafe_allow_html=True,
    )


def chart_theme(fig: go.Figure, height: int = 158) -> go.Figure:
    """为趋势图应用低干扰的舞台化主题。"""

    fig.update_layout(
        height=height,
        margin=dict(l=26, r=10, t=14, b=18),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(2,17,34,.12)",
        font=dict(family="Microsoft YaHei", color="#86adc4", size=10),
        hoverlabel=dict(bgcolor="#06233d", bordercolor="#2bdcff", font_color="white"),
        showlegend=False,
    )
    fig.update_xaxes(
        showgrid=False, showticklabels=False, zeroline=False, fixedrange=True,
        title=None,
    )
    fig.update_yaxes(
        showgrid=True, gridcolor="rgba(70,150,188,.13)", zeroline=False,
        fixedrange=True, nticks=4, title=None,
    )
    return fig


def init_state() -> None:
    """初始化交互参数、历史曲线、诊断问答和生命事件。"""

    defaults = dict(oxygen=78, glucose=82, temperature=37, toxin=12)
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)
    st.session_state.setdefault("active_experiment", "normal")
    st.session_state.setdefault("last_params", None)
    st.session_state.setdefault("last_event_params", None)
    st.session_state.setdefault("chat", [])
    st.session_state.setdefault("event_log", [])

    if "history" not in st.session_state:
        rng = np.random.default_rng(2026)
        current = calculate_metabolism(**defaults)
        st.session_state.history = [
            {
                "step": index,
                "ATP": max(0, current.atp_output + int(rng.normal(0, 65))),
                "健康指数": float(np.clip(current.health_index + rng.normal(0, 1.8), 0, 100)),
                "代谢活性": float(np.clip(current.atp_synthesis_efficiency + rng.normal(0, 2.4), 0, 100)),
            }
            for index in range(24)
        ]


def update_history(result, params: tuple[int, int, int, int]) -> None:
    """仅在参数发生变化时写入趋势历史。"""

    if st.session_state.last_params == params:
        return
    history = st.session_state.history
    history.append(
        {
            "step": history[-1]["step"] + 1,
            "ATP": result.atp_output,
            "健康指数": result.health_index,
            "代谢活性": result.atp_synthesis_efficiency,
        }
    )
    st.session_state.history = history[-32:]
    st.session_state.last_params = params


def update_event_log(events, params: tuple[int, int, int, int]) -> None:
    """记录最近两次生命事件，用于诊断中心时间线。"""

    if st.session_state.last_event_params == params:
        return
    stamp = datetime.now().strftime("%H:%M")
    log = st.session_state.event_log
    for event in events:
        log.append(
            {
                "time": stamp,
                "name": event.name,
                "icon": event.icon,
                "level": event.level,
                "trigger": event.trigger,
                "response": event.response,
            }
        )
    st.session_state.event_log = log[-4:]
    st.session_state.last_event_params = params


def environment_control(
    name: str,
    icon: str,
    key: str,
    minimum: int,
    maximum: int,
    unit: str,
    impact: str,
) -> int:
    """显示适合大屏阅读的参数标题、核心数值和机制说明。"""

    current = st.session_state[key]
    st.markdown(
        f"""
        <div class="control-meta">
          <div><b><i>{icon}</i>{name}</b><small>影响：{impact}</small></div>
          <strong>{current}<em>{unit}</em></strong>
        </div>
        """,
        unsafe_allow_html=True,
    )
    slider_format = "%d%%" if unit == "%" else f"%d{unit}"
    value = st.slider(
        name, minimum, maximum, key=key, label_visibility="collapsed",
        format=slider_format,
    )
    return value


inject_css()
init_state()

# ───────────────────────── 顶部标题舞台（10%） ─────────────────────────
with st.container(key="top_stage"):
    st.markdown(
        """
        <div class="topbar">
          <div class="motto"><span>◈</span> 探索微观生命<br><small>构建数字孪生</small></div>
          <div class="brand"><h1>生命之城 <span>LifeCity</span></h1><p>细胞代谢数字孪生系统</p></div>
          <div class="nav-icons">
            <div class="nav-item"><i>◉</i><span>细胞结构</span></div>
            <div class="nav-item"><i>⌬</i><span>代谢网络</span></div>
            <div class="nav-item"><i>ϟ</i><span>能量流动</span></div>
            <div class="nav-item"><i>▱</i><span>数字孪生</span></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ───────────────────────── 中部生命展示区 ─────────────────────────
with st.container(key="main_cockpit"):
    left, center, right = st.columns([0.20, 0.55, 0.25], gap="small")

    with left:
        with st.container(border=True, key="environment_panel"):
            panel_header("◈", "环境参数控制", "ENVIRONMENT CONTROL")
            oxygen = environment_control("氧气浓度", "O₂", "oxygen", 0, 100, "%", "线粒体氧化磷酸化")
            glucose = environment_control("葡萄糖供应", "⬡", "glucose", 0, 100, "%", "糖酵解与能量底物")
            temperature = environment_control("温度", "♨", "temperature", 20, 45, "℃", "代谢酶活性")
            toxin = environment_control("毒素浓度", "☣", "toxin", 0, 100, "%", "ROS与DNA损伤")

    # 外部环境输入完成后，数字孪生从分子机制逐层推演。
    result = calculate_metabolism(oxygen, glucose, temperature, toxin)
    params = (oxygen, glucose, temperature, toxin)
    active = EXPERIMENTS.get(st.session_state.active_experiment)
    if active and params != (active.oxygen, active.glucose, active.temperature, active.toxin):
        st.session_state.active_experiment = "custom"
    update_history(result, params)
    analysis = generate_analysis(oxygen, glucose, temperature, toxin, result)
    life_events = detect_life_events(oxygen, glucose, temperature, toxin, result)
    causal_chain = primary_causal_chain(life_events)
    update_event_log(life_events, params)

    with left:
        with st.container(border=True, key="experiment_panel"):
            panel_header("✦", "实验模式", "EXPERIMENT MODE")
            experiment_cols = st.columns(3, gap="small")
            for index, (preset_key, preset) in enumerate(EXPERIMENTS.items()):
                marker = "●" if st.session_state.active_experiment == preset_key else "○"
                with experiment_cols[index]:
                    st.button(
                        f"{marker} {preset.name}",
                        key=f"preset_{preset_key}",
                        on_click=apply_preset,
                        args=(st.session_state, preset_key),
                    )

        with st.container(border=True, key="process_panel"):
            panel_header("⌁", "关键过程状态", "KEY PROCESSES")
            process_items = (
                ("ATP合成效率", result.atp_synthesis_efficiency, False),
                ("ROS水平", result.ros_level, True),
                ("DNA稳定性", result.dna_stability, False),
                ("膜完整性", result.membrane_integrity, False),
            )
            process_html = []
            for label, value, inverse in process_items:
                danger_value = value if inverse else 100 - value
                state = "bad" if danger_value >= 55 else "warn" if danger_value >= 28 else "good"
                process_html.append(
                    f'<div class="process-row {state}"><span>{label}</span><b>{value:.0f}%</b>'
                    f'<i><em style="width:{value:.0f}%"></em></i></div>'
                )
            st.markdown(f'<div class="process-list">{"".join(process_html)}</div>', unsafe_allow_html=True)

    with center:
        city_image = ASSETS_DIR / "cell_city.png"
        ensure_placeholder(city_image, "CELL CITY")
        st.markdown(render_cell_city_html(city_image, result), unsafe_allow_html=True)
        st.markdown(render_metabolic_network_html(result), unsafe_allow_html=True)

    with right:
        with st.container(border=True, key="diagnostic_panel"):
            panel_header("◉", "AI生命解释中心", "AI LIFE INTERPRETATION")
            status_class = "healthy" if result.status == "健康稳定" else "warning" if result.status == "压力状态" else "critical"
            st.markdown(
                f"""
                <div class="diagnostic-report {status_class}">
                  <div class="diagnostic-status"><span>当前状态</span><b>{result.status}</b><i>{result.health_index:.0f}%</i></div>
                  <div class="diagnostic-section"><small>原因分析</small><p>{analysis['explanation']}</p></div>
                  <div class="diagnostic-section advice"><small>干预建议</small><p>{analysis['suggestion']}</p></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            with st.popover("向 AI 生命助手追问", width="stretch"):
                for message in st.session_state.chat[-2:]:
                    st.caption(("你：" if message["role"] == "user" else "助手：") + message["text"])
                with st.form("assistant_form", clear_on_submit=True):
                    question = st.text_input("提问", placeholder="例如：为什么 ATP 下降？", label_visibility="collapsed")
                    submitted = st.form_submit_button("生成机制解释", width="stretch")
                if submitted and question.strip():
                    st.session_state.chat.extend(
                        [
                            {"role": "user", "text": question.strip()},
                            {"role": "assistant", "text": answer_question(question, analysis, result)},
                        ]
                    )
                    st.rerun()

        with st.container(border=True, key="organelle_panel"):
            panel_header("⌬", "细胞器健康矩阵", "ORGANELLE HEALTH")
            st.markdown(f'<div class="organelle-grid">{render_organelle_cards_html(result)}</div>', unsafe_allow_html=True)

        with st.container(border=True, key="causal_panel"):
            panel_header("⟲", "生命机制因果链", "CAUSAL INFERENCE")
            st.markdown(render_causal_chain_html(causal_chain), unsafe_allow_html=True)
            st.markdown('<div class="recent-event-label">最近生命响应</div>', unsafe_allow_html=True)
            st.markdown(render_life_events_html(st.session_state.event_log), unsafe_allow_html=True)

# ───────────────────────── 底部数据舞台（30%） ─────────────────────────
history_df = pd.DataFrame(st.session_state.history)
with st.container(key="bottom_deck"):
    health_col, atp_col, atp_chart_col, health_chart_col = st.columns(4, gap="small")

    with health_col:
        with st.container(border=True, key="health_card"):
            panel_header("✣", "细胞健康指数", "CELL HEALTH INDEX")
            st.markdown(
                f"""
                <div class="hero-metric health-metric">
                  <div class="metric-ring" style="--health-angle:{result.health_index * 3.6:.1f}deg">
                    <strong>{result.health_index:.0f}<em>%</em></strong>
                  </div>
                  <div class="metric-caption"><b>{result.status}</b><span>系统综合生命状态</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with atp_col:
        with st.container(border=True, key="atp_card"):
            panel_header("ϟ", "ATP能量输出", "ATP ENERGY OUTPUT")
            st.markdown(
                f"""
                <div class="hero-metric atp-metric">
                  <div class="atp-core">ATP</div>
                  <strong>{result.atp_output:,}</strong><span>molecules / s</span>
                  <div class="energy-level"><i style="width:{result.atp_synthesis_efficiency:.0f}%"></i></div>
                  <small>合成效率 {result.atp_synthesis_efficiency:.0f}%</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with atp_chart_col:
        with st.container(border=True, key="atp_trend_card"):
            panel_header("◒", "ATP变化趋势", "ATP TREND")
            atp_fig = go.Figure()
            atp_fig.add_trace(
                go.Scatter(
                    x=history_df["step"], y=history_df["ATP"], mode="lines+markers",
                    line=dict(color="#ffd452", width=3), marker=dict(size=4, color="#fff49b"),
                    fill="tozeroy", fillcolor="rgba(255,197,34,.10)",
                    hovertemplate="ATP %{y:,.0f}<extra></extra>",
                )
            )
            chart_theme(atp_fig).update_yaxes(rangemode="tozero")
            st.plotly_chart(atp_fig, width="stretch", config={"displayModeBar": False, "staticPlot": False})

    with health_chart_col:
        with st.container(border=True, key="health_trend_card"):
            panel_header("⌁", "健康状态变化", "HEALTH TREND")
            recent_delta = history_df["健康指数"].iloc[-1] - history_df["健康指数"].iloc[-2]
            trend_word = "恢复" if recent_delta > 1 else "下降" if recent_delta < -1 else "稳定"
            trend_class = "up" if recent_delta > 1 else "down" if recent_delta < -1 else "flat"
            st.markdown(
                f'<div class="trend-badge {trend_class}"><b>{trend_word}</b><span>{recent_delta:+.1f}%</span></div>',
                unsafe_allow_html=True,
            )
            health_fig = go.Figure()
            health_fig.add_trace(
                go.Scatter(
                    x=history_df["step"], y=history_df["健康指数"], mode="lines+markers",
                    line=dict(color="#45f3b2", width=3), marker=dict(size=4),
                    fill="tozeroy", fillcolor="rgba(69,243,178,.08)",
                    hovertemplate="健康 %{y:.1f}%<extra></extra>",
                )
            )
            chart_theme(health_fig, 148).update_yaxes(range=[0, 105])
            st.plotly_chart(health_fig, width="stretch", config={"displayModeBar": False, "staticPlot": False})

