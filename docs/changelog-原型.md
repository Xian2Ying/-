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

## 2026-11-08 17:xx · v3 最小上场包（P0 四项落地）

- **修复 v2 发音链路**（`tools\build_v2.py` 重写 `AUDIO_JS`，重新生成三个 `.v2.html`）
  - 根因：`voiceFor()` 的 `onerror` 换源到在线 TTS 后只 `a.src=nx; return;`，没有重新 `play()` → 在线音「只加载不播放」、第一击无声
  - 修法：换源后补 `play()`；新增 `noLocal{}` 记忆本地缺失词；stage≥2 直接合成音
  - 验证（headless）：点击 🔊 后 stage 0→1、`play()` 调用 2 次、网络出现 youdao 请求
- **修复 battle-v2 串台文案**：标题/横幅/难度菜单从「对照组·平铺基线」改为「词怪战斗」；DOM 内「对照组」字样 0 次
- **新增 `src\proto\game.v3.html`**（由 `tools\build_v3.py` 从冻结的 `src\index.html` 生成）
  - 例句卡（100 词 `example`/`exampleZh` 现成数据）、答错停留 850→2600ms + 提示、T1 看词选义补 🔊、发音换源修复
  - 验证（headless 真实点击 10 题）：10/10 弹例句卡，T1 `spk1=true`，答对答错都有卡，正常到结算
- **对外入口收敛**（`tools\build_lab.py`）：`word-quest-lab\index.html` 改为单一正式版入口 → `game.v3.html`；
  旧 8 版本总览改为 `index.internal.html`（内部/答辩用，`&internal=1` 显示入口）
- 新增 `docs\19-执行记录-v3最小上场包.md`（改动清单 / 验证证据 / 发布步骤 / 回滚）
- **对照组 `src\index.html`、`game.html` 全程零改动**

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

## 2026-11-08 · 评委专用版 / 普通版双入口（ADR-006，队长拍板「精编演示版」）

- **决策**：普通版 `index.html` 保持零改动、沿用原分享链接；评委版另起独立入口 `judge.html`，两者共用同一套游戏文件（不复制本体）。评委版不做成 8 版本陈列，遵循 DSH「对外只留一条主路径」建议。
- **新增文件**：`C:/Users/XIAN&YING/WorkBuddy/2026-10-31-22-18-46/word-quest-lab/judge.html`
  三张卡（正式版 v1.1 / 💀 地狱模式一键直进 / A-B 方法论答辩页）+ 3 分钟与 8 分钟演示话术 + sharecode 透传脚本。
- **修改文件**：`C:/Users/XIAN&YING/WorkBuddy/2026-10-31-22-18-46/word-quest/tools/build_lab.py`
  新增 `JUDGE_HTML`、`build_judge()`、`inject_demo()`、`--judge-only` 开关；完整构建路径末尾也会生成评委版，保证可复现。
- **注入（仅部署副本）**：`C:/Users/XIAN&YING/WorkBuddy/2026-10-31-22-18-46/word-quest-lab/roguelike.v2.html`
  追加 `WQ_DEMO_PATCH`：`?demo=hell` 时 `META.unlocked=3` + `S.tierIdx=3` + `startRun('tank')`，跳过「通关 75 关才解锁」直进地狱档；幂等。仓库 `src/proto/roguelike.v2.html` 对照原件**不注入**。
- **零改动证明**：`word-quest-lab/index.html` 执行前后 sha256 均为 `01a0ba708369ba472e5d6fb493eec18b0ca6b868d9e5e9719db0f76e135d78c6`；`src/index.html`、`src/proto/*`、`src/audio/*` 全程未动。
- **本地验证（无头浏览器 4 场景全绿，零 JS 报错）**：评委版 4 个链接均拼上 sharecode；`?demo=hell` 直达「💀 地狱 难度 · 层 1/60 · 地狱I」第 1 层战斗且难度按钮数 0；不带 demo 仍是四档菜单（4 个按钮）；评委版截图排版无重叠。
- **线上状态**：改动尚未发布。重新部署后普通版仍为 `https://word-quest-60356.app.workbuddy.host/?sharecode=YMRKAOKJ7P`，评委版为 `https://word-quest-60356.app.workbuddy.host/judge.html?sharecode=YMRKAOKJ7P`。

## 2026-11-11 22:45 · 评委版发布上线（ADR-006 收尾）

- **授权**：队长「评委版也发来给我拿去测」→ 按需要公网可转发链接理解为发布授权。
- **动作**：重新发布 `C:/Users/XIAN&YING/WorkBuddy/2026-10-31-22-18-46/word-quest-lab`（静态站，entry `index.html`），沿用原应用与分享码，**普通版链接完全不变**。
- **线上前后对比**：
  - `judge.html`：404 / 335B → **200 / 5,015B**
  - `roguelike.v2.html`：121,302B 无注入 → **121,586B，`WQ_DEMO_PATCH` 在位**
  - 根 `index.html`：发布前后线上 sha256 = 本地 sha256 = `01a0ba708369ba472e5d…`（零改动）
- **线上实测（无头浏览器，剥离 script 后判定可见渲染）**：
  - 评委版 4 个子链接全部自动拼上 `sharecode`（含 `?demo=hell&sharecode=…`）
  - `?demo=hell` 真实渲染「💀 地狱 难度 終幕·最終公演 ❤❤❤❤❤ 层 1/60 · 地狱I」，**直接进第 1 层战斗、无难度菜单**
  - 不带 `demo` 仍是正常四档菜单（简单/普通/困难/地狱，后三档锁定），常态未被破坏
  - `audio/abandon.mp3` 200 / 11,757B；其余 8 个版本页保持 200
- **文档状态更新**：`docs/20-交付检查清单.md` 阻断项改为「已解决」、风险表移除「评委版未上线」；`docs/22-体验测试指引-可转发.md` 补评委版链接与 STEP 2 测试项。
- **仍未验证**：手机真机 🔊 发音（沙箱无声，需队长真机点一次）。
