import psycopg2
import os
import pandas as pd
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Get DB connection values
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Connect to RDS PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cur = conn.cursor()

# Create full table schema
cur.execute("""
    CREATE TABLE IF NOT EXISTS customer_orders (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255),
        address TEXT,
        age INTEGER,
        gender VARCHAR(10),
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION,
        email_address VARCHAR(255),
        order_datetime TIMESTAMP,
        order_status VARCHAR(100),
        order_total NUMERIC,
        items TEXT,
        total_sales NUMERIC,
        order_count INTEGER,
        rating NUMERIC,
        average_rating NUMERIC
    );
""")

# Load Excel
df = pd.read_excel("customer orders.csv.xlsx")

# Insert each row
for _, row in df.iterrows():
    try:
        cur.execute("""
            INSERT INTO customer_orders (
                full_name, address, age, gender, latitude, longitude, email_address,
                order_datetime, order_status, order_total, items, total_sales,
                order_count, rating, average_rating
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['Full Name'],
            row['Address'],
            int(row['age']) if not pd.isna(row['age']) else None,
            row['gender'],
            float(row['Latitude']) if not pd.isna(row['Latitude']) else None,
            float(row['Longitude']) if not pd.isna(row['Longitude']) else None,
            row['Email Adress'],  # Typo from your Excel header
            pd.to_datetime(row['Order Datetime']),
            row['Order Status'],
            float(row['Order Total']) if not pd.isna(row['Order Total']) else None,
            row['Items'],
            float(row['Total sales']) if not pd.isna(row['Total sales']) else None,
            int(row['Order Count']) if not pd.isna(row['Order Count']) else None,
            float(row['Rating']) if not pd.isna(row['Rating']) else None,
            float(row['Average Rating']) if not pd.isna(row['Average Rating']) else None
        ))
    except Exception as e:
        print(f"❌ Skipping row due to error: {e}")

conn.commit()
cur.close()
conn.close()

print("✅ All rows inserted successfully into RDS!")