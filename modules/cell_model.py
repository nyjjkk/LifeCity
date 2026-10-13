"""中央细胞城市视图与资源回退工具。"""

from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter
import streamlit as st

from .life_events import LifeEvent
from .metabolism import MetabolismResult


def ensure_placeholder(path: Path, title: str, accent: str = "#2bdcff") -> None:
    """资源丢失时生成有科技感的占位图，保证程序仍可运行。"""

    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (1280, 720), "#031226")
    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    draw.ellipse((235, 70, 1045, 650), outline=accent, width=12)
    draw.ellipse((320, 145, 960, 575), outline="#745cff", width=5)
    glow = glow.filter(ImageFilter.GaussianBlur(12))
    image = Image.alpha_composite(image.convert("RGBA"), glow)
    draw = ImageDraw.Draw(image)
    draw.ellipse((235, 70, 1045, 650), outline=accent, width=3)
    draw.text((60, 650), f"LifeCity / {title}", fill="white")
    image.convert("RGB").save(path, quality=92)


@st.cache_data(show_spinner=False, max_entries=8)
def _cached_image_data_uri(path_text: str, modified_ns: int) -> str:
    """将高清图片压缩为 WebP 并缓存，降低公网首屏传输体积。"""

    del modified_ns  # 文件时间用于资源变更后的缓存自动失效。
    path = Path(path_text)
    with Image.open(path) as image:
        image.thumbnail((2048, 1152), Image.Resampling.LANCZOS)
        buffer = BytesIO()
        image.convert("RGB").save(buffer, format="WEBP", quality=86, method=4)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/webp;base64,{encoded}"


def image_to_data_uri(path: Path) -> str:
    """跨平台读取图片，并复用压缩后的缓存结果。"""

    resolved = path.resolve()
    return _cached_image_data_uri(str(resolved), resolved.stat().st_mtime_ns)


def render_cell_city_html(image_path: Path, result: MetabolismResult) -> str:
    """生成带动态标注和粒子效果的中央细胞城市 HTML。"""

    ensure_placeholder(image_path, "CELL CITY")
    image_uri = image_to_data_uri(image_path)
    speed = max(0.45, 3.7 - result.particle_speed)
    brightness = result.mitochondrial_brightness
    status_class = (
        "stable" if result.status == "健康稳定" else "pressure" if result.status == "压力状态" else "danger"
    )

    return f"""
    <div class="city-stage {status_class}" style="--flow-speed:{speed:.2f}s;--energy:{brightness:.2f}">
      <img class="city-image" src="{image_uri}" alt="细胞城市数字孪生模型" />
      <div class="scanline"></div>
      <div class="corner corner-tl"></div><div class="corner corner-tr"></div>
      <div class="corner corner-bl"></div><div class="corner corner-br"></div>

      <div class="city-label dna-label">
        <div class="label-icon">⌬</div><div><b>DNA数据库中心</b><small>存储遗传信息 · 调控生命活动</small></div>
      </div>
      <div class="city-label mito-label">
        <div class="label-icon gold">⚡</div><div><b>线粒体能源中心</b><small>有氧呼吸 · 生成ATP能量</small></div>
      </div>
      <div class="city-label ribo-label">
        <div class="label-icon violet">⬡</div><div><b>核糖体工厂</b><small>mRNA进入 → 蛋白质生成</small></div>
      </div>
      <div class="city-label network-label">
        <div class="label-icon">◌</div><div><b>运输网络</b><small>物质运输与信号传递</small></div>
      </div>

      <div class="input-tag glucose-tag"><i></i> 葡萄糖输入</div>
      <div class="input-tag oxygen-tag"><i></i> O₂ 氧气供应</div>
      <div class="atp-flow"><span>ATP</span><span>ATP</span><span>ATP</span></div>
      <div class="twin-status"><i></i> DIGITAL TWIN ONLINE · {result.status}</div>
      <div class="current-state">CURRENT STATE <b>{'HEALTHY' if result.status == '健康稳定' else 'STRESSED' if result.status == '压力状态' else 'CRITICAL'}</b></div>
    </div>
    """


def render_metabolic_network_html(result: MetabolismResult) -> str:
    """渲染会随通量改变颜色的五节点代谢网络。"""

    nodes: list[str] = []
    for index, node in enumerate(result.network_nodes):
        nodes.append(
            f"""
            <div class="metabolic-node {node.state}">
              <span class="node-order">0{index + 1}</span>
              <b>{node.name}</b>
              <strong>{node.activity:.0f}%</strong>
              <small>{'通路活跃' if node.state == 'active' else '通量受压' if node.state == 'stressed' else '通路受阻'}</small>
            </div>
            """
        )
        if index < len(result.network_nodes) - 1:
            nodes.append('<div class="metabolic-arrow"><i></i><span>›</span></div>')

    return f"""
    <div class="mechanism-panel">
      <div class="mechanism-title"><span>⌬</span><b>代谢网络数字孪生</b><small>METABOLIC FLUX · 实时通量映射</small></div>
      <div class="metabolic-network">{''.join(nodes)}</div>
      <div class="network-legend"><i class="lg-active"></i>活跃　<i class="lg-stressed"></i>受压　<i class="lg-blocked"></i>受阻</div>
    </div>
    """.strip()


def render_causal_chain_html(chain: tuple[str, str, str, str]) -> str:
    """渲染环境变化到细胞响应的四阶段机制演化链。"""

    environment, mechanism, energy, response = chain
    return f"""
    <div class="causal-chain" aria-label="环境变化到分子机制再到细胞响应">
      <div class="causal-step env"><em>01</em><small>环境变化</small><b>{environment}</b></div>
      <div class="causal-link"><span>↓</span><i></i></div>
      <div class="causal-step molecule"><em>02</em><small>分子响应</small><b>{mechanism}</b></div>
      <div class="causal-link"><span>↓</span><i></i></div>
      <div class="causal-step energy"><em>03</em><small>能量变化</small><b>{energy}</b></div>
      <div class="causal-link"><span>↓</span><i></i></div>
      <div class="causal-step response"><em>04</em><small>细胞状态</small><b>{response}</b></div>
    </div>
    """.strip()


def _health_class(value: float) -> str:
    if value >= 80:
        return "healthy"
    if value >= 55:
        return "strained"
    return "damaged"


def render_organelle_cards_html(result: MetabolismResult) -> str:
    """渲染四类细胞器健康卡。"""

    items = (
        ("线粒体", "ϟ", result.mitochondrial_health, "能量转换中心"),
        ("DNA", "⌬", result.dna_stability, f"修复活性 {result.repair_activity:.0f}%"),
        ("核糖体", "⬡", result.ribosome_health, "蛋白质生产系统"),
        ("细胞膜", "◉", result.membrane_integrity, "物质交换屏障"),
    )
    cards = []
    for name, icon, value, detail in items:
        state = _health_class(value)
        status = "稳定" if state == "healthy" else "受压" if state == "strained" else "受损"
        cards.append(
            f"""
            <div class="organelle-card {state}">
              <div class="organelle-icon">{icon}</div>
              <div class="organelle-data"><b>{name}</b><small>{detail}</small>
                <div class="organelle-bar"><i style="width:{value:.0f}%"></i></div>
              </div>
              <div class="organelle-value"><strong>{value:.0f}%</strong><small>{status}</small></div>
            </div>
            """.strip()
        )
    return ''.join(cards)


def render_life_events_html(event_log: list[dict[str, str]]) -> str:
    """渲染最近发生的生命事件时间线。"""

    rows: list[str] = []
    for event in event_log[-2:][::-1]:
        rows.append(
            f"""
            <div class="life-event {event['level']}">
              <div class="event-time">[{event['time']}]</div>
              <div class="event-signal">{event['icon']}</div>
              <div class="event-copy"><b>{event['name']}</b><small>{event['trigger']} → {event['response']}</small></div>
            </div>
            """.strip()
        )
    return ''.join(rows)

