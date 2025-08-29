
# 🤖 Resume Agent

An AI chatbot that answers career-related questions on behalf of **any user**.  
Users can configure their **name**, upload a **PDF resume** (optional), and add **extra information** from a **sidebar**.  
The bot opens with:  
> “My name is {user_name} and you can ask me any career related questions.”

---

## ✨ Features

- **Generic profile setup** (no code changes needed):  
  - Name (required)  
  - PDF Resume upload (PDF-only, optional)  
  - Additional Info (contact, portfolio, short bio, achievements, etc.)
- **Streaming responses** via OpenAI Chat Completions
- **Resume parsing** (PDF → text) via `pypdf`
- **Modular codebase** (LLM client, prompts, persona, UI separated)
- **Stateful chat** using Streamlit’s `session_state`
- **Clean UX**: User message and streaming reply appear on the same run

---

## 🧱 Repository Structure
hamza-agent/
├─ app.py
├─ .env.example
├─ .gitignore
├─ README.md
├─ requirements.txt
└─ src/
├─ init.py
├─ core/
│ ├─ init.py
│ ├─ prompts.py # builds the system prompt from name + resume text + extra info
│ ├─ resume_parser.py # PDF bytes -> text extraction
│ ├─ llm.py # OpenAI client + streaming generator
│ └─ persona.py # Persona dataclass (name/resume/extra), caches parsed text
└─ ui/
├─ init.py
└─ streamlit_chat.py # Sidebar config + chat UI + streaming flow

---

## ⚙️ Requirements

- Python 3.9–3.12
- An OpenAI API key

`requirements.txt`:

```bash
openai>=1.30.0,<2
python-dotenv>=1.0.1
pypdf>=4.2.0
streamlit>=1.30.0
```
---

## 🔐 Environment Variables

Create a `.env` in the project root (copy from `.env.example`):

```bash
OPENAI_API_KEY=sk-your-key
# Optional: defaults to gpt-4o
OPENAI_MODEL=gpt-4o
```

---

## 🚀 Setup & Run
### 1) Create and activate a virtual environment
#### macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

#### Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

### 2) Install dependencies
pip install -r requirements.txt

### 3) Configure environment
cp .env.example .env

#### Edit .env and set your OPENAI_API_KEY

### 4) Start the app
streamlit run app.py


Open the local URL Streamlit prints (default: http://localhost:8501).