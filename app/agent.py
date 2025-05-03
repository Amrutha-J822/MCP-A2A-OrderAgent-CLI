# app/agent.py

import os
import re
import json
import psycopg2
import requests
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

# URL of your MCP-A2A bridge on Render
A2A_MCP_URL = os.getenv("A2A_MCP_URL").rstrip("/")

# Perplexity API key (fallback extraction)
PERP_KEY = os.getenv("PERPLEXITY_API_KEY")

# Fallback map from user phrasing → actual DB column
COLUMN_MAP = {
    "id":              "id",
    "full name":       "full_name",
    "address":         "address",
    "age":             "age",
    "gender":          "gender",
    "latitude":        "latitude",
    "longitude":       "longitude",
    "email address":   "email_address",
    "order datetime":  "order_datetime",
    "order status":    "order_status",
    "order total":     "order_total",
    "items":           "items",
    "total sales":     "total_sales",
    "order count":     "order_count",
    "rating":          "rating",
    "average rating":  "average_rating"
}


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
    # --- Step 1: Extract name + field via MCP-A2A (preferred) ---
    try:
        prompt = (
            "Extract exactly two things from this request:\n"
            "1) customer_name (the customer's full name)\n"
            "2) column (one of these fields: "
            + ", ".join(COLUMN_MAP.keys())
            + ")\n"
            "Return a JSON object with keys "
            "\"customer_name\" and \"column\".\n"
            f"User: {user_query}"
        )
        a2a = send_a2a_task(prompt)
        tid = a2a["taskId"]
        out = get_a2a_result(tid).get("response") or get_a2a_result(tid).get("content") or get_a2a_result(tid)
        # normalize to string
        raw = out if isinstance(out, str) else json.dumps(out)
        params = json.loads(raw)
        customer_name = params["customer_name"].strip()
        column_key   = params["column"].strip().lower()
        column       = COLUMN_MAP.get(column_key, None)
        if not column:
            raise KeyError(f"Unknown column '{column_key}'")
    except Exception as e:
        # --- Step 2: Fallback parsing ---
        # a) name via regex
        name_patterns = [
            r"(?:status|info|details|data)\s+(?:of|for|about)\s+(.+?)(?:\s+order|\s+'s|\s+$)",
            r"(?:what|where|when|how|show)\s+(?:is|are)\s+(.+?)(?:'s|\s+$)",
            r"(?:lookup|find|get)\s+(.+?)(?:\s+information|\s+data|\s+details|\s+$)"
        ]
        
        customer_name = None
        for pattern in name_patterns:
            m = re.search(pattern, user_query, re.IGNORECASE)
            if m:
                customer_name = m.group(1).strip()
                break
        
        # last-ditch: take first two words as name
        if not customer_name:
            customer_name = " ".join(user_query.split()[:2])
        
        # b) field via keyword map
        uq = user_query.lower()
        column = None
        # longest keys first
        for phrase in sorted(COLUMN_MAP, key=len, reverse=True):
            if phrase in uq:
                column = COLUMN_MAP[phrase]
                break
        # default to order_status
        if not column:
            column = "order_status"

    # --- Step 3: Query your RDS dynamically ---
    try:
        conn = get_connection()
        cur = conn.cursor()
        q = sql.SQL("SELECT {col} FROM customer_orders "
                    "WHERE full_name ILIKE %s "
                    "ORDER BY order_datetime DESC "
                    "LIMIT 1").format(
            col=sql.Identifier(column)
        )
        cur.execute(q, (f"%{customer_name}%",))
        row = cur.fetchone()
        cur.close()
        conn.close()
    except Exception as e:
        return {"error": f"Database error: {e}"}

    # --- Step 4: Build response ---
    if not row:
        return {"message": f"No {column} found for {customer_name}"}

    value = row[0]
    # if datetime, format
    if hasattr(value, "strftime"):
        value = value.strftime("%Y-%m-%dg %H:%M:%S")

    return {
        "customer": customer_name,
        column: value
    }