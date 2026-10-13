"""LifeCity 生命机制数字孪生模型。

模型把外部环境依次映射到分子机制、细胞器状态和整体细胞功能。它强调
因果关系的可解释性，所有指标均为科普展示量，不用于临床或科研定量计算。
"""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class MetabolicNode:
    """代谢网络中的一个反应节点。"""

    key: str
    name: str
    activity: float
    state: str


@dataclass(frozen=True)
class MetabolismResult:
    """从分子层到细胞器层的一次完整推演结果。"""

    atp_efficiency: float
    atp_synthesis_efficiency: float
    atp_output: int
    ros_level: float
    dna_stability: float
    protein_synthesis: float
    repair_activity: float
    temperature_factor: float
    metabolic_balance: float
    mitochondrial_health: float
    ribosome_health: float
    membrane_integrity: float
    health_index: float
    status: str
    status_color: str
    mitochondrial_brightness: float
    particle_speed: float
    network_nodes: tuple[MetabolicNode, ...]


def clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    """把展示指标限制在指定范围。"""

    return max(minimum, min(maximum, value))


def calculate_temperature_factor(temperature: float) -> float:
    """37 ℃ 附近酶活性最高，偏离后按高斯曲线下降。"""

    return math.exp(-((temperature - 37.0) / 7.5) ** 2)


def _node_state(activity: float) -> str:
    """将节点活性转换为交通灯状态。"""

    if activity >= 75:
        return "active"
    if activity >= 40:
        return "stressed"
    return "blocked"


def calculate_metabolism(
    oxygen: float,
    glucose: float,
    temperature: float,
    toxin: float,
) -> MetabolismResult:
    """按“环境 → 分子机制 → 细胞器 → 细胞功能”顺序完成推演。"""

    oxygen_ratio = clamp(oxygen) / 100.0
    glucose_ratio = clamp(glucose) / 100.0
    toxin_ratio = clamp(toxin) / 100.0
    temperature_factor = calculate_temperature_factor(temperature)
    temperature_stress = clamp(abs(temperature - 37.0) * 7.5)
    hypoxia_pressure = clamp((45.0 - oxygen) * 1.8) if oxygen < 45 else 0.0

    # 1) 外部环境首先改变氧化应激和基础能量转化。
    ros_level = clamp(
        7.0 + toxin * 0.72 + hypoxia_pressure * 0.48 + temperature_stress * 0.32
    )
    toxin_factor = 1.0 - 0.45 * toxin_ratio
    atp_efficiency = clamp(
        glucose_ratio * oxygen_ratio * temperature_factor * toxin_factor * 100.0
    )
    # 以正常细胞的 62% 理论效率为 100% 生理参考。
    atp_synthesis_efficiency = clamp(atp_efficiency / 62.0 * 100.0)
    atp_output = round(atp_efficiency / 100.0 * 4600)

    # 2) ROS、毒素和温度共同影响遗传信息与蛋白质生产。
    dna_stability = clamp(
        103.0 - toxin * 0.43 - ros_level * 0.22 - temperature_stress * 0.20
    )
    repair_activity = clamp(
        max(0.0, (100.0 - dna_stability) * 1.35 + max(0.0, ros_level - 25.0) * 0.52)
    )
    protein_synthesis = clamp(
        0.43 * atp_synthesis_efficiency
        + 0.31 * glucose
        + 26.0 * temperature_factor
        - 0.22 * toxin
        - 0.08 * ros_level
    )

    # 3) 分子变化进一步映射为细胞器功能状态。
    mitochondrial_health = clamp(
        0.52 * atp_synthesis_efficiency
        + 0.23 * oxygen
        + 0.25 * (100.0 - ros_level)
    )
    ribosome_health = clamp(
        0.76 * protein_synthesis + 0.24 * (100.0 - ros_level * 0.45)
    )
    membrane_integrity = clamp(
        101.0 - toxin * 0.56 - temperature_stress * 0.23 - ros_level * 0.08
    )
    substrate_balance = 100.0 - abs(oxygen - glucose) * 0.45
    metabolic_balance = clamp(
        0.45 * substrate_balance
        + 35.0 * temperature_factor
        + 0.20 * mitochondrial_health
        - 0.25 * toxin
    )

    # 4) 延续原有健康指数权重，同时让 ATP 状态来自分子机制层。
    health_index = clamp(
        0.4 * atp_synthesis_efficiency
        + 0.3 * dna_stability
        + 0.3 * metabolic_balance
    )

    if health_index >= 90:
        status, status_color = "健康稳定", "#45f3b2"
    elif health_index >= 60:
        status, status_color = "压力状态", "#ffd75e"
    else:
        status, status_color = "危险状态", "#ff5d78"

    # 代谢通路节点使用相同量纲，便于界面按状态着色。
    glycolysis = clamp(0.66 * glucose + 34.0 * temperature_factor - toxin * 0.12)
    tca_cycle = clamp(
        0.48 * glycolysis + 0.32 * oxygen + 0.20 * mitochondrial_health
    )
    electron_transport = clamp(
        0.58 * oxygen + 0.27 * mitochondrial_health + 0.15 * (100.0 - ros_level)
    )
    node_values = (
        ("glucose", "葡萄糖", clamp(glucose)),
        ("glycolysis", "糖酵解", glycolysis),
        ("tca", "三羧酸循环", tca_cycle),
        ("etc", "电子传递链", electron_transport),
        ("atp", "ATP", atp_synthesis_efficiency),
    )
    network_nodes = tuple(
        MetabolicNode(key, name, round(activity, 1), _node_state(activity))
        for key, name, activity in node_values
    )

    return MetabolismResult(
        atp_efficiency=round(atp_efficiency, 2),
        atp_synthesis_efficiency=round(atp_synthesis_efficiency, 1),
        atp_output=atp_output,
        ros_level=round(ros_level, 1),
        dna_stability=round(dna_stability, 1),
        protein_synthesis=round(protein_synthesis, 1),
        repair_activity=round(repair_activity, 1),
        temperature_factor=round(temperature_factor, 3),
        metabolic_balance=round(metabolic_balance, 1),
        mitochondrial_health=round(mitochondrial_health, 1),
        ribosome_health=round(ribosome_health, 1),
        membrane_integrity=round(membrane_integrity, 1),
        health_index=round(health_index, 1),
        status=status,
        status_color=status_color,
        mitochondrial_brightness=round(0.35 + 0.85 * atp_efficiency / 100.0, 2),
        particle_speed=round(0.7 + 2.8 * atp_efficiency / 100.0, 2),
        network_nodes=network_nodes,
    )

