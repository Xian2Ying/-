# -*- coding: utf-8 -*-
"""
对外入口收敛（ADR-002 方案 A）：
  - index.html          → 对外唯一入口：只有「正式版 v1.1」一个开始按钮
  - index.internal.html → 内部/答辩用：保留 8 版本总览，并标注「内部实验版」
不改动任何游戏文件。

幂等：index.internal.html 只在不存在时生成（避免覆盖人工改动）。
"""
import io, os, sys

LAB = "C:/Users/XIAN&YING/WorkBuddy/2026-10-31-22-18-46/word-quest-lab"
INDEX = os.path.join(LAB, "index.html")
INTERNAL = os.path.join(LAB, "index.internal.html")
JUDGE = os.path.join(LAB, "judge.html")
ROGUE = os.path.join(LAB, "roguelike.v2.html")

PUBLIC = """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>词勇者 · Word Quest</title>
<style>
:root{--bg:#15121f;--panel:#262038;--gold:#f4c75b;--txt:#f3eefb;--dim:#a89fc0;--line:#3a3358;}
*{box-sizing:border-box;}
body{margin:0;background:radial-gradient(circle at 50% 0%,#241d39,#15121f 70%);color:var(--txt);
 font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;min-height:100vh;
 display:flex;align-items:center;justify-content:center;padding:22px 16px 40px;}
.wrap{max-width:520px;width:100%;text-align:center;}
.hero{font-size:54px;line-height:1;margin-bottom:10px;}
h1{font-size:30px;margin:0 0 6px;letter-spacing:2px;}
.sub{color:var(--dim);font-size:14px;line-height:1.8;margin-bottom:24px;}
.play{display:block;background:var(--gold);color:#241f0b;font-weight:800;font-size:19px;
 border-radius:14px;padding:18px;text-decoration:none;letter-spacing:1px;box-shadow:0 6px 0 #8a6d18;}
.play:active{transform:translateY(3px);box-shadow:0 3px 0 #8a6d18;}
.meta{margin-top:16px;color:var(--dim);font-size:12px;line-height:2;}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px;
 margin-top:22px;text-align:left;font-size:13px;line-height:1.9;color:var(--txt);}
.card b{color:var(--gold);}
.mini{display:none;margin-top:28px;font-size:12px;color:var(--dim);}
.mini a{color:var(--dim);}
</style></head><body>
<div class="wrap">
  <div class="hero">⚔️</div>
  <h1>词勇者</h1>
  <div class="sub">Word Quest · 打怪就是背词<br>100 个四级高频词 · 3 关闯关 · 每道题都有例句卡</div>
  <a class="play" href="game.v3.html" id="start">▶ 开始游戏</a>
  <div class="meta">手机 / 电脑浏览器打开即玩 · 进度存在本机</div>
  <div class="card">
    <b>这一版新增</b>：答对答错都弹出「释义 + 中英例句」例句卡；<br>
    看词选义题也能点 🔊 听发音；答错多停留一会儿并给一句提示。
  </div>
  <div class="mini" id="mini">内部实验版本（8 版本 A/B 对照，答辩用）→ <a href="index.internal.html">打开</a></div>
</div>
<script>
(function(){
  if(/(^|[?&])internal=1(&|$)/.test(location.search)){ var m=document.getElementById('mini'); if(m) m.style.display='block'; }
  var q=(location.search||"").match(/[?&]sharecode=[^&]*/);
  if(!q) return;
  var v=q[0].replace(/^[?&]/,"");
  Array.prototype.forEach.call(document.querySelectorAll("a[href]"),function(a){
    var h=a.getAttribute("href")||"";
    if(!h||/^(https?:|#|mailto:|javascript:|data:)/.test(h)) return;
    if(h.indexOf("sharecode=")!==-1) return;
    a.setAttribute("href", h+(h.indexOf("?")===-1?"?":"&")+v);
  });
})();
</script>
</body></html>
"""

CARD_OLD = """  <a class="card" data-play href="game.html">
    <div class="top"><span class="name">🏆 词勇者 主游戏</span><span class="badge b-game">正式版 v1.0</span></div>
    <div class="file">game.html</div>
    <div class="desc">完整版：首页 / 3 关地图 / 3 种题型 / 结算 / 错题本 / 设置，100 词真实词库，本地真人发音 mp3，localStorage 存档。</div>
    <div class="test"><b>测试要点：</b>整条闯关流程是否顺、答错进错题本、🔊 发音是否出声（设置页还有「声音自检」）。</div>
    <span class="go">▶ 打开正式版</span>
  </a>"""

CARD_NEW = """  <a class="card" data-play href="game.v3.html">
    <div class="top"><span class="name">🏆 词勇者 主游戏</span><span class="badge b-game">正式版 v1.1</span></div>
    <div class="file">game.v3.html（对外入口）</div>
    <div class="desc">完整版 + 例句卡：答对答错都展示「释义 + 中英例句」，T1 看词选义补 🔊 喇叭，答错延长停留并给提示。100 词真实词库、本地发音、localStorage 存档。</div>
    <div class="test"><b>测试要点：</b>每道题答完是否弹出例句卡、看词选义能否点喇叭、答错停留是否够看清例句。</div>
    <span class="go">▶ 打开正式版 v1.1</span>
  </a>
  <a class="card" data-play href="game.html">
    <div class="top"><span class="name">🏆 词勇者 主游戏 v1.0</span><span class="badge b-ctl">冻结对照</span></div>
    <div class="file">game.html</div>
    <div class="desc">v1.0 原件（A/B 基准，全程未改）：只有颜色闪烁反馈、无例句卡、T1 无喇叭。用来对照 v1.1 的「学会感」提升。</div>
    <div class="test"><b>测试要点：</b>与 v1.1 对比答完题的信息量差异。</div>
    <span class="go">▶ 打开 v1.0 对照</span>
  </a>"""

LEGEND_OLD = '  <div class="li"><span class="badge b-game">正式版 v1.0</span> 主游戏（完整版）</div>'
LEGEND_NEW = ('  <div class="li"><span class="badge b-game">正式版 v1.1</span> 对外唯一入口（game.v3.html）</div>\n'
              '  <div class="li"><span class="badge b-ctl">v1.0 冻结</span> 旧主游戏，A/B 对照</div>')

BANNER = ('<div class="tips" style="border-left-color:#9ff0bf"><b>🔒 内部实验版总览</b> —— 对外请只发正式版入口（index.html → game.v3.html）。'
          '本页保留 8 个版本与 A/B 对照，供答辩与内部复盘使用。</div>')


# ---------------------------------------------------------------------------
# 评委专用版（ADR-006）：judge.html + 地狱模式演示直进
#   - 普通版 index.html 保持零改动，沿用原分享链接
#   - 评委版独立入口 judge.html，共用同一套游戏文件（不复制本体）
#   - ?demo=hell 仅注入部署副本，仓库 src/proto 对照原件不注入
# ---------------------------------------------------------------------------

JUDGE_HTML = """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>词勇者 · 评委演示版</title>
<style>
:root{--bg:#15121f;--panel:#262038;--gold:#f4c75b;--txt:#f3eefb;--dim:#a89fc0;--line:#3a3358;--hell:#a83232;}
*{box-sizing:border-box;}
body{margin:0;background:radial-gradient(circle at 50% 0%,#2a1d3d,#15121f 70%);color:var(--txt);
 font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;min-height:100vh;padding:24px 16px 48px;}
.wrap{max-width:600px;margin:0 auto;}
.kicker{display:inline-block;font-size:11px;font-weight:800;letter-spacing:1px;color:#241f0b;
 background:var(--gold);padding:4px 10px;border-radius:20px;margin-bottom:14px;}
h1{font-size:30px;margin:0 0 8px;letter-spacing:2px;}
.sub{color:var(--dim);font-size:13px;line-height:1.9;margin-bottom:22px;}
.card{display:block;background:var(--panel);border:1px solid var(--line);border-radius:14px;
 padding:16px 18px;margin:12px 0;text-decoration:none;color:var(--txt);transition:transform .12s;}
.card:active{transform:translateY(2px);}
.card.main{border-color:var(--gold);}
.card.hell{border-color:var(--hell);background:#2a1620;}
.card .t{font-size:18px;font-weight:800;margin-bottom:6px;}
.card .d{font-size:13px;line-height:1.85;color:var(--dim);}
.card .go{display:inline-block;margin-top:10px;font-size:14px;font-weight:800;color:var(--gold);}
.card.hell .go{color:#ff9a9a;}
.card .step{float:right;font-size:11px;color:var(--dim);font-weight:700;}
.tips{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--gold);
 border-radius:10px;padding:14px 16px;margin-top:24px;font-size:13px;line-height:2;text-align:left;}
.tips b{color:var(--gold);}
.tips ol{margin:8px 0 0;padding-left:20px;}
.tips li{margin:4px 0;}
.foot{margin-top:24px;font-size:12px;color:var(--dim);line-height:2;text-align:center;}
.foot a{color:var(--dim);}
</style></head><body>
<div class="wrap">
  <div class="kicker">评委演示专用 · 含演示直进参数</div>
  <h1>⚔️ 词勇者 · Word Quest</h1>
  <div class="sub">背词 × 闯关 × 肉鸽 · 校园 AI 智能体创新应用大赛（AI+教学科研方向）<br>
  一句话定位：<b style="color:var(--gold)">游戏是壳、AI 是核</b></div>

  <a class="card main" href="game.v3.html">
    <div class="t">🏆 正式版 v1.1 · 完整体验 <span class="step">STEP 1</span></div>
    <div class="d">3 关线性地图 · 100 个四级高频词真实词库 · 每道题答完弹出「释义 + 中英例句」例句卡 ·
    错题本「答对 2 次毕业」 · 本地真人发音 mp3。这是产品主形态，请先答两题。</div>
    <span class="go">▶ 打开正式版</span>
  </a>

  <a class="card hell" href="roguelike.v2.html?demo=hell">
    <div class="t">💀 地狱模式 · 一键直进 <span class="step">STEP 2 · 记忆点</span></div>
    <div class="d">跳过「通关 75 关才解锁」的门槛，直接进地狱档：60 层、每 10 层 Boss、四幕 I~IV；
    HP / 永久死亡 / 三选一天赋 / 记忆碎片 / 应援角色反馈。<b>「背词 × 肉鸽」是本作品最大亮点。</b></div>
    <span class="go">💀 直进地狱档</span>
  </a>

  <a class="card ab" href="index.internal.html">
    <div class="t">🧪 A/B 方法论与版本演进 <span class="step">STEP 3 · 答辩投屏</span></div>
    <div class="d">8 个版本贴好标签（v0 初始演示 / 对照组·冻结 / v2 实验组 / 正式版 v1.1）。
    讲「原文件冻结作对照、改动另起新文件」的可控演进方法，以及治疗组 / 对照组 / 创新组三组对照。</div>
    <span class="go">🧪 打开版本总览</span>
  </a>

  <div class="tips">
    <b>建议演示顺序</b>
    <ol>
      <li><b>3 分钟版</b>：正式版答 2 题（看例句卡与答错停留）→ 地狱模式看 60 层 / Boss / 永久死亡 → 投屏 A/B 页讲方法论。</li>
      <li><b>完整版（约 8 分钟）</b>：再加错题本「答对 2 次毕业」、🔊 发音与设置页声音自检、v1.0 冻结版对照。</li>
      <li><b>收尾一句话</b>：错题本把「答对 2 次」变成毕业条件，肉鸽把「背词」变成有代价的闯关——学习动机由玩法承担。</li>
    </ol>
  </div>

  <div class="foot">
    本页仅供评委演示：地狱模式链接带 <code>demo=hell</code> 演示参数，常态试玩请用
    <a href="index.html">普通版入口</a>。<br>进度存在本机浏览器 · 手机 / 电脑浏览器打开即玩
  </div>
</div>
<script>
(function(){
  var q=(location.search||"").match(/[?&]sharecode=[^&]*/);
  if(!q) return;
  var v=q[0].replace(/^[?&]/,"");
  Array.prototype.forEach.call(document.querySelectorAll("a[href]"),function(a){
    var h=a.getAttribute("href")||"";
    if(!h||/^(https?:|#|mailto:|javascript:|data:)/.test(h)) return;
    if(h.indexOf("sharecode=")!==-1) return;
    a.setAttribute("href", h+(h.indexOf("?")===-1?"?":"&")+v);
  });
})();
</script>
</body></html>
"""

DEMO_MARK = "WQ_DEMO_PATCH"
DEMO_ANCHOR = "tierSelect();\n</script>"
DEMO_CODE = """/* WQ_DEMO_PATCH: 评委演示直进地狱档（幂等，仅作用于部署副本；仓库 src/proto 对照原件不注入） */
if(/(^|[?&])demo=hell(&|$)/.test(location.search)){
  META.unlocked=3; S.tierIdx=3; applyTheme(TIERS[3]); showBanner(TIERS[3]); startRun('tank');
}else{ tierSelect(); }
</script>"""


def build_judge():
    io.open(JUDGE, "w", encoding="utf-8", newline="\n").write(JUDGE_HTML)
    print("WROTE judge:", JUDGE)


def inject_demo():
    s = io.open(ROGUE, encoding="utf-8").read()
    if DEMO_MARK in s:
        print("SKIP demo (already injected):", ROGUE)
        return
    if DEMO_ANCHOR not in s:
        raise SystemExit("ANCHOR NOT FOUND: " + repr(DEMO_ANCHOR))
    io.open(ROGUE, "w", encoding="utf-8", newline="\n").write(
        s.replace(DEMO_ANCHOR, DEMO_CODE, 1))
    print("INJECT demo:", ROGUE)


def main():
    # --judge-only：只生成评委版 + 注入演示参数，绝不重写普通版 index.html
    if "--judge-only" in sys.argv:
        build_judge()
        inject_demo()
        return
    s = io.open(INDEX, encoding="utf-8").read()

    if not os.path.exists(INTERNAL):
        t = s
        for old, new, label in [
            (CARD_OLD, CARD_NEW, "正式版卡片"),
            (LEGEND_OLD, LEGEND_NEW, "图例"),
            ('最后开 <b>🏆 正式版 v1.0</b>', '最后开 <b>🏆 正式版 v1.1</b>', "建议顺序"),
            ('<code>正式版 v1.0</code> = 当前主游戏', '<code>正式版 v1.1</code> = 当前主游戏', "图例脚注"),
            ('<h1>⚔️ 词勇者 · 全版本标签总览</h1>', '<h1>⚔️ 词勇者 · 全版本标签总览</h1>\n' + BANNER, "横幅"),
            ('<div class="sec">🏆 A. 正式版（当前主游戏）</div>', '<div class="sec">🏆 A. 正式版（当前主游戏 · 对外入口 game.v3.html）</div>', "小节标题"),
        ]:
            if old not in t:
                raise SystemExit("ANCHOR NOT FOUND: " + label)
            t = t.replace(old, new, 1)
        t = t.replace("词勇者 / Word Quest · 校园 AI 智能体创新应用大赛 · 赛前测试版",
                      "词勇者 / Word Quest · 校园 AI 智能体创新应用大赛 · 内部实验版（勿对外发送）", 1)
        io.open(INTERNAL, "w", encoding="utf-8", newline="\n").write(t)
        print("WROTE internal:", INTERNAL)
    else:
        print("SKIP internal (exists):", INTERNAL)

    io.open(INDEX, "w", encoding="utf-8", newline="\n").write(PUBLIC)
    print("WROTE public index:", INDEX)

    build_judge()
    inject_demo()


if __name__ == "__main__":
    main()
