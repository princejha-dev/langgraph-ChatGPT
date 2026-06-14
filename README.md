# 🤖 LangGraph Chatbot

<p align="center">
  <img src="assets/banner.png" alt="LangGraph Chatbot Banner" width="100%">
</p>

<p align="center">
  <b>An AI-powered agentic chatbot built with LangGraph, Streamlit, and Groq — featuring tool calling, conversation memory, smart summarization, and LangSmith observability.</b>
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-121212?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-00A67E?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-000000?style=for-the-badge)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge\&logo=sqlite\&logoColor=white)
![LangSmith](https://img.shields.io/badge/LangSmith-Observability-orange?style=for-the-badge)

</p>

---

# ✨ Features

| Feature | Description |
|---|---|
| 💬 Multi-turn conversations | Full chat history per thread |
| 🧠 Persistent memory | SQLite-backed conversation storage |
| 📝 Smart summarization | Auto-compresses long chats to manage LLM context window |
| 🌐 Web Search | Real-time search via Tavily API |
| 📈 Stock Price Lookup | Live stock data via Alpha Vantage |
| ⚡ Streaming responses | Token-by-token real-time output |
| 🛠️ Tool calling | Smart LangGraph routing — only calls tools when needed |
| 🗂️ Multiple threads | Create and switch between independent conversations |
| 🔍 LangSmith tracing | Full observability and trace replay via LangSmith |
| 🎨 Modern UI | Clean Streamlit interface with sidebar thread management |

---

# 🖥️ Demo

<p align="center">
<img src="assets/demo.png" width="90%">
</p>

---

# 🏗️ Architecture

```
                User
                  │
                  ▼
          Streamlit Frontend
                  │
                  ▼
           LangGraph Agent
          (chat_node  ·  Groq LLM)
                  │
        ┌─────────┴──────────┐
        │                    │
        ▼                    ▼
   tools node          summarization_node
  (Web / Stock)       (context mgmt — runs
        │              when msgs > 16)
        └─────────┬──────────┘
                  │
                  ▼
          Streaming Response
                  │
                  ▼
     SQLite Checkpointer + LangSmith
```

---

# 📂 Project Structure

```
langgraph-chatgpt/
│
├── app/
│   ├── backend/
│   │   ├── agent.py        ← Graph definition & compilation
│   │   ├── nodes.py        ← chat_node, summarization_node, routing
│   │   ├── state.py        ← ChatState definition
│   │   ├── tools.py        ← web_search, get_stock_price
│   │   └── __init__.py
│   │
│   └── frontend/
│       ├── app.py          ← Streamlit entry point
│       ├── ui.py           ← Sidebar & chat rendering
│       ├── utils.py        ← Session state & thread helpers
│       └── __init__.py
│
├── config/
│   └── settings.py         ← Centralised env var loading
│
├── data/
│   └── chatbot.db          ← Auto-created SQLite database
│
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

---

# 🚀 Getting Started

## 1. Clone Repository

```bash
git clone https://github.com/princejha-dev/langgraph-ChatGPT.git
cd langgraph-ChatGPT
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ Yes | Your Groq API key |
| `TAVILY_API_KEY` | ✅ Yes | Your Tavily search API key |
| `GROQ_MODEL` | Optional | Defaults to `llama-3.3-70b-versatile` |
| `DATABASE_PATH` | Optional | Defaults to `data/chatbot.db` |
| `LANGCHAIN_TRACING_V2` | Optional | Set `true` to enable LangSmith tracing |
| `LANGCHAIN_API_KEY` | Optional | Your LangSmith API key |
| `LANGCHAIN_PROJECT` | Optional | LangSmith project name |

---

## 4. Run

```bash
streamlit run app/frontend/app.py
```

Open in browser: `http://localhost:8501`

---

# 🔧 Available Tools

| Tool | Trigger | API Used |
|---|---|---|
| 🌐 **Web Search** | Current events, recent news, live info | Tavily Search |
| 📈 **Stock Price** | "What is the price of AAPL?" | Alpha Vantage |

> The agent only calls tools when real-time or live data is explicitly needed. General knowledge questions are answered directly without a tool call.

---

# 🗄️ Conversation Flow

```
User Message
      │
      ▼
chat_node (Groq LLM)
      │
      ├── Has tool_calls? ──► tools node ──► back to chat_node
      │
      └── No tool_calls?
               │
               ├── messages > 16? ──► summarization_node
               │                         │
               │                    Summarizes old msgs into
               │                    a rolling `summary` string,
               │                    removes old messages from state
               │                         │
               └─────────────────────────┘
                             │
                             ▼
                    Stream response to UI
                             │
                             ▼
               SQLite checkpointer (persistence)
                             │
                             ▼
                    LangSmith trace (if enabled)
```

---

# 📝 Summarization Memory

To handle the LLM's context window limit, this chatbot uses a **rolling summarization strategy**:

1. After every response, the router checks if `len(messages) > 16`
2. If yes, `summarization_node` runs using a fast model (`llama-3.1-8b-instant`)
3. It summarizes all messages **except the most recent 6** into a compact summary string
4. Old messages are removed from the state using `RemoveMessage`
5. On the next turn, `chat_node` prepends the summary as a system message so the LLM retains full conversational context

This keeps the context window lean while preserving important history.

---

# 🔍 LangSmith Observability

Enable full trace visibility by adding these to your `.env`:

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=Agentic-Chatbot
```

You can then view:
- Full graph execution traces
- Node-level latency and token counts
- Tool call inputs/outputs
- Summarization runs

Visit [smith.langchain.com](https://smith.langchain.com) to access your traces.

---

# ☁️ Deploy on Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository and set:

| Setting | Value |
|---|---|
| Branch | `main` |
| Main file | `app/frontend/app.py` |

4. Add all environment variables from `.env.example` in the **Secrets** section
5. Click **Deploy** 🎉

---

# ⚙️ Environment Variables

| Variable | Default | Description |
|---|---|---|
| `GROQ_API_KEY` | — | Groq API key (required) |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | LLM model for chat |
| `TAVILY_API_KEY` | — | Tavily search key (required) |
| `DATABASE_PATH` | `data/chatbot.db` | SQLite database path |
| `LANGCHAIN_TRACING_V2` | `false` | Enable LangSmith tracing |
| `LANGCHAIN_API_KEY` | — | LangSmith API key |
| `LANGCHAIN_PROJECT` | `Agentic-Chatbot` | LangSmith project name |

---

# 🐞 Troubleshooting

| Problem | Solution |
|---|---|
| `No such file: chatbot.db` | Auto-created on first run — no action needed |
| `GROQ_API_KEY not found` | Add the key to `.env` or Streamlit Secrets |
| `TAVILY_API_KEY not found` | Add your Tavily key to `.env` |
| Tools not working | Verify internet connectivity and API credentials |
| LangSmith traces not appearing | Set `LANGCHAIN_TRACING_V2=true` and verify `LANGCHAIN_API_KEY` |
| Blank assistant message on chat switch | Already fixed — empty `AIMessage` objects are filtered out |

---

# 📚 Tech Stack

| Technology | Role |
|---|---|
| [Python](https://python.org) | Core language |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Agent graph orchestration |
| [LangChain](https://github.com/langchain-ai/langchain) | LLM abstraction layer |
| [Groq](https://groq.com) | Ultra-fast LLM inference |
| [Streamlit](https://streamlit.io) | Frontend UI |
| [Tavily](https://tavily.com) | Real-time web search |
| [Alpha Vantage](https://www.alphavantage.co) | Live stock price data |
| [SQLite](https://sqlite.org) | Conversation persistence |
| [LangSmith](https://smith.langchain.com) | Observability & tracing |

---

# ⭐ Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub.

It helps others discover the project and motivates further development

---

# 📄 License

MIT License

---

# 👨‍💻 Author

Built with ❤️ using **LangGraph**, **Streamlit**, and **Groq**.
