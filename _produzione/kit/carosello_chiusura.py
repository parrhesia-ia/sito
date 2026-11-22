# 8 · chiusura
im, d = frame(8, None, None)
logo(d, 64, 330, 170)
d.text((66, 540), "E DICO LE COSE COME STANNO.", font=F(XB, 64), fill=INK)
para(d, 66, 660, "Articolo completo, con tutte le fonti:", F(IM, 40), MUTED, W - 128)
d.text((66, 730), "parrhesia-ia.com", font=F(BLACK, 96), fill=RED)
d.rounded_rectangle([64, 920, 600, 990], radius=35, outline=LINE, width=2, fill=BG2)
d.ellipse([90, 946, 108, 964], fill=RED); d.text((124, 955), "Contenuto generato con IA", font=F(ISB, 30), fill=MUTED, anchor="lm")
d.text((66, 1050), "Segui @parrhesia_ia · salva e condividi", font=F(ISB, 36), fill=INK)
slides.append(im)

for k, s in enumerate(slides, 1): grain(s).save(f"{OUT}/slide_{k}.png")
# provino
th = [Image.open(f"{OUT}/slide_{k}.png").resize((324, 405)) for k in range(1, N + 1)]
sh = Image.new("RGB", (4 * 334 + 10, 2 * 415 + 10), "white")
for k, t in enumerate(th): sh.paste(t, (10 + (k % 4) * 334, 10 + (k // 4) * 415))
sh.save(f"{D}/out/carosello_provino.png"); print("ok")
