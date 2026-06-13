# 🤖 LangGraph Chatbot

<p align="center">
  <img src="assets/banner.png" alt="LangGraph Chatbot Banner" width="100%">
</p>

<p align="center">
  <b>An AI-powered chatbot built with LangGraph, Streamlit, and Groq featuring tool calling, conversation memory, and real-time streaming.</b>
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-121212?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-00A67E?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-000000?style=for-the-badge)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge\&logo=sqlite\&logoColor=white)

</p>

---

# ✨ Features

* 💬 Multi-turn conversations
* 🧠 Persistent conversation memory (SQLite)
* 📝 Automatic summarization for long chats (context window management)
* 🌐 Web Search via Tavily
* 📈 Live Stock Price Lookup
* ⚡ Real-time streaming AI responses
* 🛠️ LangGraph tool calling with smart routing
* 🗂️ Multiple chat threads
* 🎨 Modern Streamlit UI

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
                  │
        ┌─────────┴──────────┐
        │                    │
        ▼                    ▼
   Tool Calling       Summarization Node
  (Web / Stock)    (context window mgmt)
        │                    │
        └─────────┬──────────┘
                  │
                  ▼
              Groq LLM
                  │
                  ▼
          Streaming Response
                  │
                  ▼
            SQLite Memory
```

---

# 📂 Project Structure

```
langgraph-chatbot/

├── app/
│
├── backend/
│   ├── agent.py
│   ├── nodes.py
│   ├── state.py
│   ├── tools.py
│   └── __init__.py
│
├── frontend/
│   ├── app.py
│   ├── ui.py
│   ├── utils.py
│   └── __init__.py
│
├── config/
│   └── settings.py
│
├── data/
│   └── chatbot.db
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
git clone https://github.com/yourusername/langgraph-chatbot.git

cd langgraph-chatbot
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key

# Optional: defaults to llama-3.3-70b-versatile
GROQ_MODEL=llama-3.3-70b-versatile

# Optional: defaults to <project_root>/data/chatbot.db
DATABASE_PATH=data/chatbot.db
```

---

## 4. Run

```bash
streamlit run app/frontend/app.py
```

Application:

```
http://localhost:8501
```

---

# 🔧 Available Tools

## 🌐 Web Search

Example:

```
Search latest AI news
```

Uses Tavily Search for real-time information.

---

## 📈 Stock Price Lookup

Example:

```
What is the current price of AAPL?
```

Fetches live stock prices.

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
               ├── messages > 10? ──► summarization_node
               │                         │
               │                    Summarizes old msgs,
               │                    stores in `summary`,
               │                    deletes old messages
               │                         │
               └─────────────────────────┘
                             │
                             ▼
                       Stream Response
                             │
                             ▼
                       Store in SQLite
```

---

# ☁️ Deploy on Streamlit Cloud

## Push Code

```bash
git init

git add .

git commit -m "Initial Commit"

git remote add origin https://github.com/yourusername/langgraph-chatbot.git

git push -u origin main
```

## Deploy

* Create a Streamlit Cloud account
* Connect your GitHub repository
* Select:

```
Branch:
main

Main file:
app/frontend/app.py
```

Add Secrets:

```text
GROQ_API_KEY="your_key"

GROQ_MODEL="llama-3.1-8b-instant"

DATABASE_PATH="data/chatbot.db"
```

Click **Deploy** 🎉

---

# ⚙️ Environment Variables

| Variable        | Description     |
| --------------- | --------------- |
| GROQ_API_KEY    | Groq API Key    |
| GROQ_MODEL      | Model Name      |
| DATABASE_PATH   | SQLite Database |
| STREAMLIT_THEME | UI Theme        |

---

# 🐞 Troubleshooting

### Database Missing

```
No such file: chatbot.db
```

✅ The database is automatically created on first run.

---

### API Key Missing

```
GROQ_API_KEY not found
```

✅ Add the key to your `.env` or Streamlit Secrets.

---

### Tools Not Working

* Verify internet connectivity
* Verify API credentials
* Restart the application

---

# 📚 Tech Stack

* Python
* LangGraph
* LangChain
* Streamlit
* Groq
* Tavily Search
* SQLite

---

# ⭐ Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub.

It helps others discover the project and motivates further development.

---

# 📄 License

MIT License

---

# 👨‍💻 Author

Built with ❤️ using **LangGraph**, **Streamlit**, and **Groq**.
