# word-quest（工作名）· 像素闯关英语学习游戏

> 第一届校园 AI 智能体创新应用大赛参赛作品 · AI+教学科研方向

## 🎮 立即试玩（三选一）

1. **手机**：微信扫一扫根目录的 [扫码开始游戏.png](https://github.com/Xian2Ying/-/raw/main/扫码开始游戏.png)，
   或直接打开 → **https://word-quest-60356.app.workbuddy.host/?sharecode=YMRKAOKJ7P&v=013**
2. **电脑**：双击根目录的 **开始游戏.url**（用浏览器打开线上版）；或双击 `src/index.html`（离线可玩）。
3. 队友测玩时请用线上链接，这样大家玩的都是最新版。

用像素闯关游戏的方式学英语：单词靠闯关反复练（艾宾浩斯间隔重复），口语和 AI 聊着练。**移动端 H5 优先**，6-30 岁人群。

## 文档导航

> 以下为 GitHub 绝对链接，任何设备/软件打开都能点开。

- [AGENTS.md](https://github.com/Xian2Ying/-/blob/main/AGENTS.md) — AI 协作规范与项目背景（所有 AI 必读，共享上下文）
- [CONTRIBUTING.md](https://github.com/Xian2Ying/-/blob/main/CONTRIBUTING.md) — **队友必看**：git 协作流程、日常三步曲、谁碰什么文件、冲突怎么办
- [docs/00-项目章程.md](https://github.com/Xian2Ying/-/blob/main/docs/00-项目章程.md) — 命题理解、痛点、目标与价值
- [docs/01-功能拆解-draft.md](https://github.com/Xian2Ying/-/blob/main/docs/01-功能拆解-draft.md) — 玩法循环与功能模块（草稿）
- [docs/02-待拍板问题.md](https://github.com/Xian2Ying/-/blob/main/docs/02-待拍板问题.md) — 需要团队确认的问题清单
- [docs/03-决策结论.md](https://github.com/Xian2Ying/-/blob/main/docs/03-决策结论.md) — 客观约束分析与八项选择（历史底稿）
- [docs/04-方案选型决策.md](https://github.com/Xian2Ying/-/blob/main/docs/04-方案选型决策.md) — **当前执行依据**：对话式 AI vs 小游戏选型、MVP 范围、时间表、降级预案
- [docs/06-技术方案.md](https://github.com/Xian2Ying/-/blob/main/docs/06-技术方案.md) — 移动端优先 + 双端数据互通技术方案
- [docs/07-组长作战手册.md](https://github.com/Xian2Ying/-/blob/main/docs/07-组长作战手册.md) — 零经验三人队四周作战表
- [docs/08-分工与责任表.md](https://github.com/Xian2Ying/-/blob/main/docs/08-分工与责任表.md) — **三人分工**：角色定位、责任清单、时间轴交付、协作红线
- [docs/09-任务计划-内容官A.html](https://github.com/Xian2Ying/-/blob/main/docs/09-任务计划-内容官A.html) — **队友 A 稳定打开版（单文件 HTML）**：逐日任务 + 100 词预分 3 关（配套 [.md 版](https://github.com/Xian2Ying/-/blob/main/docs/09-任务计划-内容官A.md)）
- [docs/10-任务计划-体验官B.md](https://github.com/Xian2Ying/-/blob/main/docs/10-任务计划-体验官B.md) — 队友 B 逐日任务（手机测玩 + 截图 + 测试记录表）
- [docs/11-任务计划-组长.md](https://github.com/Xian2Ying/-/blob/main/docs/11-任务计划-组长.md) — 组长行动清单与即时下一步

## 跑起来（三种方式，任选）

0. **手机直接玩（最新版在线链接）**：https://word-quest-60356.app.workbuddy.host/?sharecode=YMRKAOKJ7P
   —— 发到微信/QQ 里点开即可，体验官 B 用这个测。
1. **最省事**：双击 `src/index.html`，浏览器直接打开就能玩（词库已内联，断网也能玩；**发音也离线可用**）。
2. **手机测玩**：把 `src` 整个文件夹发到微信/QQ 传给手机，用浏览器打开 `index.html`；或直接用上面的在线链接。
   ⚠️ 只发 `index.html` 一个文件的话单词没声音——发音音频在同目录 `audio/` 里。
3. **改了词库之后**：内容官改完 `src/data/words.json`，在仓库根目录跑一次
   ```bash
   python tools/build.py        # 把 JSON 注入 index.html
   python tools/fetch_audio.py  # 补齐新词的发音 mp3（已有的会跳过）
   python tools/smoke.py        # 自动点一遍，自检有没有跑崩
   ```

## 发音为什么不用浏览器自带语音

手机端（微信内置浏览器、iOS Safari）的 `speechSynthesis` 经常静默失效，听起来就是「完全没声音」。
所以 100 个词的真人发音已提前下载到 `src/audio/<单词>.mp3`（共约 1.2 MB，平均 12 KB/词），游戏直接播本地文件：
无延迟、离线可用、跨机型一致。万一某个文件缺失，会自动退回在线发音接口，再不行才用设备合成音。

> 音频来自公开词典发音接口，仅用于本参赛作品的教学演示。词库改动后跑 `python tools/fetch_audio.py` 补齐即可。

## 当前状态

**已报名** ✅；游戏名暂定「词勇者」；100 词词库已交付并转为 `src/data/words.json`；**第一版游戏已能玩**（首页 / 地图 / 3 种题型答题 / 结算 / 错题本 / 设置，进度存本机）。
待办：AI 口语 NPC（P1）、艾宾浩斯完整调度（P1）、PC 端布局优化、美术素材替换。
报名截止 11-13（已完成），开发冻结 11-24，赛程结束 11-28。

## 团队

3 人，全部零编码经验，代码由 AI 承担：
- 🧭 组长（你）：拍板 / 守范围 / 验收 / 对外 / 写交付物
- 📚 队友 A（内容官）：词库 / 释义 / 题目 / 校对
- 🔍 队友 B（体验官）：手机测玩 / 找 bug / 提体验
- 🤖 AI（WorkBuddy）：写代码 / 调研 / PRD / 原型 / 素材 / PPT / 视频

详见 [docs/08-分工与责任表.md](https://github.com/Xian2Ying/-/blob/main/docs/08-分工与责任表.md)。
