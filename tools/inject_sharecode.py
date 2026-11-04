# -*- coding: utf-8 -*-
"""
给「版本测试站」(word-quest-lab) 的 HTML 副本注入 sharecode 传递补丁。
背景：部署平台要求分享口令才能取静态页，不带 ?sharecode= 的子页面会返回占位页。
用途：把当前 URL 的 sharecode 自动拼到所有站内相对链接，保证测试者点任何入口都能打开真页面。
幂等：带 WQ_SHARE_PATCH 标记的文件会跳过。
注意：只作用于 lab 副本；word-quest/src 下的对照组原件绝不动。
"""
import glob, io, os, sys

LAB = r"C:/Users/XIAN&YING/WorkBuddy/2026-10-31-22-18-46/word-quest-lab"
MARK = "WQ_SHARE_PATCH"

PATCH = """
<script>/* WQ_SHARE_PATCH: 部署平台分享口令透传（幂等，仅作用于测试站副本） */
(function(){
  var m=(location.search||"").match(/[?&]sharecode=[^&]*/);
  if(!m) return;
  var q=m[0].replace(/^[?&]/,"");
  Array.prototype.forEach.call(document.querySelectorAll("a[href]"),function(a){
    var h=a.getAttribute("href")||"";
    if(!h||/^(https?:|#|mailto:|javascript:|data:)/.test(h)) return;
    if(h.indexOf("sharecode=")!==-1) return;
    a.setAttribute("href", h+(h.indexOf("?")===-1?"?":"&")+q);
  });
})();
</script>
"""

def main():
    changed = []
    for f in sorted(glob.glob(os.path.join(LAB, "*.html"))):
        # 总览页 index.html 自带透传脚本，跳过以免重复
        if os.path.basename(f).lower() == "index.html":
            print("SKIP (self-contained):", os.path.basename(f))
            continue
        s = io.open(f, encoding="utf-8").read()
        if MARK in s:
            print("SKIP (already patched):", os.path.basename(f))
            continue
        if "</body>" not in s:
            print("WARN no </body>:", os.path.basename(f))
            continue
        s = s.replace("</body>", PATCH + "\n</body>", 1)
        io.open(f, "w", encoding="utf-8", newline="").write(s)
        changed.append(os.path.basename(f))
    print("PATCHED:", changed)

if __name__ == "__main__":
    main()
