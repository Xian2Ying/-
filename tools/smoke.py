#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
冒烟自检：用无头 Edge 打开 index.html，自动点一遍「开始冒险 → 第 1 关 → 答第 1 题 → 进入第 2 题」，
把走过的页面和状态打印出来。零经验队友也能跑：

  python tools/smoke.py

期望输出包含：SMOKE:s-home>s-map>s-quiz>s-quiz，且 idx 是「第 2/10 题」。
"""
import io
import os
import re
import subprocess
import sys

try:
    from html import unescape
except ImportError:                      # py2 兜底
    from HTMLParser import HTMLParser
    unescape = HTMLParser().unescape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src", "index.html")
TMP = os.path.join(ROOT, "src", "_smoke.html")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

DRIVER = """
<script>
var log = [];
function step(){ var on = document.querySelector(".screen.on"); log.push(on ? on.id : "none"); }
window.onerror = function(e){ document.title = "JSERROR:" + e; };
setTimeout(function(){
  step();
  document.getElementById("btn-start").click();
  setTimeout(function(){
    step();
    document.querySelectorAll("#nodes .node")[0].click();
    setTimeout(function(){
      step();
      var opts = document.querySelectorAll("#opts .opt");
      var inp = document.getElementById("sp");
      if(opts.length){ opts[0].click(); }
      else if(inp){ inp.value = "abandon"; document.getElementById("ok").click(); }
      setTimeout(function(){
        step();
        var idx = document.getElementById("q-idx");
        document.title = "SMOKE:" + log.join(">") + "|idx=" + (idx ? idx.textContent : "-");
      }, 1600);
    }, 600);
  }, 600);
}, 400);
</script>
"""


def main():
    if not os.path.exists(EDGE):
        print("没找到 Edge，跳过浏览器自检")
        return 1
    html = io.open(SRC, encoding="utf-8").read()
    io.open(TMP, "w", encoding="utf-8").write(html.replace("</body>", DRIVER + "</body>"))
    try:
        out = subprocess.run(
            [EDGE, "--headless=new", "--disable-gpu", "--virtual-time-budget=9000",
             "--dump-dom", "file:///" + TMP.replace("\\", "/")],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=90
        ).stdout.decode("utf-8", "ignore")
    finally:
        if os.path.exists(TMP):
            os.remove(TMP)

    m = re.search(r"<title>([^<]*)</title>", out)
    title = unescape(m.group(1)) if m else "(没拿到 title)"
    print("结果：", title)

    ok = "s-home>s-map>s-quiz>s-quiz" in title and "第 2/10 题" in title
    print("判定：", "✅ 通过：首页→地图→答题→下一题 全部走通" if ok else "❌ 没走通，检查上面输出")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
