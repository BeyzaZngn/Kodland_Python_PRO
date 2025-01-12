import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Veritabanı bağlantısını sağlayan yardımcı işlev
def get_db_connection():
    conn = sqlite3.connect('quiz.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return redirect(url_for('quiz'))

# Quiz Sayfası
@app.route('/quiz')
def quiz():
    username = session.get('username', '')  # Oturumdan kullanıcı adını al
    best_score = 0

    with get_db_connection() as conn:
        questions = conn.execute('SELECT * FROM questions').fetchall()

        if username:  # Eğer kullanıcı adı oturumda varsa
            user = conn.execute('SELECT best_score FROM users WHERE username = ?', (username,)).fetchone()
            best_score = user['best_score'] if user else 0

    return render_template('quiz.html', questions=questions, best_score=best_score)

# Test Gönderimi ve Sonuç
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')  # Formdan kullanıcı adını al
    session['username'] = username  # Kullanıcı adını oturuma kaydet
    score = 0

    with get_db_connection() as conn:
        # Her sorunun doğru cevabını kontrol et
        for key in request.form:
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])
                user_answer = request.form[key]
                correct_answer = conn.execute('SELECT correct_option FROM questions WHERE id = ?', (question_id,)).fetchone()['correct_option']
                if user_answer == correct_answer:
                    score += 10

        # Kullanıcıyı kontrol et ve best_score'u güncelle
        user = conn.execute('SELECT best_score FROM users WHERE username = ?', (username,)).fetchone()

        if user:
            if score > user['best_score']:  # Yeni skor daha yüksekse güncelle
                conn.execute('UPDATE users SET best_score = ? WHERE username = ?', (score, username))
        else:
            # Yeni kullanıcıyı ekle
            conn.execute('INSERT INTO users (username, best_score) VALUES (?, ?)', (username, score))

        # En yüksek skor her zaman hesaplanır
        best_score = max(score, user['best_score'] if user else 0)

    return render_template('result.html', username=username, score=score, best_score=best_score)

# Kullanıcı Skorları Sayfası
@app.route('/scores')
def scores():
    username = session.get('username', '')
    best_score = 0

    with get_db_connection() as conn:
        results = conn.execute('SELECT username, best_score FROM users ORDER BY best_score DESC').fetchall()

        if username:
            user = conn.execute('SELECT best_score FROM users WHERE username = ?', (username,)).fetchone()
            best_score = user['best_score'] if user else 0

    return render_template('scores.html', results=results, best_score=best_score)

if __name__ == '__main__':
    app.run(debug=True)