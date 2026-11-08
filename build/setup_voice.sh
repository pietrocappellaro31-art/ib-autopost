#!/usr/bin/env bash
# Prepare a fresh session to voice Reels and YouTube videos.
#
#   bash build/setup_voice.sh            then: source ~/voice-tools/env.sh
#
# Voices since 8 Nov: Reels rotate G2, BELLA, EMMA; YouTube is GEORGE. All four
# are synthetic (Kokoro, Apache 2.0), so no key is needed. VOICE_KEY (Project doc
# claude/voice-samples-key.md) is only for re-rendering Pietro's older clones
# (P1, L2, L3, L4); never print, paste or commit it.
# Downloads about 1 GB from GitHub (reachable from this workspace):
#   Kokoro-82M (voices BELLA, EMMA, GEORGE and G2's sample), misaki dictionaries,
#   sherpa-onnx, Pocket TTS (G2's engine, CC BY 4.0, Kyutai), Parakeet (word
#   check), WeSpeaker (G2's take selection), DNSMOS (daily quality score).
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
T="${VOICE_TOOLS:-$HOME/voice-tools}"
mkdir -p "$T/voices" "$T/kokoro"
cd "$T"
R=https://github.com/k2-fsa/sherpa-onnx/releases/download
get() { [ -d "$2" ] || { echo "downloading $2"; curl -sSL "$R/$1/$2.tar.bz2" | tar xj; }; }
get v2.0.1 sherpa-onnx-v2.0.1-linux-x64-shared
get tts-models sherpa-onnx-pocket-tts-int8-2026-01-26
get asr-models sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8
[ -f wespeaker_en_voxceleb_resnet34.onnx ] || curl -sSL -o wespeaker_en_voxceleb_resnet34.onnx \
  "$R/speaker-recongition-models/wespeaker_en_voxceleb_resnet34.onnx"
K=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -f kokoro/kokoro-v1.0.onnx ] || curl -sSL -o kokoro/kokoro-v1.0.onnx "$K/kokoro-v1.0.onnx"
[ -f kokoro/voices-v1.0.bin ] || curl -sSL -o kokoro/voices-v1.0.bin "$K/voices-v1.0.bin"
cp "$REPO/build/voices/kokoro/config.json" kokoro/config.json
if [ ! -f kokoro/us_gold.json ]; then
  rm -rf misaki && git clone -q --depth 1 https://github.com/hexgrad/misaki misaki
  cp misaki/misaki/data/us_gold.json misaki/misaki/data/us_silver.json kokoro/ && rm -rf misaki
fi
if [ ! -f dnsmos/sig_bak_ovr.onnx ]; then
  rm -rf dns && GIT_LFS_SKIP_SMUDGE=1 git clone -q --depth 1 --filter=blob:none --sparse https://github.com/microsoft/DNS-Challenge dns
  (cd dns && git sparse-checkout set DNSMOS/DNSMOS)
  mkdir -p dnsmos && cp dns/DNSMOS/DNSMOS/sig_bak_ovr.onnx dnsmos/ && rm -rf dns
fi
if [ -n "${VOICE_KEY:-}" ]; then
  for enc in "$REPO"/build/voices/*.flac.enc; do            # Pietro's older clones, only for re-renders
    n=$(basename "$enc" .flac.enc)
    openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -in "$enc" -pass env:VOICE_KEY \
      | ffmpeg -v error -y -f flac -i - -ac 1 -ar 24000 "voices/$n.wav"
  done
fi
cat > env.sh <<ENV
export KOKORO_DIR=$T/kokoro
export SHERPA_DIR=$T/sherpa-onnx-v2.0.1-linux-x64-shared
export POCKET_DIR=$T/sherpa-onnx-pocket-tts-int8-2026-01-26
export PARAKEET_DIR=$T/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8
export SPEAKER_MODEL=$T/wespeaker_en_voxceleb_resnet34.onnx
export DNSMOS_MODEL=$T/dnsmos/sig_bak_ovr.onnx
export VOICE_DIR=$T/voices
ENV
echo "ready: source $T/env.sh"
