# 🎰 Vegas Insider: Agentic AI Orchestrator
A modular AI-powered event discovery system that scrapes, indexes, and recommends activities in Las Vegas using a RAG (Retrieval-Augmented Generation) architecture.

## 🚀 Features
- **Automated Ingestion:** Uses Playwright to navigate and scrape JS-heavy content from Meetup.com.
- **Data Integrity:** Implements Pydantic schemas for strict validation of event dates, prices, and metadata.
- **Local Memory:** Leverages ChromaDB as a vector store for efficient semantic search ($0 cost).
- **Orchestrated Sync:** A dedicated sync engine manages duplicates and expires past events automatically.
- **AI Concierge:** A GPT-4o-mini powered agent that provides personalized recommendations based on natural language queries.

## 🛠️ Tech Stack
- **Language:** Python 3.12+
- **Orchestration:** Instructor, Pydantic
- **AI Model:** OpenAI GPT-4o-mini
- **Database:** ChromaDB (Local Vector Store)
- **Scraping:** Playwright, BeautifulSoup4
- **Environment:** uv, VS Code

## 🏁 Quick Start
1. Clone the repo.
2. Install dependencies: `uv pip install -r requirements.txt`
3. Set your API key: `export OPENAI_API_KEY='your-key-here'`
4. Run the sync: `python sync_engine.py`
5. Start the agent: `python main.py`