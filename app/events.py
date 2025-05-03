from fastapi import APIRouter, Request
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
event_router = APIRouter()

def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

@event_router.post("/amazon-events")
async def ingest_order(request: Request):
    data = await request.json()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO customer_orders (
            full_name, order_status, order_datetime, order_total
        ) VALUES (%s, %s, %s, %s)
    """, (
        data.get("full_name"),
        data.get("order_status"),
        datetime.now(),
        float(data.get("order_total", 0))
    ))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": f"Order inserted for {data.get('full_name')}"}