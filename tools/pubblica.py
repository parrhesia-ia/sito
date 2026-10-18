"""Pubblica una bozza: python3 tools/pubblica.py <slug> "<data testo>"
Sposta _bozze/<slug>.html in articoli/, aggiorna data/articoli.json e rigenera le card."""
import json, os, sys, subprocess
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
slug, data_testo = sys.argv[1], sys.argv[2]
src, dst = os.path.join(R, "_bozze", slug + ".html"), os.path.join(R, "articoli", slug + ".html")
if os.path.exists(src): os.replace(src, dst)
elif not os.path.exists(dst): sys.exit(f"bozza non trovata: {slug}")
p = os.path.join(R, "data/articoli.json"); items = json.load(open(p, encoding="utf-8"))
url = f"articoli/{slug}.html"; found = False
for it in items:
    if it.get("slug") == slug or it.get("url") == url or (not it.get("url") and it.get("bozza") == slug):
        it["url"] = url; it["data_testo"] = data_testo; found = True
if not found: sys.exit(f"voce non trovata in articoli.json: {slug}")
pub = sorted([x for x in items if x["url"]], key=lambda x: x["data"], reverse=True)
soon = sorted([x for x in items if not x["url"]], key=lambda x: x["data"])
json.dump(pub + soon, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
subprocess.run([sys.executable, os.path.join(R, "tools/build.py")], check=True)
print("pubblicato", url)
