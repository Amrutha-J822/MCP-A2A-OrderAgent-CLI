# app/agent.py

import os
import re
import psycopg2
import requests
from dotenv import load_dotenv

load_dotenv()

A2A_MCP_URL = os.getenv("A2A_MCP_URL")

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
    # 1) Try regex: "status of X order"
    match = re.search(r"status of\s+(.+?)\s+order", user_query, re.IGNORECASE)
    if match:
        customer_name = match.group(1).strip()
    else:
        # 2) Fallback to MCP-A2A bridge name extraction
        try:
            a2a_resp = send_a2a_task(user_query)
            task_id  = a2a_resp["taskId"]
            result   = get_a2a_result(task_id)
            customer_name = result.get("customer_name", "").strip()
            if not customer_name:
                raise ValueError("Empty customer_name from A2A result")
        except Exception as e:
            return {"error": f"A2A extraction failed: {e}"}

    # 3) Query your RDS for that customer
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("""
            SELECT order_status, order_datetime
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

    # 4) Return result or not-found
    if not row:
        return {"message": f"No orders found for {customer_name}"}

    return {
        "customer":     customer_name,
        "order_status": row[0],
        "order_date":   row[1].strftime("%Y-%m-%d %H:%M:%S")
    }