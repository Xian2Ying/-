# -*- coding: utf-8 -*-
"""
对外入口收敛（ADR-002 方案 A）：
  - index.html          → 对外唯一入口：只有「正式版 v1.1」一个开始按钮
  - index.internal.html → 内部/答辩用：保留 8 版本总览，并标注「内部实验版」
不改动任何游戏文件。

幂等：index.internal.html 只在不存在时生成（避免覆盖人工改动）。
"""
import io, os

LAB = "C:/Users/XIAN&YING/WorkBuddy/2026-10-31-22-18-46/word-quest-lab"
INDEX = os.path.join(LAB, "index.html")
INTERNAL = os.path.join(LAB, "index.internal.html")

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


def main():
    s = io.open(INDEX, encoding="utf-8").read()

    if not os.path.exists(INTERNAL):
        t = s
        for old, new, label in [
            (CARD_OLD, CARD_NEW, "正式版卡片"),
            (LEGEND_OLD, LEGEND_NEW, "图例"),
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


if __name__ == "__main__":
    main()
