# Whisper ASR Server

OpenAI-compatible speech-to-text service for `xiaozhi-server` using
`faster-whisper`.

The service exposes:

- `GET /health`
- `GET /v1/models`
- `POST /v1/audio/transcriptions`

`xiaozhi-server`'s existing `ASR.OpenaiASR` adapter can use this endpoint
directly.

## Docker

```bash
cd main/whisper-asr-server
docker compose up --build
```

Default endpoint:

```text
http://127.0.0.1:8001/v1/audio/transcriptions
```

Useful environment variables:

| Variable | Default | Meaning |
| --- | --- | --- |
| `WHISPER_MODEL` | `tiny` | faster-whisper model name or local model path. Use `small`, `medium`, or `large-v3` after the pipeline is stable. |
| `WHISPER_DEVICE` | `cpu` | `cpu`, `cuda`, or `auto`. |
| `WHISPER_COMPUTE_TYPE` | `int8` | Common CPU value: `int8`; common CUDA values: `float16`, `int8_float16`. |
| `WHISPER_LANGUAGE` | `vi` | Default transcription language. Use empty value for auto-detect. |
| `WHISPER_BEAM_SIZE` | `5` | Beam search size. Higher can improve quality but costs latency. |
| `WHISPER_INITIAL_PROMPT` | Vietnamese prompt | Bias text normalization for Vietnamese output. |
| `WHISPER_MODEL_DIR` | `/models` | Model cache/download directory in Docker. |
| `ASR_API_KEY` | empty | Optional bearer token. Empty means no auth enforcement. |

## Local Python

```bash
cd main/whisper-asr-server
./scripts/install.sh
./scripts/start.sh
```

## xiaozhi-server config

Put this in `main/xiaozhi-server/data/.config.yaml`:

```yaml
selected_module:
  ASR: OpenaiASR

ASR:
  OpenaiASR:
    type: openai
    api_key: local
    base_url: http://127.0.0.1:8001/v1/audio/transcriptions
    model_name: tiny
    output_dir: tmp/
```

If `ASR_API_KEY` is set on the Whisper service, use the same value in
`api_key`.
