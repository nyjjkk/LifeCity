"""无需网络接口的规则型 AI 生命助手。"""

from __future__ import annotations

from .metabolism import MetabolismResult


def generate_analysis(
    oxygen: float,
    glucose: float,
    temperature: float,
    toxin: float,
    result: MetabolismResult,
) -> dict[str, str]:
    """根据当前参数返回状态摘要、机理解释和建议。"""

    causes: list[str] = []
    suggestions: list[str] = []

    if oxygen < 30:
        causes.append("氧气供应不足，电子传递链效率显著降低，氧化磷酸化受限")
        suggestions.append("提高氧供应，优先恢复线粒体有氧呼吸")
    elif oxygen < 55:
        causes.append("氧浓度偏低，线粒体正在降低 ATP 合成速率")
        suggestions.append("适度提高氧浓度并持续观察 ATP 曲线")

    if glucose < 30:
        causes.append("葡萄糖底物不足，糖酵解可用原料减少")
        suggestions.append("补充葡萄糖以恢复能量底物供应")
    elif glucose > 92:
        causes.append("葡萄糖供应过高，可能造成代谢负荷和渗透压力")
        suggestions.append("将葡萄糖调回适宜区间")

    if abs(temperature - 37) >= 6:
        causes.append("温度明显偏离 37℃，关键代谢酶活性受到抑制")
        suggestions.append("把温度逐步恢复至 37℃ 附近")
    elif abs(temperature - 37) >= 3:
        causes.append("温度偏离最适区间，酶促反应效率正在下降")
        suggestions.append("微调温度至 35–39℃ 的稳定区间")

    if toxin >= 60:
        causes.append(
            f"高毒素使 ROS 升至 {result.ros_level:.0f}%，正在破坏细胞膜并诱发 DNA 损伤"
        )
        suggestions.append(
            f"立即降低毒素浓度；当前 DNA 修复通路活性为 {result.repair_activity:.0f}%"
        )
    elif toxin >= 30:
        causes.append(f"毒素已触发氧化应激，ROS 水平升至 {result.ros_level:.0f}%")
        suggestions.append("降低毒素暴露，观察 DNA 稳定性是否恢复")

    if not causes:
        causes.append("氧气与葡萄糖供应充足，温度接近酶活性最佳区间")
        suggestions.append("维持当前环境，并继续监测代谢波动")

    opening = {
        "健康稳定": "当前细胞处于健康稳定状态。",
        "压力状态": "当前细胞处于代谢压力状态。",
        "危险状态": "当前细胞已进入危险状态，需要及时干预。",
    }[result.status]

    return {
        "summary": opening,
        "explanation": "；".join(causes) + "。",
        "suggestion": "；".join(suggestions) + "。",
    }


def answer_question(question: str, analysis: dict[str, str], result: MetabolismResult) -> str:
    """用关键词规则回应常见科普提问。"""

    q = question.strip().lower()
    if not q:
        return "可以问我：为什么 ATP 下降、怎样恢复健康，或 DNA 是否稳定。"
    if "atp" in q or "能量" in q:
        return (
            f"当前 ATP 输出约 {result.atp_output:,} molecules/s。"
            f"{analysis['explanation']}"
        )
    if "dna" in q or "遗传" in q:
        return (
            f"当前 DNA 稳定性为 {result.dna_stability:.0f}%。"
            f"修复通路活性为 {result.repair_activity:.0f}%。"
            "毒素升高和温度偏离 37℃ 都会增加遗传信息受损风险。"
        )
    if "ros" in q or "氧化" in q or "自由基" in q:
        return (
            f"当前 ROS 水平为 {result.ros_level:.0f}%。"
            "ROS 过量会造成膜脂质氧化和 DNA 损伤，并推动细胞启动抗氧化与修复通路。"
        )
    if "蛋白" in q or "核糖体" in q:
        return (
            f"当前蛋白质合成能力为 {result.protein_synthesis:.0f}%，"
            f"核糖体健康度为 {result.ribosome_health:.0f}%。ATP不足或 ROS 过高都会降低翻译效率。"
        )
    if "因果" in q or "机制" in q:
        return (
            f"当前机制链为：外部环境扰动 → ROS {result.ros_level:.0f}% / ATP合成效率 "
            f"{result.atp_synthesis_efficiency:.0f}% → 细胞健康指数 {result.health_index:.0f}%。"
        )
    if "建议" in q or "恢复" in q or "怎么办" in q:
        return analysis["suggestion"]
    if "氧" in q:
        return "氧气是线粒体电子传递链的末端电子受体；缺氧会直接限制氧化磷酸化。"
    return f"{analysis['summary']}{analysis['explanation']}建议：{analysis['suggestion']}"

