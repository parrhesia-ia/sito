"""Template caroselli ParrhesIA, 1080x1350 (4:5). Prova: decreto cortei."""
import os, random
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps

D = os.path.dirname(os.path.abspath(__file__)); OUT = f"{D}/out/carosello"; os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1350
BG = (14, 14, 14); BG2 = (24, 24, 24); INK = (240, 238, 234); MUTED = (154, 154, 154); RED = (214, 38, 38); LINE = (46, 46, 46)
def F(n, s): return ImageFont.truetype(n if n.startswith("/") else f"{D}/fonts/{n}.ttf", s)
BLACK, XB, BOLD = "BarlowCondensed-Black", "BarlowCondensed-ExtraBold", "BarlowCondensed-Bold"
IB, ISB, IM, IR = [f"/usr/share/fonts/opentype/inter/Inter-{w}.otf" for w in ("Bold", "SemiBold", "Medium", "Regular")]
N = 8

random.seed(3)
GR = Image.effect_noise((W // 2, H // 2), 40).resize((W, H)).convert("L")
def grain(im):
    return Image.composite(im, Image.new("RGB", (W, H), (0, 0, 0)), ImageOps.invert(GR).point(lambda v: 255 - v // 7))

def wrap(d, t, f, mw):
    out, cur = [], ""
    for w in t.split():
        x = (cur + " " + w).strip()
        if d.textlength(x, font=f) > mw and cur: out.append(cur); cur = w
        else: cur = x
    if cur: out.append(cur)
    return out

def para(d, x, y, t, f, fill, mw, lh=1.32):
    for ln in wrap(d, t, f, mw): d.text((x, y), ln, font=f, fill=fill); y += f.size * lh
    return y

def logo(d, x, y, s):
    f = F(BLACK, s); d.text((x, y), "PARRHES", font=f, fill=INK); d.text((x + d.textlength("PARRHES", font=f), y), "IA", font=f, fill=RED)

def stamp(im, txt, cx, cy, size, rot=-4):
    f = F(BLACK, size); tmp = Image.new("RGBA", (W, int(size * 1.7)), (0, 0, 0, 0)); d = ImageDraw.Draw(tmp)
    tw = d.textlength(txt, font=f); pad = size * .18
    d.rectangle([W/2 - tw/2 - pad, size*.2, W/2 + tw/2 + pad, size*1.45], outline=RED + (255,), width=max(5, size // 14))
    d.text((W/2, size*.82), txt, font=f, fill=RED + (255,), anchor="mm")
    r = random.Random(len(txt))
    for _ in range(int(tw)):
        px, py = r.uniform(W/2 - tw/2 - pad, W/2 + tw/2 + pad), r.uniform(0, size*1.7)
        d.ellipse([px, py, px + r.uniform(2, 6), py + r.uniform(2, 6)], fill=(0, 0, 0, 0))
    tmp = tmp.rotate(rot, resample=Image.BICUBIC)
    im.paste(tmp, (int(cx - W/2), int(cy - tmp.height/2)), tmp)

def frame(i, rubrica=None, fonte=None):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    logo(d, 64, 52, 46)
    d.text((W - 64, 60), f"{i}/{N}", font=F(BOLD, 36), fill=MUTED, anchor="ra")
    if rubrica:
        f = F(XB, 34); tw = d.textlength(rubrica.upper(), font=f)
        d.rectangle([64, 128, 64 + tw + 36, 176], fill=RED); d.text((82, 152), rubrica.upper(), font=f, fill=INK, anchor="lm")
    d.line([64, H - 110, W - 64, H - 110], fill=LINE, width=2)
    if fonte: d.text((64, H - 80), "Fonti: " + fonte, font=F(IM, 24), fill=MUTED)
    d.text((W - 64, H - 80), "parrhesia-ia.com", font=F(ISB, 24), fill=INK, anchor="ra")
    if i < N: d.text((W - 64, H - 160), "SCORRI  ›", font=F(IB, 28), fill=RED, anchor="ra")
    return im, d

def photo_bg(path, darken=.6):
    p = Image.open(path).convert("RGB"); p = ImageEnhance.Color(p).enhance(.2)
    s = max(W / p.width, H / p.height); p = p.resize((int(p.width*s)+1, int(p.height*s)+1))
    x, y = (p.width - W)//2, (p.height - H)//2; p = p.crop((x, y, x + W, y + H))
    p = Image.blend(p, Image.new("RGB", (W, H), BG), darken)
    g = Image.linear_gradient("L").resize((W, H)).point(lambda v: int(max(0, v - 60) * 1.3))
    return Image.composite(Image.new("RGB", (W, H), BG), p, g)

slides = []
