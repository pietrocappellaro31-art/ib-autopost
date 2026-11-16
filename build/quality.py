"""The daily quality score (8 Nov): DNSMOS P.835 (Microsoft, ONNX) for a speech file: SIG (how clean and
natural the voice itself sounds), BAK (background), OVRL (overall), each on a
1 to 5 scale. Port of DNSMOS/dnsmos_local.py without librosa."""
import subprocess, tempfile, pathlib, numpy as np, onnxruntime as ort
import os
M = pathlib.Path(os.environ.get("DNSMOS_MODEL", ""))
_s = None
P_SIG = np.poly1d([-0.08397278, 1.22083953, 0.0052439]); P_BAK = np.poly1d([-0.13166888, 1.60915514, -0.39604546])
P_OVR = np.poly1d([-0.06766283, 1.11546468, 0.04602535])
def load16(path):
    with tempfile.TemporaryDirectory() as d:
        r = pathlib.Path(d) / "a.raw"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "16000", "-f", "f32le", str(r)], check=True)
        return np.fromfile(r, np.float32)
def score(path):
    global _s
    if _s is None: _s = ort.InferenceSession(str(M), providers=["CPUExecutionProvider"])
    a = load16(path); L = int(9.01 * 16000)
    while len(a) < L: a = np.append(a, a)
    hops = int(np.floor(len(a) / 16000) - 9.01) + 1
    out = []
    for i in range(hops):
        seg = a[i * 16000: i * 16000 + L]
        if len(seg) < L: continue
        s, b, o = _s.run(None, {"input_1": seg[np.newaxis, :]})[0][0]
        out.append((P_SIG(s), P_BAK(b), P_OVR(o)))
    m = np.mean(out, 0)
    return dict(sig=round(float(m[0]), 2), bak=round(float(m[1]), 2), ovrl=round(float(m[2]), 2))
def score_at(path, lufs=-23.0):
    """16 Nov: DNSMOS at a common loudness. The model is level-sensitive: the same raw HEART stem, only turned up,
    scores SIG 3.71 at -23 LUFS and 3.60 at -14 (build/sig_stages.py on shorts-down-50-up-50), so a voice stem at
    about -22 against a -14 LUFS master showed a 'drop' of 0.10 to 0.16 that no stage of the master caused. Scoring
    both at -23 LUFS (EBU R128's reference) measures only what the mix does to the voice."""
    import levels as L
    i, _ = L.loudness(path)
    with tempfile.TemporaryDirectory() as d:
        out = pathlib.Path(d) / "lm.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(path), "-vn", "-af", f"volume={lufs - i:.2f}dB", "-ac", "1",
                        "-c:a", "pcm_f32le", str(out)], check=True)
        return score(out)
if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]: print(p.split("/")[-1], score(p))
