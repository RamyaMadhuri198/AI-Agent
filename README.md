# 🤖 AI Agent

An intelligent conversational agent built from scratch using LangGraph, capable of web search, mathematical analysis, and summarization — deployed with a clean Streamlit UI.

**Live Demo:** [Try it here](https://ai-agent-duxvx3rtxbuimcx4kuejiq.streamlit.app/)

---

## ✨ Features

- 🔍 **Web Search** — Searches the web in real time using DuckDuckGo
- 🧮 **Python REPL** — Executes Python code for math and data analysis
- 📝 **Summarization** — Condenses and explains complex information clearly
- 🧠 **Multi-node Architecture** — Planner, Tool Caller, Analyzer, and Responder nodes
- 💬 **Chat History** — Keeps track of the full conversation in the session
- ⚡ **Fast Inference** — Powered by Groq's ultra-fast LLM API

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [LangGraph](https://github.com/langchain-ai/langgraph) | Agent framework & graph orchestration |
| [Groq + Llama 3.3](https://groq.com) | LLM inference (free & fast) |
| [DuckDuckGo Search](https://pypi.org/project/ddgs/) | Free web search tool |
| [ChromaDB](https://www.trychroma.com/) | Vector memory storage |
| [Streamlit](https://streamlit.io) | Frontend UI |

---

## 🏗️ Architecture

```
User Question
      ↓
 Planner Node      ← decides if a tool is needed
      ↓
 Tool Caller       ← runs web search or Python REPL
      ↓
 Analyzer Node     ← evaluates if the result is satisfactory
      ↓
 Responder Node    ← generates the final answer
```

---

## 🚀 Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/RamyaMadhuri198/AI-Agent.git
cd AI-Agent
```

**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=ai-agent
```

**5. Run the app**
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
AI-AGENT/
├── agent/
│   ├── __init__.py
│   ├── graph.py       # LangGraph graph definition
│   ├── nodes.py       # All agent nodes
│   └── state.py       # AgentState definition
├── app.py             # Streamlit UI
├── main.py            # Local testing entry point
├── requirements.txt
└── .env               # (not committed)
```

---

## 👩‍💻 Author

**Ramya Madhuri Narapureddy**  
Built as a hands-on project to learn agentic AI systems from scratch.
