#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
把 src/data/words.json 注入 src/index.html 的内联数据块。

为什么要有这一步：
  游戏第一版是单个 index.html，双击就能玩（file:// 下 fetch 本地 JSON 会被浏览器拦掉），
  所以词库必须内联。但词库的唯一来源是 src/data/words.json（内容官只改这个文件）。
  内容官改完 JSON 后，跑一次本脚本，index.html 里的词库就同步了。

用法（在仓库根目录）：
  python tools/build.py
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "src", "data", "words.json")
HTML_PATH = os.path.join(ROOT, "src", "index.html")
START = "<!--WORDS:START-->"
END = "<!--WORDS:END-->"


def main():
    with io.open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)

    words = data.get("words", [])
    payload = json.dumps({"meta": data.get("meta", {}), "words": words},
                         ensure_ascii=False, separators=(",", ":"))
    # 防止 JSON 里出现 </script> 之类提前闭合标签的情况
    payload = payload.replace("</", "<\\/")
    block = (START + "\n<script id=\"word-data\" type=\"application/json\">"
             + payload + "</script>\n" + END)

    with io.open(HTML_PATH, encoding="utf-8") as f:
        html = f.read()

    i = html.find(START)
    j = html.find(END)
    if i < 0 or j < 0:
        print("找不到 WORDS 标记，index.html 未改动")
        return 1

    new = html[:i] + block + html[j + len(END):]
    with io.open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(new)

    print("已写入 %d 个词到 src/index.html（%.1f KB）"
          % (len(words), os.path.getsize(HTML_PATH) / 1024.0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
