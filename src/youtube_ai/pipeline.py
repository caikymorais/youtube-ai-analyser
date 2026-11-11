import logging
import re
from pathlib import Path

from youtube_ai.config import Settings
from youtube_ai.llm import build_chain
from youtube_ai.prompts import DEFAULT_QUESTION
from youtube_ai.youtube import extract_video_id, get_transcript, get_video_metadata

logger = logging.getLogger(__name__)


def _safe_filename(value: str) -> str:
    """Gera um nome de arquivo simples e seguro."""
    slug = re.sub(r"[^A-Za-z0-9_-]+", "_", value).strip("_")
    return slug[:70] or "video"


def save_transcript(transcript: str, metadata: dict, output_dir: Path) -> Path:
    """Salva a transcrição completa em UTF-8."""
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{_safe_filename(metadata['id'])}_transcript.txt"
    path.write_text(
        f"Título: {metadata['title']}\n"
        f"Canal: {metadata['channel']}\n"
        f"URL: {metadata['url']}\n\n"
        f"{transcript}\n",
        encoding="utf-8",
    )
    return path


def save_analysis(answer: str, question: str, metadata: dict, output_dir: Path) -> Path:
    """Salva a pergunta e a resposta em Markdown."""
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{_safe_filename(metadata['id'])}_analysis.md"
    content = (
        f"# Análise do vídeo\n\n"
        f"- **Título:** {metadata['title']}\n"
        f"- **Canal:** {metadata['channel']}\n"
        f"- **URL:** {metadata['url']}\n\n"
        f"## Pergunta\n\n{question}\n\n"
        f"## Resposta\n\n{answer}\n"
    )
    path.write_text(content, encoding="utf-8")
    return path


def run_pipeline(
    url_or_id: str,
    question: str = DEFAULT_QUESTION,
    settings: Settings | None = None,
) -> dict[str, str]:
    """Executa o fluxo completo e retorna os caminhos e a resposta."""
    settings = settings or Settings()
    video_id = extract_video_id(url_or_id)

    logger.info("Obtendo metadados do vídeo %s", video_id)
    metadata = get_video_metadata(video_id)

    logger.info("Buscando transcrição")
    transcript = get_transcript(video_id, settings.transcript_languages)
    transcript_path = save_transcript(transcript, metadata, settings.output_dir)

    logger.info("Inicializando modelo %s", settings.ollama_model)
    chain = build_chain(settings)

    logger.info("Executando análise com LangChain")
    answer = chain.invoke(
        {
            "title": metadata["title"],
            "question": question,
            "transcript": transcript,
        }
    )
    analysis_path = save_analysis(answer, question, metadata, settings.output_dir)

    return {
        "video_title": metadata["title"],
        "transcript_path": str(transcript_path),
        "analysis_path": str(analysis_path),
        "answer": answer,
    }
