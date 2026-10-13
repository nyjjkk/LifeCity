# 生命之城 LifeCity

**细胞代谢数字孪生展示系统**，用于“生命演绎·智演万象——生命机制模拟创意大赛”。项目把细胞映射为一座持续运转的未来城市：细胞核是 DNA 数据库，线粒体是能源中心，核糖体是生产工厂，细胞质运输通路则是城市物流网络。系统会实时推演环境扰动如何沿分子通路演化为细胞响应。

**公网体验：** [https://lifecity-qb8b592cd8xc5wyaiscgzr.streamlit.app/](https://lifecity-qb8b592cd8xc5wyaiscgzr.streamlit.app/)

## 功能亮点

- 16:9 深色科技生命展示平台，玻璃面板、发光边框和动态粒子效果
- 外部环境、分子机制、细胞功能三级数字孪生结构
- 氧气、葡萄糖、温度、毒素四项环境参数实时控制
- 正常细胞、缺氧挑战、毒素攻击三种一键实验
- ATP、ROS、DNA 修复、蛋白质合成和细胞器健康联动推演
- 葡萄糖 → 糖酵解 → 三羧酸循环 → 电子传递链 → ATP 的动态代谢网络
- 缺氧、毒素、底物短缺和温度应激生命事件，可并发触发
- “环境变化 → 分子机制 → 细胞响应”实时因果链解释
- 线粒体亮度、ATP 粒子速度与代谢效率同步变化
- 无需 API 的规则型“AI 生命助手”，支持常见科普提问
- Plotly 实时趋势图和动态健康仪表盘
- 图片自动压缩为 WebP 并缓存，兼顾公网加载速度与高清展示
- 图片资源缺失时自动生成占位图，避免程序启动失败

## 快速运行

建议使用 Python 3.10 或更高版本。

```powershell
cd LifeCity
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m streamlit run app.py
```

浏览器通常会自动打开 `http://localhost:8501`。建议使用 1920×1080 分辨率与浏览器全屏模式获得最佳展示效果。

Linux / macOS：

```bash
cd LifeCity
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m streamlit run app.py
```

## 公网部署

项目已按 Streamlit Community Cloud 标准整理，无需数据库、外部 API 或系统级依赖。

1. 将整个 `LifeCity` 目录推送到 GitHub 公共仓库。
2. 登录 [Streamlit Community Cloud](https://share.streamlit.io/)。
3. 选择仓库、分支 `main`，入口文件填写 `app.py`。
4. 点击 Deploy。平台会自动读取 `requirements.txt` 与 `.streamlit/config.toml`。

部署前可执行以下检查：

```powershell
python -m compileall -q app.py modules
python -m streamlit run app.py --server.headless true
```

## 项目结构

```text
LifeCity/
├── app.py                     # Streamlit 主程序与驾驶舱布局
├── ui_preview.py              # 独立静态 UI 预览，不参与主程序逻辑
├── modules/
│   ├── metabolism.py          # ATP 与健康指数数学模型
│   ├── cell_model.py          # 细胞城市动态视图和资源回退
│   ├── experiment.py          # 实验预设
│   ├── life_events.py         # 动态生命事件与因果链
│   └── ai_assistant.py        # 规则型科普助手
├── assets/
│   ├── cell_city.png          # 中央细胞城市主视觉
│   ├── mitochondria.png       # 线粒体素材
│   ├── dna.png                # DNA 素材
│   ├── style.css              # HUD 视觉主题
│   └── icons/                 # 矢量功能图标
├── requirements.txt
├── .streamlit/
│   └── config.toml            # 公网部署主题与无头服务配置
├── .gitignore
└── README.md
```

## 模型说明

本项目用于生命机制科普，不用于科研定量计算或医疗诊断。

基础 ATP 效率：

```text
ATP效率 = 葡萄糖比例 × 氧气比例 × 温度系数 × 毒素修正 × 100
```

温度系数在 37℃ 附近达到最大；偏离越远，模拟酶活性越低。健康指数按以下权重合成：

```text
Health = 0.4 × ATP状态 + 0.3 × DNA稳定性 + 0.3 × 代谢平衡
```

- 90–100：健康稳定
- 60–90：压力状态
- 0–60：危险状态

代谢网络中的葡萄糖、糖酵解、三羧酸循环、电子传递链和 ATP 节点会分别计算 0–100% 通量，并按“活跃、受压、受阻”着色。毒素与缺氧还会影响 ROS、DNA 修复活性、蛋白质合成以及线粒体、核糖体和细胞膜状态。

## 展示建议

1. 从“正常细胞”开始讲解细胞城市的四个功能区。
2. 点击“缺氧挑战”，观察线粒体变暗、ATP 下跌和助手解释。
3. 点击“毒素攻击”，对比 DNA 稳定性和健康曲线。
4. 手动恢复氧气、温度与毒素参数，演示数字孪生的实时反馈。

## 素材说明

主视觉和器官素材为本项目生成的原创 AI 视觉资产。资源通过项目相对路径加载，兼容 Windows 与 Linux；主视觉在首次读取时会压缩为 WebP，后续访问复用 Streamlit 缓存。代码中保留了资源缺失回退逻辑；如需替换，只要保持文件名不变即可。

