# 文件修改跟踪记录（原型阶段）

> 规则：原始游戏 `C:\Users\XIAN&YING\WorkBuddy\2026-10-31-22-18-46\word-quest\src\index.html` **全程不改**，作为对照组。
> 所有新内容放在 `src\proto\` 与 `docs\` 下的新文件，逐条记录绝对路径。
> 状态：模板待评审。队长判定「好→采用 / 不好→再改」后再决定是否并入主游戏。

---

## 2026-11-03 23:xx · 版本标签（Git 里程碑）

- 新建 `src\proto\index.compare.html`（升级为「版本标签总览」，v0/对照组/v2 三色徽章 + 角色定位）
- 更新 `docs\16-版本比对-对照组vs实验组.md`：新增「一-B 版本标签矩阵」「八 Git 版本标签」
- 提交 `5011c22`，打三个本地标签：`v0-initial-demo` / `v1-control-baseline` / `v2-experimental`（未推送远程）
- 清理 `src\proto\*.test.html` 测试垃圾文件

---

## 2026-11-04 20:xx · 全版本测试站（找人测试交付）

- 新建独立目录 `C:\Users\XIAN&YING\WorkBuddy\2026-10-31-22-18-46\word-quest-lab\`（**不进 git**，独立部署）
  - `index.html`：全版本标签总览入口，覆盖 9 个可玩页，四组分区 + 建议测试顺序 + sharecode 透传
  - `game.html`（复制 `src\index.html`，原件未改）+ `audio\*.mp3`（100 个）
  - 6 个原型副本 + `hub.html`（复制 `src\proto\index.html` 并改名）
  - 8 个游戏页注入 `WQ_SHARE_PATCH` 幂等脚本（防平台把子页面拦成占位页）
- 新建 `tools\inject_sharecode.py`（幂等注入工具，可复现）
- 新建 `docs\17-全版本测试站交付.md`（链接 / 9 版本标签 / 修改记录 / 线上验证）
- 部署：`https://word-quest-60356.app.workbuddy.host/?sharecode=YMRKAOKJ7P`
  - ⚠️ 平台将其并入**原正式版同一应用**，旧链接落地页由「直接进游戏」变为「全版本总览」；正式版仍可经 `game.html` 访问；旧 `wordquest-proto` 实验站未受影响
- 验证：9 页 HTTP 200 均为真实内容；`audio/abandon.mp3` 200/11757B；8/8 链接透传 sharecode；9 页零 JS 报错
- **对照组原件 `src\index.html`、`src\proto\*.html`、`src\audio\*` 全部零改动**

---

## 2026-11-02 20:27 · 创建战斗原型模板

- 新建 `C:\Users\XIAN&YING\WorkBuddy\2026-10-31-22-18-46\word-quest\src\proto\battle-template.html`
  - 类型：单文件、零依赖、双击即开（无需 build、无需联网）
  - 演示内容：把 GDD 评审图 1（词=怪机制映射）与图 2（每题 Juice 循环）落地为可玩原型
  - 已实现：
    - 怪物拟人身份（abandon→遗弃怪 / vulnerable→脆脆怪 / efficient→疾风怪）+ 台词气泡
    - 答对：怪物被击退（下沉缩小消失）+ 绿框闪烁 + 🔥连击计数 + WebAudio 清脆音
    - 答错：怪物反击抖动 + 红框闪烁 + 低频音，**不中断流程**，并标出正确答案（✓）
    - 无障碍：对错除红/绿配色外，额外加 ✓ / ✗ 图标与形状，避免色盲误判
  - 数据：内联 3 个演示词，**非真实词库**（合并时需替换为 words.json 抽题）
  - 对照：原始 index.html 未读取、未修改

- 新建 `C:\Users\XIAN&YING\WorkBuddy\2026-10-31-22-18-46\word-quest\docs\changelog-原型.md`
  - 本文件，全程跟踪所有原型相关改动

---

## 待补充（采用后）

- [ ] 队长评审结论：采用 / 再改
- [ ] 若采用：把怪物机制与 Juice 并入 `src\index.html`（保留原件为对照，新版本另存或加版本号）
- [ ] 替换内联演示词为 words.json 真实抽题 + 干扰项
- [ ] 发音改为本地 mp3（沿用主游戏已验证方案，避免手机无声旧坑）
