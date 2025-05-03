# app/agent.py

import os
import re
import psycopg2
import requests
from dotenv import load_dotenv

load_dotenv()

# URL of your MCP-A2A bridge
A2A_MCP_URL = os.getenv("A2A_MCP_URL")

# Your Perplexity API key for the fallback
PERP_KEY = os.getenv("PERPLEXITY_API_KEY")


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def send_a2a_task(message: str) -> dict:
    resp = requests.post(
        f"{A2A_MCP_URL}/v1/tools/a2a_send_task",
        headers={"Content-Type": "application/json"},
        json={"message": message}
    )
    resp.raise_for_status()
    return resp.json()


def get_a2a_result(task_id: str) -> dict:
    resp = requests.post(
        f"{A2A_MCP_URL}/v1/tools/a2a_get_task",
        headers={"Content-Type": "application/json"},
        json={"taskId": task_id}
    )
    resp.raise_for_status()
    return resp.json()


async def process_user_query(user_query: str):
    # 1) Regex quick-path: "status of X order"
    m = re.search(r"status of\s+(.+?)\s+order", user_query, re.IGNORECASE)
    if m:
        customer_name = m.group(1).strip()
    else:
        # 2) Try MCP-A2A bridge → Perplexity under the hood
        try:
            a2a = send_a2a_task(user_query)
            tid = a2a["taskId"]
            result = get_a2a_result(tid)
            customer_name = result.get("customer_name", "").strip()
            if not customer_name:
                raise ValueError("empty name from bridge")
        except Exception:
            # 2b) Fallback: direct Perplexity call with Mistral
            try:
                headers = {
                    "Authorization": f"Bearer {PERP_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "mistral-7b-instruct",
                    "messages": [
                        {"role": "system", "content": "Extract the customer's full name from this query."},
                        {"role": "user",   "content": user_query}
                    ]
                }
                resp = requests.post(
                    "https://api.perplexity.ai/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=10
                )
                resp.raise_for_status()
                customer_name = resp.json()["choices"][0]["message"]["content"].strip()
            except Exception as e:
                return {"error": f"Name extraction failed (bridge & mistral): {e}"}

    # 3) Now query your RDS for that customer’s latest order
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT order_status, order_datetime, order_total
            FROM customer_orders
            WHERE full_name ILIKE %s
            ORDER BY order_datetime DESC
            LIMIT 1
        """, (f"%{customer_name}%",))
        row = cur.fetchone()
        cur.close()
        conn.close()
    except Exception as e:
        return {"error": f"Database error: {e}"}

    # 4) Build the response
    if not row:
        return {"message": f"No orders found for {customer_name}"}

    return {
        "customer":     customer_name,
        "order_status": row[0],
        "order_date":   row[1].strftime("%Y-%m-%d %H:%M:%S"),
        "order_total":  float(row[2]) if row[2] is not None else None
    }