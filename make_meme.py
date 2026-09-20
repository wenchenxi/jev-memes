# -*- coding: utf-8 -*-
"""
make_meme.py —— 生成一张给 TypeSafe 看的梗图（Jev vs 普通 LLM）

主题：我只想要一个「是/否」，一个让我读 900 个 token，一个直接给我 0.92。
画法用 PIL 逐字排版（不用生图模型），保证文字清晰、没有乱码。
"""
import os

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
W, H = 1280, 720
BG = (11, 11, 17)
PANEL = (22, 22, 30)
PANEL_JEV = (14, 32, 21)
WHITE = (240, 240, 245)
GREY = (140, 140, 155)
DIM = (100, 100, 115)
GREEN = (34, 197, 94)
RED = (196, 92, 92)
ACCENT = (232, 121, 199)      # TypeSafe 站上的那种粉色

F = lambda name, size: ImageFont.truetype("C:/Windows/Fonts/" + name, size)

title_font = F("arialbd.ttf", 30)
label_font = F("arialbd.ttf", 24)
body_font = F("arial.ttf", 17)
stat_font = F("consola.ttf", 16)
big_font = F("arialbd.ttf", 108)
sub_font = F("arial.ttf", 26)
cap_font = F("arialbd.ttf", 24)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# 顶部标题
d.text((60, 40), 'ME: "I just need a yes/no answer."', font=title_font, fill=WHITE)
d.line([(60, 92), (W - 60, 92)], fill=(45, 45, 58), width=2)

# 两块面板
TOP, BOT = 120, 600
LW = 560
LEFT_X, RIGHT_X = 60, 660
for x, fill, edge in ((LEFT_X, PANEL, (40, 40, 52)), (RIGHT_X, PANEL_JEV, (34, 120, 70))):
    d.rounded_rectangle([x, TOP, x + LW, BOT], radius=18, fill=fill, outline=edge, width=2)

# ---- 左：普通 LLM（啰嗦 + 又慢又贵）
d.text((LEFT_X + 28, TOP + 24), "AN LLM", font=label_font, fill=GREY)
ramble = [
    "Certainly! This is an important question, and the",
    "answer really depends on several factors. Let me",
    "walk through them carefully. First, it's worth",
    "noting that context matters a great deal here.",
    "Second, there are nuances on both sides that",
    "reasonable people might weigh differently...",
    "",
    "In conclusion, the answer is probably yes, though",
    "I'd encourage you to consider the caveats above.",
]
y = TOP + 78
for line in ramble:
    d.text((LEFT_X + 28, y), line, font=body_font, fill=(176, 176, 190))
    y += 27
d.text((LEFT_X + 28, BOT - 46), "~900 output tokens  ·  $0.02  ·  6.4 s",
       font=stat_font, fill=RED)

# ---- 右：Jev（一个数）
d.text((RIGHT_X + 28, TOP + 24), "JEV", font=label_font, fill=GREEN)
d.text((RIGHT_X + 28, TOP + 96), "0.92", font=big_font, fill=WHITE)
d.text((RIGHT_X + 28, TOP + 224), "yes — 92% calibrated", font=sub_font, fill=(150, 220, 175))
d.text((RIGHT_X + 28, TOP + 320), "…and that is the entire response.",
       font=F("ariali.ttf", 19), fill=DIM)
d.text((RIGHT_X + 28, BOT - 46), "0 output tokens  ·  $0.0004  ·  0.15 s",
       font=stat_font, fill=GREEN)

# 底部一句话
caption = "same question. same state. one of them never wrote a word."
tw = d.textlength(caption, font=cap_font)
d.text(((W - tw) / 2, BOT + 46), caption, font=cap_font, fill=ACCENT)

out = os.path.join(OUT_DIR, "why-i-want-jev.png")
img.save(out)
print("已生成:", out, os.path.getsize(out), "字节", img.size)
