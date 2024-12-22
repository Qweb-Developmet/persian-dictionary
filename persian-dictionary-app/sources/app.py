from flask import Flask, request, jsonify, render_template, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'persian_dictionary.db'

def get_db():
    try:
        conn = sqlite3.connect(DATABASE)
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setup')
def setup():
    conn = get_db()
    if conn is None:
        return "Database connection error."
    cursor = conn.cursor()
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            persian_word TEXT NOT NULL,
            english_translation TEXT NOT NULL,
            part_of_speech TEXT NOT NULL
        )
        ''')
        predefined_words = [
            ("کتاب", "book", "noun"),
            ("خانه", "house", "noun"),
            ("مدرسه", "school", "noun"),
            ("دانشگاه", "university", "noun"),
            ("دوست", "friend", "noun"),
            ("سیب", "apple", "noun"),
            ("میز", "table", "noun"),
            ("صندلی", "chair", "noun"),
            ("درخت", "tree", "noun"),
            ("گل", "flower", "noun"),
            ("زیبا", "beautiful", "adjective"),
            ("سریع", "fast", "adjective"),
            ("آرام", "calm", "adjective"),
            ("بزرگ", "big", "adjective"),
            ("کوچک", "small", "adjective"),
            ("به سرعت", "quickly", "adverb"),
            ("آرام", "slowly", "adverb"),
            ("به خوبی", "well", "adverb"),
            ("به سختی", "hardly", "adverb"),
            ("به طور کامل", "completely", "adverb"),
            ("دویدن", "run", "verb"),
            ("خوردن", "eat", "verb"),
            ("نوشیدن", "drink", "verb"),
            ("خوابیدن", "sleep", "verb"),
            ("خواندن", "read", "verb"),
            ("پرواز", "fly", "verb"),
            ("شنا", "swim", "verb"),
            ("نوشتن", "write", "verb"),
            ("گفتن", "say", "verb"),
            ("دیدن", "see", "verb"),
            ("شنیدن", "hear", "verb"),
            ("لمس کردن", "touch", "verb"),
            ("بوییدن", "smell", "verb"),
            ("چشیدن", "taste", "verb"),
            ("فکر کردن", "think", "verb"),
            ("دانستن", "know", "verb"),
            ("فهمیدن", "understand", "verb"),
            ("یاد گرفتن", "learn", "verb"),
            ("آموختن", "teach", "verb"),
            ("کار کردن", "work", "verb"),
            ("بازی کردن", "play", "verb"),
            ("دوست داشتن", "love", "verb"),
            ("نفرت داشتن", "hate", "verb"),
            ("امید داشتن", "hope", "verb"),
            ("ترسیدن", "fear", "verb"),
            ("خوشحال", "happy", "adjective"),
            ("غمگین", "sad", "adjective"),
            ("عصبانی", "angry", "adjective"),
            ("خسته", "tired", "adjective"),
            ("هیجان زده", "excited", "adjective"),
            ("آرام", "calm", "adjective"),
            ("مضطرب", "anxious", "adjective"),
            ("مطمئن", "confident", "adjective"),
            ("ناامید", "disappointed", "adjective"),
            ("شجاع", "brave", "adjective"),
            ("ترسو", "cowardly", "adjective"),
            ("باهوش", "intelligent", "adjective"),
            ("احمق", "stupid", "adjective"),
            ("سریع", "fast", "adjective"),
            ("کند", "slow", "adjective"),
            ("قوی", "strong", "adjective"),
            ("ضعیف", "weak", "adjective"),
            ("زیبا", "beautiful", "adjective"),
            ("زشت", "ugly", "adjective"),
            ("بلند", "tall", "adjective"),
            ("کوتاه", "short", "adjective"),
            ("چاق", "fat", "adjective"),
            ("لاغر", "thin", "adjective"),
            ("جوان", "young", "adjective"),
            ("پیر", "old", "adjective"),
            ("جدید", "new", "adjective"),
            ("قدیمی", "old", "adjective"),
            ("گرم", "warm", "adjective"),
            ("سرد", "cold", "adjective"),
            ("داغ", "hot", "adjective"),
            ("خنک", "cool", "adjective"),
            ("خشک", "dry", "adjective"),
            ("مرطوب", "wet", "adjective"),
            ("سخت", "hard", "adjective"),
            ("نرم", "soft", "adjective"),
            ("سنگین", "heavy", "adjective"),
            ("سبک", "light", "adjective"),
            ("تمیز", "clean", "adjective"),
            ("کثیف", "dirty", "adjective"),
            ("خوشمزه", "delicious", "adjective"),
            ("بد مزه", "tasteless", "adjective"),
            ("شیرین", "sweet", "adjective"),
            ("تلخ", "bitter", "adjective"),
            ("ترش", "sour", "adjective"),
            ("شور", "salty", "adjective"),
            ("خوشبو", "fragrant", "adjective"),
            ("بدبو", "stinky", "adjective"),
            ("آرام", "quiet", "adjective"),
            ("پر سر و صدا", "noisy", "adjective"),
            ("روشن", "bright", "adjective"),
            ("تاریک", "dark", "adjective"),
        ]
        cursor.executemany('''
        INSERT INTO words (persian_word, english_translation, part_of_speech)
        VALUES (?, ?, ?)
        ''', predefined_words)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database setup error: {e}")
        return "Database setup error."
    finally:
        conn.close()
    return "Database setup completed successfully."

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search_term', '')
    if not search_term:
        return "لطفاً یک کلمه برای جستجو وارد کنید."
    conn = get_db()
    if conn is None:
        return "Database connection error."
    cursor = conn.cursor()
    try:
        cursor.execute('''
        SELECT persian_word, english_translation, part_of_speech
        FROM words
        WHERE persian_word = ? OR english_translation = ?
        ''', (search_term, search_term))
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Search query error: {e}")
        return "Search query error."
    finally:
        conn.close()
    if results:
        response = ""
        for row in results:
            response += f"<div class='dictionary-entry'>"
            response += f"<h2>کلمه: {row[0]}</h2>"
            response += f"<p>ترجمه: {row[1]}</p>"
            response += f"<p>نوع: {row[2]}</p>"
            response += f"</div>"
        return response
    else:
        return "کلمه مورد نظر در فرهنگ لغت موجود نیست."

@app.route('/suggestions')
def suggestions():
    search_term = request.args.get('term', '')
    if not search_term:
        return jsonify([])
    conn = get_db()
    if conn is None:
        return jsonify([])
    cursor = conn.cursor()
    try:
        cursor.execute('''
        SELECT persian_word, english_translation
        FROM words
        WHERE persian_word LIKE ? OR english_translation LIKE ?
        LIMIT 10
        ''', (f'%{search_term}%', f'%{search_term}%'))
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Suggestions query error: {e}")
        return jsonify([])
    finally:
        conn.close()
    suggestions = [f"{row[0]} - {row[1]}" for row in results]
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
