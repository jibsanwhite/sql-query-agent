"""
SQL Query Agent using LangChain.

Connects to a SQLite database and answers natural language questions
by generating and executing SQL queries.

Usage:
    python agent.py                          # uses demo database
    python agent.py --db path/to/db.sqlite   # your database
    python agent.py --db mydb.sqlite --question "How many users signed up last month?"
"""

import argparse
import os
import sqlite3
from urllib.parse import quote

from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType

load_dotenv()


def create_demo_database(db_path: str):
    """Creates a demo e-commerce SQLite database for testing."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            country TEXT,
            created_at DATE DEFAULT CURRENT_DATE
        );
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER REFERENCES customers(id),
            product_id INTEGER REFERENCES products(id),
            quantity INTEGER NOT NULL,
            total REAL NOT NULL,
            order_date DATE DEFAULT CURRENT_DATE
        );
        INSERT OR IGNORE INTO customers VALUES
            (1,'Alice Johnson','alice@example.com','USA','2024-01-15'),
            (2,'Bob Smith','bob@example.com','UK','2024-02-20'),
            (3,'Carlos Lima','carlos@example.com','Brazil','2024-03-10'),
            (4,'Diana Prince','diana@example.com','USA','2024-01-05');
        INSERT OR IGNORE INTO products VALUES
            (1,'Laptop Pro','Electronics',1299.99,45),
            (2,'Wireless Mouse','Electronics',29.99,200),
            (3,'Python Book','Books',49.99,120),
            (4,'Standing Desk','Furniture',599.99,15);
        INSERT OR IGNORE INTO orders VALUES
            (1,1,1,1,1299.99,'2024-04-01'),
            (2,1,2,2,59.98,'2024-04-01'),
            (3,2,3,1,49.99,'2024-04-05'),
            (4,3,4,1,599.99,'2024-04-10'),
            (5,4,1,1,1299.99,'2024-04-12'),
            (6,2,2,3,89.97,'2024-04-15');
    """)
    conn.commit()
    conn.close()


def sqlite_uri(db_path: str, read_only: bool = True) -> str:
    abs_path = os.path.abspath(db_path)
    if read_only:
        return f"sqlite:///file:{quote(abs_path)}?mode=ro&uri=true"
    return f"sqlite:///{abs_path}"


def build_llm():
    """Elige el modelo segun LLM_PROVIDER (ver .env.example).

    - openai (original del repo): GPT-4o-mini, necesita OPENAI_API_KEY (de pago).
    - gemini (adaptacion para D.J.): Gemini habla el mismo protocolo que
      OpenAI, asi que el resto del codigo no cambia. La clave es GRATIS en
      Google AI Studio (aistudio.google.com -> Get API key) y no pide tarjeta.
    """
    provider = os.environ.get("LLM_PROVIDER", "openai").lower()
    if provider == "gemini":
        return ChatOpenAI(
            model=os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=os.environ.get("GEMINI_API_KEY"),
            temperature=0,
        )
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)


def build_agent(db_path: str, read_only: bool = True):
    db = SQLDatabase.from_uri(sqlite_uri(db_path, read_only=read_only))
    llm = build_llm()
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
    )
    return agent, db


def main():
    parser = argparse.ArgumentParser(description="SQL Query Agent")
    parser.add_argument("--db", default="demo.sqlite", help="SQLite database path")
    parser.add_argument("--question", help="Natural language question (omit for interactive)")
    parser.add_argument("--allow-write", action="store_true", help="Open the SQLite database read-write instead of read-only")
    args = parser.parse_args()

    if args.db == "demo.sqlite" and not os.path.exists("demo.sqlite"):
        print("🏗️  Creating demo e-commerce database...")
        create_demo_database("demo.sqlite")

    agent, db = build_agent(args.db, read_only=not args.allow_write)
    print(f"\n📊 Connected to: {args.db}")
    print(f"🔒 Mode: {'read-write' if args.allow_write else 'read-only'}")
    print(f"📋 Tables: {', '.join(db.get_table_names())}\n")

    if args.question:
        print(f"❓ Question: {args.question}")
        result = agent.invoke({"input": args.question})
        print(f"\n✅ Answer: {result['output']}")
    else:
        print("💬 SQL Agent ready. Ask questions in natural language. Type 'quit' to exit.\n")
        while True:
            question = input("You: ").strip()
            if question.lower() in ("quit", "exit", "q"):
                break
            if not question:
                continue
            result = agent.invoke({"input": question})
            print(f"\nAgent: {result['output']}\n")


if __name__ == "__main__":
    main()
