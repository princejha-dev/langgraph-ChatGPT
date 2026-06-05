# LangGraph Chatbot

An intelligent chatbot built with **LangGraph** and **Streamlit** that uses the Groq LLM with web search and stock price lookup capabilities.

## 🚀 Features

- **Multi-turn Conversations** - Persistent chat history with multiple threads
- **Web Search** - Real-time web search using DuckDuckGo
- **Stock Price Lookup** - Fetch live stock prices
- **Streaming Responses** - Real-time response streaming
- **Conversation Memory** - SQLite-based persistent storage
- **Clean UI** - Modern Streamlit interface

## 🧩 Technologies Used

<p align="center">
  <img src="https://media.giphy.com/media/l0Exk8EUzSLsrErEQ/giphy.gif" alt="Python GIF" width="120" />
  <img src="https://media.giphy.com/media/3o7aCVf7QWv6gGEa44/giphy.gif" alt="Streamlit GIF" width="120" />
  <img src="https://media.giphy.com/media/3owzWwyKKC4zQC8KQo/giphy.gif" alt="AI GIF" width="120" />
  <img src="https://media.giphy.com/media/3oriO7A7bt1wsEP4cw/giphy.gif" alt="Database GIF" width="120" />
</p>

Built with: **Python**, **Streamlit**, **LangGraph**, **Groq**, **DuckDuckGo Search**, and **SQLite**.

## 📁 Project Structure

```
langgraph-chatgpt/
├── app/
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── agent.py          # Main LangGraph agent
│   │   └── tools.py          # Tool definitions
│   ├── frontend/
│   │   ├── __init__.py
│   │   └── app.py            # Streamlit UI
│   └── __init__.py
├── config/
│   ├── __init__.py
│   └── settings.py           # Configuration
├── data/
│   └── chatbot.db            # SQLite database
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🔧 Setup

### 1. Prerequisites
- Python 3.8+
- Groq API key (get it free at [console.groq.com](https://console.groq.com))

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```env
GROQ_API_KEY=your_actual_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
DATABASE_PATH=data/chatbot.db
```

## 🏃 Running Locally

### Development Mode

```bash
streamlit run app/frontend/app.py
```

The app will open at `http://localhost:8501`

## 📤 Deploy on Streamlit Cloud

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/langgraph-chatbot.git
git push -u origin main
```

### Step 2: Create Streamlit Account

1. Go to [streamlit.io](https://streamlit.io)
2. Sign up with GitHub
3. Authorize Streamlit to access your GitHub repositories

### Step 3: Deploy App

1. Click "New app" on Streamlit Cloud dashboard
2. Select your GitHub repository
3. Choose branch: `main`
4. Set main file path: `app/frontend/app.py`
5. Click "Deploy"

### Step 4: Add Secrets

1. Go to your app's settings
2. Click "Secrets"
3. Add your environment variables:

```
GROQ_API_KEY = "your_actual_groq_api_key"
GROQ_MODEL = "llama-3.1-8b-instant"
DATABASE_PATH = "data/chatbot.db"
```

### Step 5: Done! 🎉

Your app is now live on Streamlit Cloud. Share the public URL with others!

## 📊 How It Works

1. **User sends message** → Stored in session state
2. **LLM processes** → Decides if tools are needed
3. **Tools execute** → Web search or stock lookup (if needed)
4. **Response streams** → Real-time to user interface
5. **Conversation persists** → Saved in SQLite database

## 🛠️ Tools Available

### Web Search
- Searches the web using DuckDuckGo
- Usage: "Search for AI trends 2024"

### Stock Price
- Fetches real-time stock prices
- Usage: "What's the current price of AAPL?"

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key | Required |
| `GROQ_MODEL` | LLM model to use | `llama-3.1-8b-instant` |
| `DATABASE_PATH` | SQLite database location | `data/chatbot.db` |
| `STREAMLIT_THEME` | UI theme | `light` |

## 🐛 Troubleshooting

**Issue: "No such file or directory: 'data/chatbot.db'"**
- Solution: The database will be created automatically on first run

**Issue: "GROQ_API_KEY not found"**
- Solution: Ensure `.env` file is created and GROQ_API_KEY is set correctly

**Issue: Tools not working**
- Solution: Check your internet connection and API key validity

## 📚 Learn More

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Groq API Documentation](https://console.groq.com/docs)

## 📄 License

MIT License - feel free to use this project for learning and building!

## 👨‍💻 Author

Built with ❤️ using LangGraph and Streamlit
