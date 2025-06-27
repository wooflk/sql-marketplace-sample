import psycopg2
from flask import Flask, render_template
import random

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name TEXT,
            description TEXT,
            price NUMERIC,
            category TEXT
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS buy (
            id SERIAL PRIMARY KEY,
            date TEXT,
            name TEXT,
            price NUMERIC
        )
    ''')

    conn.commit()
    cur.close()
    conn.close()



names = ["ultra", "fresh", "glow", "hydra", "clear", "soft", "pure", "silky", "shiny", "bright"]
types = ["cream", "gel", "serum", "oil", "mask", "toner", "cleanser", "lotion", "peeling", "foam"]
descriptions = [
    "perfect for daily care",
    "softens and hydrates skin",
    "deep cleansing effect",
    "gentle on sensitive skin",
    "improves texture and tone",
    "for radiant complexion",
    "removes excess oil",
    "suitable for all types",
    "long-lasting effect",
    "with natural extracts"
]
categories = ["skin", "makeup", "hair", "body", "fragrance", "tools"]

def generate_item():
    name = f"{random.choice(names)} {random.choice(types)}"
    description = random.choice(descriptions)
    price = random.randint(2000, 15000)
    category = random.choice(categories)
    return (name, description, price, category)

items = [generate_item() for _ in range(30)]

conn = psycopg2.connect(
    dbname="items",
    user="postgres",
    password="963600zx",
    host="localhost",
    port="5432"
)
conn.set_client_encoding('WIN1251')
cur = conn.cursor()

cur.executemany('''
    INSERT INTO items (name, description, price, category)
    VALUES (%s, %s, %s, %s)
''', items)

conn.commit()
conn.close()
