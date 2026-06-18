import importlib
import math
import sys
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def load_app(monkeypatch):
    monkeypatch.setenv("VIENEU_PRELOAD", "false")
    monkeypatch.setenv("TTS_API_KEY", "")
    module = importlib.import_module("app")
    module.engine = module.FakeEngine(sample_rate=module.SAMPLE_RATE)
    return module


def test_health_reports_default_voice_and_voices(monkeypatch):
    module = load_app(monkeypatch)
    client = TestClient(module.app)

    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["sample_rate"] == 24000
    assert body["default_voice"] == "Thục Đoan (Nữ - Miền Nam)"
    assert body["loaded"] is True
    assert "Thục Đoan" in body["voices"]


def test_openai_speech_returns_wav_for_default_voice(monkeypatch):
    module = load_app(monkeypatch)
    client = TestClient(module.app)

    response = client.post(
        "/v1/audio/speech",
        json={
            "model": "vieneu-v2-turbo",
            "input": "Xin chào, tôi là Xiaozhi.",
            "response_format": "wav",
        },
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/wav"
    assert response.content.startswith(b"RIFF")
    assert response.content[8:12] == b"WAVE"


def test_index_stream_tts_returns_raw_pcm_by_default(monkeypatch):
    module = load_app(monkeypatch)
    client = TestClient(module.app)

    response = client.post("/tts", json={"text": "Xin chào", "character": "Thục Đoan"})

    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/pcm"
    assert len(response.content) > 0
    assert not response.content.startswith(b"RIFF")
    assert len(response.content) % 2 == 0


def test_benchmark_returns_latency_and_resource_metrics(monkeypatch, tmp_path):
    module = load_app(monkeypatch)
    monkeypatch.setattr(module, "BENCHMARK_DIR", tmp_path)
    monkeypatch.setattr(module, "BENCHMARK_LATEST_PATH", tmp_path / "latest.json")
    client = TestClient(module.app)

    response = client.post("/benchmark", json={"text": "Xin chào benchmark"})

    assert response.status_code == 200
    body = response.json()
    assert body["cases"][0]["total_latency_ms"] >= 0
    assert body["cases"][0]["synthesis_ms"] >= 0
    assert body["cases"][0]["chars_per_sec"] > 0
    assert math.isfinite(body["cases"][0]["realtime_factor"])
    assert body["resources"]["ram_mb_peak"] >= body["resources"]["ram_mb_start"]
    assert (tmp_path / "latest.json").exists()


def test_invalid_voice_is_rejected(monkeypatch):
    module = load_app(monkeypatch)
    client = TestClient(module.app)

    response = client.post("/tts", json={"text": "Xin chào", "character": "khong-co"})

    assert response.status_code == 400
    assert "voice" in response.json()["detail"].lower()
