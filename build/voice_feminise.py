"""
Turn Pietro's voice sample into a woman's voice (7 Nov, Pietro's request: "a
sweet, decisive, calm and joyful woman voice" from his own voice).

Two steps on the sample, then Pocket TTS clones the result:
  1. formants raised by warping the spectral envelope (cepstrum, per STFT
     frame) by k, so the vocal tract sounds shorter; the harmonics, phase and
     timing are left alone;
  2. pitch raised by p with rubberband, formants preserved.
Pocket TTS then speaks new lines in that voice, which smooths away most of the
processing and keeps Pietro's delivery.

Measured 7 Nov (8 takes each; his male clone: about 11% word errors):
  L3 sample, p 1.62, k 1.14   median pitch 182 Hz, 4% word errors   (calm)
  L2 sample, p 1.72, k 1.14   215 Hz, 10%                          (bright)
  story read, p 1.72, k 1.14  202 Hz, 9%                           (warm)
Resampling-based formant shifts (asetrate) were less clear (10 to 47%).
Some sources drift back towards a male pitch in some takes (his WACC and
Levels #3 reads); check the pitch of every take.

    python build/voice_feminise.py sample.wav out.wav 1.62 1.14
"""
import subprocess, sys, tempfile, pathlib, wave
import numpy as np
from scipy.signal import stft, istft
SR = 24000
def load(p):
    w = wave.open(str(p)); return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
def save(p, a):
    a = np.clip(a, -1, 1); w = wave.open(str(p), "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((a * 32767).astype(np.int16).tobytes()); w.close()
def warp_formants(a, k, n_fft=1024, hop=128, lifter=36):
    f, t, Z = stft(a, SR, nperseg=n_fft, noverlap=n_fft - hop)
    mag, ph = np.abs(Z) + 1e-9, np.angle(Z)
    logm = np.log(mag)
    cep = np.fft.irfft(logm, axis=0)                       # real cepstrum per frame
    cep[lifter:-lifter] = 0                                  # keep the envelope
    env = np.fft.rfft(cep, axis=0).real[: mag.shape[0]]
    bins = np.arange(mag.shape[0])
    src = np.clip(bins / k, 0, mag.shape[0] - 1)             # new envelope at f = old envelope at f / k
    env_w = np.vstack([np.interp(src, bins, env[:, j]) for j in range(env.shape[1])]).T
    gain = np.exp(np.clip(env_w - env, -4, 4))
    _, y = istft(mag * gain * np.exp(1j * ph), SR, nperseg=n_fft, noverlap=n_fft - hop)
    y = y[: len(a)]
    return y * (np.sqrt(np.mean(a ** 2)) / (np.sqrt(np.mean(y ** 2)) + 1e-9))
def feminise(src, out, p, k):
    a = load(src)
    with tempfile.TemporaryDirectory() as d:
        mid = pathlib.Path(d) / "w.wav"; save(mid, warp_formants(a, k))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mid), "-af", f"rubberband=pitch={p}:formant=preserved:pitchq=quality",
                        "-ar", str(SR), "-ac", "1", str(out)], check=True)
if __name__ == "__main__":
    feminise(sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]))
