import psycopg2
from flask import Flask, render_template, request, redirect, url_for
import random
from datetime import datetime

app = Flask(__name__) 

def get_connection():
    return psycopg2.connect(
        dbname="items",
        user="postgres",
        password="963600zx",
        host="localhost",
        port="5432"
    )

@app.route('/', methods=['POST', 'GET'])
def index():
    message = None
    last_bought_id = None

    if request.method == 'POST':
        item_id = request.form.get('item_id')
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT name, price FROM items WHERE id = %s', (item_id,))
        row = cur.fetchone()
        if row:
            now = datetime.now()
            cur.execute(
                'INSERT INTO buy(name, price, date) VALUES (%s, %s, %s)',
                (row[0], row[1], now)
            )
            conn.commit()
            message = f'yipeee! you bougth {row[0]} for {row[1]}.'
            last_bought_id = int(item_id)
        conn.close()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, description, price, category FROM items")
    rows = cur.fetchall()
    conn.close()

    return render_template('index.html', rows=rows, message=message, last_bought_id = last_bought_id)

@app.route('/account')
def account():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT date, name, price FROM buy ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()
    
    return render_template('account.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
