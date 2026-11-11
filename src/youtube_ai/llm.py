from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from youtube_ai.config import Settings


PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Você é um assistente que analisa transcrições de vídeos. "
            "Responda em português e utilize exclusivamente as informações "
            "presentes no título e na transcrição. Se a informação não estiver "
            "no conteúdo, diga claramente que ela não foi identificada.",
        ),
        (
            "human",
            "Título do vídeo: {title}\n\n"
            "Pergunta: {question}\n\n"
            "Transcrição:\n{transcript}",
        ),
    ]
)


def build_chain(settings: Settings):
    """Monta a chain LangChain: Prompt -> Ollama -> Parser."""
    model = ChatOllama(
        model=settings.ollama_model,
        temperature=settings.temperature,
    )
    return PROMPT | model | StrOutputParser()
