#!/usr/bin/env bash
# Prepare a fresh session to voice Reels in Pietro's two cloned voices (L2, L3).
#
#   VOICE_KEY=<key> bash build/setup_voice.sh      then: source ~/voice-tools/env.sh
#
# VOICE_KEY is in the claude.ai Project doc "claude/voice-samples-key.md". Never
# paste it into the repo, a commit, a caption or a chat message.
# Downloads (about 0.7 GB, from GitHub releases, which this workspace can reach):
# sherpa-onnx (runs the models), Pocket TTS (the voice model, CC BY 4.0, Kyutai)
# and Parakeet (speech recognition, to check every line says the script).
set -euo pipefail
: "${VOICE_KEY:?set VOICE_KEY from the Project doc claude/voice-samples-key.md}"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
T="${VOICE_TOOLS:-$HOME/voice-tools}"
mkdir -p "$T/voices"
cd "$T"
R=https://github.com/k2-fsa/sherpa-onnx/releases/download
get() { [ -d "$2" ] || { echo "downloading $2"; curl -sSL "$R/$1/$2.tar.bz2" | tar xj; }; }
get v2.0.1 sherpa-onnx-v2.0.1-linux-x64-shared
get tts-models sherpa-onnx-pocket-tts-int8-2026-01-26
get asr-models sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8
for enc in "$REPO"/build/voices/*.flac.enc; do                # every encrypted voice sample (L2, L3, ...)
  n=$(basename "$enc" .flac.enc)
  openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -in "$enc" -pass env:VOICE_KEY \
    | ffmpeg -v error -y -f flac -i - -ac 1 -ar 24000 "voices/$n.wav"
done
cat > env.sh <<ENV
export SHERPA_DIR=$T/sherpa-onnx-v2.0.1-linux-x64-shared
export POCKET_DIR=$T/sherpa-onnx-pocket-tts-int8-2026-01-26
export PARAKEET_DIR=$T/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8
export VOICE_DIR=$T/voices
ENV
echo "ready: source $T/env.sh"
