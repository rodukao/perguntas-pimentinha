# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    """Cria a tabela pending_questions, se não existir."""
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pending_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level INTEGER NOT NULL,
            question TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return 'API Admin Questions Running!'

@app.route('/add_question', methods=['POST'])
def add_question():
    data = request.get_json()
    level = data.get('level')
    question = data.get('question')

    if not level or not question:
        return jsonify({"error": "level and question are required"}), 400

    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute('INSERT INTO pending_questions (level, question) VALUES (?,?)', (level, question))
    conn.commit()
    conn.close()

    return jsonify({"message": "Pergunta adicionada com sucesso!"})

@app.route('/list_pending', methods=['GET'])
def list_pending():
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute('SELECT id, level, question FROM pending_questions')
    rows = c.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "level": row[1],
            "question": row[2]
        })

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
