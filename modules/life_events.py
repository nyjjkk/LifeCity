"""动态生命事件检测与因果链生成。"""

from __future__ import annotations

from dataclasses import dataclass

from .metabolism import MetabolismResult


@dataclass(frozen=True)
class LifeEvent:
    """一次由环境扰动触发的生命机制事件。"""

    name: str
    icon: str
    level: str
    trigger: str
    mechanism: str
    response: str


def detect_life_events(
    oxygen: float,
    glucose: float,
    temperature: float,
    toxin: float,
    result: MetabolismResult,
) -> tuple[LifeEvent, ...]:
    """检测可同时发生的生命事件，而不是互斥的单一状态。"""

    events: list[LifeEvent] = []

    if oxygen < 35:
        level = "critical" if oxygen < 20 else "warning"
        events.append(
            LifeEvent(
                "缺氧响应", "O₂", level,
                f"氧气降至 {oxygen:.0f}%",
                "电子传递链受阻，氧化磷酸化效率下降",
                f"ATP降至 {result.atp_output:,} molecules/s，线粒体进入节能模式",
            )
        )

    if toxin >= 35:
        level = "critical" if toxin >= 65 else "warning"
        events.append(
            LifeEvent(
                "毒素应激", "☣", level,
                f"毒素升至 {toxin:.0f}%",
                f"ROS升至 {result.ros_level:.0f}%，DNA稳定性下降",
                f"DNA修复通路启动，修复活性 {result.repair_activity:.0f}%",
            )
        )

    if glucose < 25:
        events.append(
            LifeEvent(
                "底物短缺", "⬡", "warning",
                f"葡萄糖仅 {glucose:.0f}%",
                "糖酵解底物不足，三羧酸循环通量下降",
                "蛋白质合成减速，细胞优先维持基础生命活动",
            )
        )

    if abs(temperature - 37) >= 6:
        events.append(
            LifeEvent(
                "温度应激", "♨", "warning",
                f"温度偏离最适值至 {temperature:.0f}℃",
                "酶构象与反应速率改变，代谢网络通量降低",
                "热休克/低温保护机制启动，蛋白质合成受到抑制",
            )
        )

    if not events:
        events.append(
            LifeEvent(
                "稳态维持", "✓", "stable",
                "外部环境处于适宜区间",
                "代谢网络通畅，ROS维持低水平",
                "ATP供给充足，各细胞器协同运行",
            )
        )

    return tuple(events)


def primary_causal_chain(events: tuple[LifeEvent, ...]) -> tuple[str, str, str, str]:
    """返回最紧迫事件的四阶段机制演化链。"""

    rank = {"critical": 2, "warning": 1, "stable": 0}
    primary = max(events, key=lambda event: rank[event.level])
    if primary.name == "缺氧响应":
        return primary.trigger, "电子传递链受阻", "ATP生成降低", "细胞进入低能状态"
    if primary.name == "毒素应激":
        return primary.trigger, "ROS水平升高", "DNA损伤风险增加", "启动DNA修复"
    if primary.name == "底物短缺":
        return primary.trigger, "糖酵解通量下降", "ATP底物不足", "细胞启动节能程序"
    if primary.name == "温度应激":
        return primary.trigger, "代谢酶活性改变", "蛋白质合成减速", "应激保护机制启动"
    return "环境条件适宜", "代谢网络通畅", "ATP稳定生成", "细胞维持稳态"

