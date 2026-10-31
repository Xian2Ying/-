# word-quest（工作名）· 像素闯关英语学习游戏

> 第一届校园 AI 智能体创新应用大赛参赛作品 · AI+教学科研方向

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

1. **最省事**：双击 `src/index.html`，浏览器直接打开就能玩（词库已内联，断网也能玩）。
2. **手机测玩**：把 `src/index.html` 发到微信/QQ 传给手机，用浏览器打开；或等 AI 部署成链接。
3. **改了词库之后**：内容官改完 `src/data/words.json`，在仓库根目录跑一次
   ```bash
   python tools/build.py     # 把 JSON 注入 index.html
   python tools/smoke.py     # 自动点一遍，自检有没有跑崩
   ```

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
