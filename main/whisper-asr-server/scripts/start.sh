#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -d .venv ]; then
  echo "Missing .venv. Run ./scripts/install.sh first." >&2
  exit 1
fi

. .venv/bin/activate

export WHISPER_MODEL="${WHISPER_MODEL:-quocphu/PhoWhisper-ct2-FasterWhisper/PhoWhisper-small-ct2-fasterWhisper}"
export WHISPER_DEVICE="${WHISPER_DEVICE:-cpu}"
export WHISPER_COMPUTE_TYPE="${WHISPER_COMPUTE_TYPE:-int8}"
export WHISPER_LANGUAGE="${WHISPER_LANGUAGE:-vi}"
export WHISPER_MODEL_DIR="${WHISPER_MODEL_DIR:-./models}"

exec uvicorn app:app --host "${HOST:-0.0.0.0}" --port "${PORT:-8001}"
