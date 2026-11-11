import re
from typing import Any

import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter


VIDEO_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{11}$")


def extract_video_id(url_or_id: str) -> str:
    """Extrai e valida o ID de um vídeo a partir de uma URL ou ID."""
    value = url_or_id.strip()
    if VIDEO_ID_PATTERN.fullmatch(value):
        return value

    patterns = (
        r"(?:youtube\.com/watch\?.*?v=)([A-Za-z0-9_-]{11})",
        r"youtu\.be/([A-Za-z0-9_-]{11})",
        r"youtube\.com/(?:shorts|embed)/([A-Za-z0-9_-]{11})",
    )
    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            return match.group(1)

    raise ValueError("URL ou ID do YouTube inválido. Informe um vídeo válido.")


def get_video_metadata(video_id: str) -> dict[str, Any]:
    """Obtém título e metadados sem baixar o vídeo."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    options = {"quiet": True, "no_warnings": True, "noplaylist": True}

    with yt_dlp.YoutubeDL(options) as downloader:
        info = downloader.extract_info(url, download=False)

    return {
        "id": info.get("id", video_id),
        "title": info.get("title") or "Título não encontrado",
        "url": url,
        "channel": info.get("channel") or info.get("uploader") or "Não informado",
        "duration": info.get("duration"),
    }


def get_transcript(video_id: str, languages: tuple[str, ...]) -> str:
    """Busca e formata a transcrição, priorizando os idiomas configurados."""
    try:
        transcript = YouTubeTranscriptApi().fetch(
            video_id,
            languages=list(languages),
        )
        text = TextFormatter().format_transcript(transcript)
        cleaned_text = " ".join(text.split())
        if not cleaned_text:
            raise ValueError("A transcrição retornada está vazia.")
        return cleaned_text
    except Exception as exc:
        raise RuntimeError(
            "Não foi possível obter a transcrição. Verifique se o vídeo possui "
            "legendas disponíveis e se o acesso ao YouTube está funcionando."
        ) from exc
