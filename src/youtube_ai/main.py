import argparse
import logging

from youtube_ai.config import load_settings
from youtube_ai.pipeline import run_pipeline
from youtube_ai.prompts import DEFAULT_QUESTION


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extrai a transcrição de um vídeo do YouTube e analisa com IA."
    )
    parser.add_argument("url", help="URL ou ID do vídeo do YouTube")
    parser.add_argument(
        "-q", "--question", default=DEFAULT_QUESTION,
        help="Pergunta que será respondida com base na transcrição",
    )
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )
    args = parse_args()
    settings = load_settings()

    try:
        result = run_pipeline(args.url, args.question, settings)
    except Exception as exc:
        logging.error("Falha no processamento: %s", exc)
        raise SystemExit(1) from exc

    print("\n========== RESULTADO ==========\n")
    print(f"Vídeo: {result['video_title']}\n")
    print(result["answer"])
    print("\nArquivos gerados:")
    print(f"- Transcrição: {result['transcript_path']}")
    print(f"- Análise: {result['analysis_path']}")


if __name__ == "__main__":
    main()
