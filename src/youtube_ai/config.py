from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Configurações carregadas do ambiente."""

    model_provider: str = "ollama"
    ollama_model: str = "phi3"
    temperature: float = 0.1
    output_dir: Path = Path("output")
    transcript_languages: tuple[str, ...] = ("pt", "pt-BR", "en")


def load_settings() -> Settings:
    """Carrega o .env e devolve as configurações da aplicação."""
    load_dotenv()

    provider = os.getenv("MODEL_PROVIDER", "ollama").strip().lower()
    if provider != "ollama":
        raise ValueError(
            f"Provedor '{provider}' ainda não implementado. Use MODEL_PROVIDER=ollama."
        )

    try:
        temperature = float(os.getenv("MODEL_TEMPERATURE", "0.1"))
    except ValueError as exc:
        raise ValueError("MODEL_TEMPERATURE precisa ser um número.") from exc

    if not 0 <= temperature <= 2:
        raise ValueError("MODEL_TEMPERATURE deve estar entre 0 e 2.")

    languages = tuple(
        item.strip()
        for item in os.getenv("TRANSCRIPT_LANGUAGES", "pt,pt-BR,en").split(",")
        if item.strip()
    )

    return Settings(
        model_provider=provider,
        ollama_model=os.getenv("OLLAMA_MODEL", "phi3").strip(),
        temperature=temperature,
        output_dir=Path(os.getenv("OUTPUT_DIR", "output")),
        transcript_languages=languages or ("pt", "pt-BR", "en"),
    )
