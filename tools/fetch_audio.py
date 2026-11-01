# -*- coding: utf-8 -*-
"""
把词库里的每个单词的发音下载到 src/audio/<word>.mp3。

为什么不用浏览器自带语音合成：手机端（微信内置浏览器、iOS Safari）的
speechSynthesis 经常静默失效，比赛现场也不一定有好网络。
自带 mp3 是最稳的方案：本地文件、无延迟、离线可听。

用法（改完词表后重跑一次即可，已有的不会重复下载）：
    python tools/fetch_audio.py            # 只补缺失的
    python tools/fetch_audio.py --force    # 全部重下
"""
import json
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORDS = os.path.join(ROOT, "src", "data", "words.json")
OUT = os.path.join(ROOT, "src", "audio")
API = "https://dict.youdao.com/dictvoice?audio={}&type={}"  # type=2 美音（与词库音标一致），type=1 英音备用
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"


def looks_like_mp3(data):
    return len(data) > 2000 and (data[:3] == b"ID3" or data[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2"))


def download(word, voice_type):
    req = urllib.request.Request(API.format(word, voice_type), headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def fetch(word, force=False):
    path = os.path.join(OUT, word + ".mp3")
    if not force and os.path.exists(path) and os.path.getsize(path) > 2000:
        return word, "skip", os.path.getsize(path)
    # 个别词的美音接口会返回 WAV（体积大且格式不符），此时退回英音 mp3
    for voice_type, note in ((2, "ok"), (1, "ok-uk")):
        try:
            data = download(word, voice_type)
        except Exception as e:
            last = "error: %s" % e
            continue
        if looks_like_mp3(data):
            with open(path, "wb") as f:
                f.write(data)
            return word, note, len(data)
        last = "error: 返回内容不是 mp3（%d 字节）" % len(data)
    return word, last, 0


def main():
    force = "--force" in sys.argv
    with open(WORDS, encoding="utf-8") as f:
        words = [w["en"] for w in json.load(f)["words"]]
    os.makedirs(OUT, exist_ok=True)

    done, skipped, uk, errs = 0, 0, [], []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for word, status, size in ex.map(lambda w: fetch(w, force), words):
            if status == "ok":
                done += 1
            elif status == "ok-uk":
                done += 1
                uk.append(word)
            elif status == "skip":
                skipped += 1
            else:
                errs.append((word, status))

    total = sum(os.path.getsize(os.path.join(OUT, w + ".mp3")) for w in words
                if os.path.exists(os.path.join(OUT, w + ".mp3")))
    print("下载 %d 个 / 跳过 %d 个 / 失败 %d 个" % (done, skipped, len(errs)))
    print("音频目录总大小：%.1f KB" % (total / 1024.0))
    if uk:
        print("以下词美音接口异常，已用英音（发音差异极小）：%s" % ", ".join(uk))
    for w, e in errs:
        print("  失败：%s -> %s" % (w, e))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
