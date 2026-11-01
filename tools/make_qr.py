# -*- coding: utf-8 -*-
"""
生成「扫码开始游戏」的二维码图。链接变了就改 GAME_URL 重跑一次。

用法（需要装有 qrcode + pillow 的 Python，Windows 上可用 E:\\Python\\python.exe）：
    python tools/make_qr.py
产出：仓库根目录 `扫码开始游戏.png`
"""
import os

import qrcode
from PIL import Image, ImageDraw, ImageFont

GAME_URL = "https://word-quest-60356.app.workbuddy.host/?sharecode=YMRKAOKJ7P&v=013"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "扫码开始游戏.png")

W, H = 900, 1180
BG = (255, 255, 255)
INK = (32, 28, 48)
DIM = (120, 116, 140)
ACCENT = (108, 92, 231)


def font(size, bold=False):
    for path in (r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
                 r"C:\Windows\Fonts\simhei.ttf"):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def main():
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M,
                       box_size=12, border=2)
    qr.add_data(GAME_URL)
    qr.make(fit=True)
    code = qr.make_image(fill_color=INK, back_color=BG).convert("RGB")

    canvas = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(canvas)

    # 顶部标题
    d.text((W // 2, 90), "词勇者", font=font(66, True), fill=INK, anchor="mm")
    d.text((W // 2, 156), "Word Quest · 像素闯关背单词", font=font(30), fill=DIM, anchor="mm")
    d.text((W // 2, 214), "手机扫码，直接开玩", font=font(40, True), fill=ACCENT, anchor="mm")

    # 二维码居中
    qw, qh = code.size
    if qw > 700:
        scale = 700 / qw
        code = code.resize((int(qw * scale), int(qh * scale)), Image.NEAREST)
        qw, qh = code.size
    canvas.paste(code, ((W - qw) // 2, 290))

    # 底部说明
    y = 290 + qh + 56
    d.text((W // 2, y), "扫码后直接打开，无需下载安装", font=font(28), fill=DIM, anchor="mm")
    d.text((W // 2, y + 46), "3 关 · 100 词 · 手机可玩", font=font(26), fill=DIM, anchor="mm")
    d.text((W // 2, H - 70), "如果扫不出来，手动输入下面网址", font=font(20), fill=DIM, anchor="mm")
    d.text((W // 2, H - 38), "word-quest-60356.app.workbuddy.host", font=font(20), fill=ACCENT, anchor="mm")

    canvas.save(OUT)
    print("已生成：%s（%dx%d，%.0f KB）" % (OUT, W, H, os.path.getsize(OUT) / 1024.0))


if __name__ == "__main__":
    main()
