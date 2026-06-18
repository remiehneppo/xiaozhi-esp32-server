import os
import tempfile
import time
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, Form, Header, HTTPException, UploadFile
from faster_whisper import WhisperModel
from huggingface_hub import snapshot_download
from pydantic import BaseModel


MODEL_NAME = os.getenv(
    "WHISPER_MODEL",
    "quocphu/PhoWhisper-ct2-FasterWhisper/PhoWhisper-small-ct2-fasterWhisper",
)
MODEL_DIR = os.getenv("WHISPER_MODEL_DIR", "./models")
DEVICE = os.getenv("WHISPER_DEVICE", "cpu")
COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")
DEFAULT_LANGUAGE = os.getenv("WHISPER_LANGUAGE", "vi") or None
BEAM_SIZE = int(os.getenv("WHISPER_BEAM_SIZE", "5"))
INITIAL_PROMPT = os.getenv(
    "WHISPER_INITIAL_PROMPT",
    "Đây là hội thoại tiếng Việt. Hãy chép lại tự nhiên, đúng dấu tiếng Việt, "
    "giữ tên riêng và thuật ngữ kỹ thuật nếu có.",
)
API_KEY = os.getenv("ASR_API_KEY", "")

app = FastAPI(title="Máy chủ Whisper ASR", version="1.0.0")
model: Optional[WhisperModel] = None


class TranscriptionResponse(BaseModel):
    text: str


def require_auth(authorization: Optional[str]) -> None:
    if not API_KEY:
        return
    expected = f"Bearer {API_KEY}"
    if authorization != expected:
        raise HTTPException(status_code=401, detail="Token bearer không hợp lệ")


def resolve_model_path(model_name: str) -> str:
    model_path = Path(model_name).expanduser()
    if model_path.exists():
        return str(model_path)

    parts = model_name.split("/")
    if len(parts) <= 2:
        return model_name

    repo_id = "/".join(parts[:2])
    subfolder = "/".join(parts[2:])
    snapshot_path = snapshot_download(
        repo_id=repo_id,
        cache_dir=MODEL_DIR,
        allow_patterns=[f"{subfolder}/*"],
    )
    return str(Path(snapshot_path) / subfolder)


def get_model() -> WhisperModel:
    global model
    if model is None:
        Path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
        model = WhisperModel(
            resolve_model_path(MODEL_NAME),
            device=DEVICE,
            compute_type=COMPUTE_TYPE,
            download_root=MODEL_DIR,
        )
    return model


@app.on_event("startup")
def preload_model() -> None:
    if os.getenv("WHISPER_PRELOAD", "true").lower() == "true":
        get_model()


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "model": MODEL_NAME,
        "device": DEVICE,
        "compute_type": COMPUTE_TYPE,
        "language": DEFAULT_LANGUAGE,
    }


@app.get("/v1/models")
def models() -> dict:
    return {
        "object": "list",
        "data": [
            {
                "id": MODEL_NAME,
                "object": "model",
                "owned_by": "local",
            }
        ],
    }


@app.post("/v1/audio/transcriptions", response_model=TranscriptionResponse)
async def transcriptions(
    file: UploadFile = File(...),
    model_name: str = Form(default="", alias="model"),
    language: Optional[str] = Form(default=None),
    prompt: Optional[str] = Form(default=None),
    authorization: Optional[str] = Header(default=None),
) -> TranscriptionResponse:
    require_auth(authorization)

    suffix = Path(file.filename or "audio.wav").suffix or ".wav"
    start = time.time()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        whisper = get_model()
        segments, _info = whisper.transcribe(
            tmp_path,
            language=language or DEFAULT_LANGUAGE,
            beam_size=BEAM_SIZE,
            initial_prompt=prompt or INITIAL_PROMPT,
            vad_filter=True,
        )
        text = "".join(segment.text for segment in segments).strip()
        elapsed = time.time() - start
        print(
            f"Đã chuyển giọng nói thành văn bản file={file.filename} model_yêu_cầu={model_name or MODEL_NAME} "
            f"số_ký_tự={len(text)} thời_gian={elapsed:.3f}s",
            flush=True,
        )
        return TranscriptionResponse(text=text)
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
