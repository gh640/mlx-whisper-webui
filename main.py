"""STT (Speach-to-Text) Web UI with mlx-whisper"""

from functools import partial, wraps

import gradio as gr
import mlx_whisper

HF_REPO = "mlx-community/whisper-turbo"
LANGUAGE = "ja"


def main():
    iface = build_interface(hf_repo=HF_REPO, language=LANGUAGE)
    iface.launch()


def build_interface(hf_repo: str, language: str):
    transcribe_ = partial(transcribe, hf_repo=hf_repo, language=language)
    iface = gr.Interface(
        fn=for_gradio(transcribe_),
        inputs=gr.Audio(type="filepath"),
        outputs="text",
    )

    return iface


def for_gradio(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        try:
            return f(*args, **kwds)
        except Exception as err:
            raise gr.Error(str(err)) from err

    return wrapper


def transcribe(audio: str | None, hf_repo: str, language: str) -> str | None:
    if audio is None:
        return None

    result = mlx_whisper.transcribe(
        audio,
        path_or_hf_repo=hf_repo,
        language=language,
    )
    return result["text"]


if __name__ == "__main__":
    main()
