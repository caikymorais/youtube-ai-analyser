# YouTube AI Analyzer

Pipeline em Python para extrair metadados e transcrições de vídeos do YouTube e gerar respostas com um modelo de linguagem local, usando **LangChain + Ollama**.

## Funcionalidades

- Extração de metadados com `yt-dlp`.
- Busca de legendas/transcrições com `youtube-transcript-api`.
- Suporte a URL completa ou ID do vídeo.
- Análise orientada por pergunta com LangChain.
- Execução local com Ollama, sem chave de API de IA.
- Exportação da transcrição em TXT e da análise em Markdown.

## Arquitetura

```text
src/youtube_ai/
├── config.py       # Configurações e variáveis de ambiente
├── youtube.py      # ID, metadados e transcrição
├── llm.py          # Modelo Ollama e chain LangChain
├── prompts.py      # Pergunta padrão
├── pipeline.py     # Orquestração e persistência dos resultados
└── main.py         # Interface de linha de comando

tests/
└── test_youtube.py
```

## Requisitos

- Python 3.10 ou superior.
- [Ollama](https://ollama.com/) instalado e em execução.
- Um modelo disponível no Ollama. O exemplo utiliza `phi3`.
- O vídeo precisa disponibilizar legendas em um dos idiomas configurados.

## Instalação (Windows / PowerShell)

Clone o repositório e entre na pasta:

```powershell
git clone https://github.com/SEU-USUARIO/youtube-ai-analyzer.git
cd youtube-ai-analyzer
```

Crie e ative o ambiente virtual:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

Instale o modelo e inicie o Ollama:

```powershell
ollama pull phi3
```

O aplicativo se conecta ao serviço local do Ollama. Normalmente, o aplicativo Ollama mantém esse serviço em execução. Se necessário, inicie-o com `ollama serve` em outro terminal.

## Configuração

Copie o arquivo de exemplo:

```powershell
Copy-Item .env.example .env
```

Edite `.env` se quiser alterar o modelo, a temperatura, os idiomas das legendas ou a pasta de saída.

## Como executar

Com uma URL:

```powershell
python -m youtube_ai.main "https://www.youtube.com/watch?v=II28i__Tf3M"
```

Com uma pergunta personalizada:

```powershell
python -m youtube_ai.main "https://www.youtube.com/watch?v=II28i__Tf3M" --question "Quais são os principais conceitos apresentados?"
```

Também é possível informar somente o ID do vídeo.

## Resultados

Os arquivos são gravados na pasta `output/`:

- `VIDEO_ID_transcript.txt`: transcrição completa e metadados básicos.
- `VIDEO_ID_analysis.md`: pergunta e resposta produzida pelo modelo.

A pasta de resultados é ignorada pelo Git para evitar publicar arquivos gerados localmente.

## Testes

```powershell
python -m unittest discover -s tests -v
```

## Limitações conhecidas

- O projeto depende da disponibilidade de legendas/transcrições no YouTube.
- O modelo local possui limite de contexto. Vídeos muito longos podem exceder esse limite; uma evolução planejada é implementar divisão em chunks e sumarização hierárquica.
- A disponibilidade de vídeos e legendas pode variar conforme região, idioma e configurações do canal.
- O modelo pode produzir respostas incorretas; confira a transcrição e valide informações importantes.

## Próximas evoluções

- Implementar estratégia map-reduce para transcrições longas.
- Adicionar interface web com Streamlit ou FastAPI.
- Permitir seleção de provedores/modelos por configuração.
- Adicionar testes de integração com mocks para YouTube e Ollama.
- Exportar resumos em PDF.

## Tecnologias

`Python` · `LangChain` · `Ollama` · `yt-dlp` · `YouTube Transcript API`
