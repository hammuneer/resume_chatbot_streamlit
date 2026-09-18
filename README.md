# Resume Agent

A configurable Streamlit chatbot that answers career-related questions **on behalf of any user** —
not just one hardcoded persona. Visitors set a name, optionally upload a PDF resume, and add free-text
notes from the sidebar; the assistant is grounded in whatever is provided.

## Features

- **Generic profile setup**, no code changes needed: name (required), PDF resume upload (optional),
  and free-text extra info (contact details, portfolio link, achievements, ...).
- **Streaming responses** via the OpenAI Chat Completions API.
- **Resume parsing** (PDF bytes → text) via `pypdf`, tolerant of missing/malformed PDFs.
- **Modular codebase**: LLM client, prompt construction, persona state, and UI are separated.
- **Stateful chat** using Streamlit's `session_state`.

## How it works

```
Sidebar (name, resume PDF, extra info)
        │
        ▼
   Persona (resume_agent.core.persona)
        │  caches parsed PDF text
        ▼
build_system_prompt (resume_agent.core.prompts)
        │
        ▼
stream_chat (resume_agent.core.llm) ──> OpenAI Chat Completions (streamed)
        │
        ▼
st.write_stream (resume_agent.ui.streamlit_chat)
```

## Project structure

```
.
├── app.py                          # Streamlit entry point
├── src/resume_agent/
│   ├── core/
│   │   ├── llm.py                  # OpenAI client + streaming generator
│   │   ├── persona.py              # Persona dataclass; caches parsed resume text
│   │   ├── prompts.py              # builds the system prompt
│   │   └── resume_parser.py        # PDF bytes -> text extraction
│   └── ui/
│       └── streamlit_chat.py       # sidebar config + chat UI + streaming flow
├── tests/
├── pyproject.toml
└── requirements.txt
```

## Getting started

### Prerequisites

- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys)

### Installation

```bash
git clone https://github.com/hammuneer/resume_chatbot_streamlit.git
cd resume_chatbot_streamlit
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### Configuration

```bash
cp .env.example .env
# then edit .env and set OPENAI_API_KEY (OPENAI_MODEL is optional, defaults to gpt-4o)
```

### Run

```bash
streamlit run app.py
```

Open the local URL Streamlit prints (default: http://localhost:8501), then set your name (and
optionally upload a resume PDF) in the sidebar and click **Apply / Update Profile**.

## Testing

```bash
pytest
```

## License

See [LICENSE](LICENSE).
