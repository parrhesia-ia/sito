_kb = kenburns
def kenburns(name, x, *a, **k): return _kb(name, max(x, 0.002), *a, **k)  # evita arrotondamenti negativi al fotogramma 0
OUTNAME = "ParrhesIA_32_kennedy_1963"
MUSIC = sys.argv[sys.argv.index("--music") + 1] if "--music" in sys.argv else None
def main():
    dummy = "--dummy" in sys.argv
    T, total = m.timeline(dummy)
    total += 2.0
    T[0]["at"] = T[0]["t0"]; T[0]["t0"] = 0.0  # la prima scena si vede dal primo fotogramma
    out = f"{D}/out"; os.makedirs(out, exist_ok=True)
    orig_sub = m.subtitles
    m.subtitles = lambda d, seg, t: orig_sub(d, seg, t) if seg["words"] else None
    if "--frames" in sys.argv:
        for tt in [float(v) for v in sys.argv[sys.argv.index("--frames") + 1].split(",")]:
            m.frame(T, total, tt, 0).save(f"{out}/f_{tt:05.1f}.png")
        print("scene:", [(s["scene"], round(s["t0"], 1)) for s in T], "totale", round(total, 1)); return
    segs = [s for s in T if s["audio"]]
    parts, filt = [], []
    for i, s in enumerate(segs):
        parts += ["-i", s["audio"]]; ms = int(s.get("at", s["t0"]) * 1000); filt.append(f"[{i}:a]adelay={ms}|{ms},aformat=channel_layouts=stereo[a{i}]")
    n = len(segs)
    parts += ["-i", f"{D}/firma.mp3", "-i", f"{D}/firma.mp3", "-stream_loop", "-1", "-i", MUSIC or f"{D}/tappeto.mp3"]
    end_ms = int((total - 4.3) * 1000)
    filt.append(f"[{n}:a]volume=0.45,aformat=channel_layouts=stereo[f1]")
    filt.append(f"[{n+1}:a]adelay={end_ms}|{end_ms},volume=0.8,aformat=channel_layouts=stereo[f2]")
    mix = "".join(f"[a{i}]" for i in range(n))
    filt.append(f"{mix}amix=inputs={n}:normalize=0,apad,atrim=0:{total},loudnorm=I=-15:TP=-1.5,asplit=2[v][sc]")
    filt.append(f"[{n+2}:a]atrim=0:{total},afade=t=in:d=0.3,afade=t=out:st={total-3}:d=3,volume=0.22,aformat=channel_layouts=stereo[bed0]")
    filt.append("[bed0][f1]amix=inputs=2:normalize=0[bed]")
    filt.append("[bed][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[duck]")
    filt.append("[v][duck][f2]amix=inputs=3:normalize=0,alimiter=limit=0.95[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *parts, "-filter_complex", ";".join(filt), "-map", "[out]", "-ar", "44100", "-t", str(total), f"{out}/audio.wav"], check=True)
    nf = int(total * FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", f"{out}/audio.wav", "-c:a", "aac", "-b:a", "192k", "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
           "-preset", "medium", "-movflags", "+faststart", f"{out}/{OUTNAME}.mp4"]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(nf):
        p.stdin.write(m.frame(T, total, fi / FPS, fi).tobytes())
        if fi % 600 == 0: print("frame", fi, "/", nf, flush=True)
    p.stdin.close(); p.wait(); print("fatto", round(total, 1))

if __name__ == "__main__":
    main()
