"""预设实验场景及参数说明。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExperimentPreset:
    name: str
    icon: str
    description: str
    oxygen: int
    glucose: int
    temperature: int
    toxin: int


EXPERIMENTS = {
    "normal": ExperimentPreset(
        "正常细胞", "✦", "标准环境，观察细胞正常代谢状态", 78, 82, 37, 12
    ),
    "hypoxia": ExperimentPreset(
        "缺氧挑战", "▲", "降低氧气浓度，观察代谢链变化", 15, 80, 37, 15
    ),
    "toxin": ExperimentPreset(
        "毒素攻击", "⚗", "引入毒素，观察细胞应激反应", 65, 70, 39, 72
    ),
}


def apply_preset(session_state, preset_key: str) -> None:
    """将预设写入 Streamlit 会话状态。"""

    preset = EXPERIMENTS[preset_key]
    session_state["oxygen"] = preset.oxygen
    session_state["glucose"] = preset.glucose
    session_state["temperature"] = preset.temperature
    session_state["toxin"] = preset.toxin
    session_state["active_experiment"] = preset_key

