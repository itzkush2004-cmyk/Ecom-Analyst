# NL-SQL Analyst — Conversational AI for E-Commerce Data

A natural language interface to a live e-commerce database. Ask plain English business questions, get SQL-powered answers, AI-generated insights, and confidence scores — no SQL knowledge needed.

Built on the Olist Brazilian E-Commerce dataset (1.5M+ records, 9 tables) hosted on Supabase.

---

## What it does

- Translates plain English questions into PostgreSQL queries using LLaMA 3
- Executes queries against a live Supabase database
- Returns results with an AI insight explaining what the numbers mean
- Rates query confidence (High / Medium / Low) so you know when to trust the result
- Remembers conversation context so follow-up questions work naturally

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | LLaMA 3.3 70B via Groq API |
| Database | Supabase (PostgreSQL) |
| Backend | Python, SQLAlchemy, psycopg2 |
| AI layers | Groq API (SQL gen, insight, confidence) |

## Project structure
```
ecom-analyst/
├── app.py                  # Streamlit UI
├── requirements.txt
├── .env                    # Not committed
└── src/
    ├── db.py               # Supabase connection
    ├── llm.py              # SQL generation via LLaMA 3
    ├── query_runner.py     # Orchestrates the pipeline
    ├── validator.py        # SQL safety checker
    ├── confidence.py       # Query confidence scoring
    └── insight.py          # Plain English result interpretation
```

## Setup

1. Clone the repo
2. Create a `.env` file:
```
SUPABASE_URL=your_supabase_connection_string
GROQ_API_KEY=your_groq_api_key
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run:
```bash
streamlit run app.py
```

## Sample questions to ask

- Which product category has the highest average review score?
- What are the top 5 states by total revenue?
- How many orders were delivered late?
- What is the most common payment method?
- Which seller has the most orders?
- Show me monthly order trends for 2018
- What is the average delivery time by state?

## Known limitations

- Date columns stored as varchar — all date queries require explicit CAST
- LLM may misinterpret highly ambiguous questions (flagged via Low Confidence)
- Geolocation table not yet used in queries
- No authentication — anyone with the URL can query the database
- Supabase free tier has connection limits under heavy load
