# VieNeu TTS Server

Local FastAPI service for Xiaozhi TTS using VieNeu-TTS v2 Turbo GGUF through the
`vieneu` SDK. It exposes both OpenAI-compatible speech synthesis and the
`index_stream` PCM endpoint expected by `xiaozhi-server`.

Default voice: `Thục Đoan (Nữ - Miền Nam)`.

## API

- `GET /health`
- `GET /v1/voices`
- `POST /v1/audio/speech`
- `POST /tts`
- `POST /benchmark`
- `GET /benchmark/last`

`/tts` returns raw PCM by default: signed 16-bit little-endian, mono, 24 kHz.
`/v1/audio/speech` accepts `response_format` as `wav` or `pcm`.

## Run With Docker

CPU:

```bash
cd main/vieneu-tts-server
docker compose up --build
```

GPU with NVIDIA Container Toolkit:

```bash
cd main/vieneu-tts-server
docker compose -f docker-compose.yml -f docker-compose.gpu.yml up --build
```

Models are cached under `./models`.

GPU mode requires a working host NVIDIA driver plus NVIDIA Container Toolkit.
Verify Docker GPU access before starting the service:

```bash
./scripts/check_gpu_docker.sh
```

If Docker reports `failed to discover GPU vendor from CDI` or cannot find
`nvidia-container-runtime`, install/configure `nvidia-container-toolkit` on the
host first.

## Local Python

```bash
cd main/vieneu-tts-server
./scripts/install.sh
./scripts/start.sh
```

Useful environment variables:

| Variable | Default |
| --- | --- |
| `VIENEU_MODEL_ID` | `pnnbao-ump/VieNeu-TTS-v2-Turbo-GGUF` |
| `VIENEU_MODE` | `turbo` |
| `VIENEU_MODEL_DIR` | `/models` |
| `HF_HOME` | `/models` |
| `HUGGINGFACE_HUB_CACHE` | `/models/hub` |
| `VIENEU_DEFAULT_VOICE` | `Thục Đoan (Nữ - Miền Nam)` |
| `VIENEU_DEVICE` | `cpu` |
| `VIENEU_N_GPU_LAYERS` | `0` |
| `VIENEU_THREADS` | CPU count minus one |
| `VIENEU_N_CTX` | `2048` |
| `VIENEU_FAKE` | `false` |
| `TTS_API_KEY` | empty |
| `PORT` | `8004` |

`VIENEU_FAKE=true` is only for local smoke tests and returns synthetic PCM
without loading the real model.

Set `HF_TOKEN` when available to avoid Hugging Face unauthenticated rate limits
during first model download.

## Xiaozhi Config

OpenAI-compatible provider:

```yaml
type: openai
api_url: http://vieneu-tts-server:8004/v1/audio/speech
model: vieneu-v2-turbo
voice: Thục Đoan (Nữ - Miền Nam)
format: wav
```

Realtime provider:

```yaml
type: index_stream
api_url: http://vieneu-tts-server:8004/tts
voice: Thục Đoan (Nữ - Miền Nam)
audio_format: pcm
```

See `examples/xiaozhi-config.yaml` for a fuller snippet.

## Benchmark

With the server running:

```bash
cd main/vieneu-tts-server
./scripts/benchmark.py --cold-start
```

The benchmark writes JSON to `benchmarks/latest.json` and includes latency,
realtime factor, throughput, CPU/RAM, and NVIDIA GPU utilization/VRAM metrics
when `nvidia-smi` is available.

CPU run:

```bash
docker compose up --build
./scripts/benchmark.py
```

GPU run:

```bash
docker compose -f docker-compose.yml -f docker-compose.gpu.yml up --build
./scripts/benchmark.py
```
