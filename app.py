from flask import Flask, render_template, session, request, jsonify
import random
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app)

words = ["flask", "hangman", "python", "interface", "browser", "developer", "template", "session", "server", "debug"]


@app.route('/')
def index():
    session['word'] = random.choice(words)
    session['guessed'] = []
    session['lives'] = 10
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    letter = request.json.get('letter').lower()
    word = session.get('word')
    guessed = session.get('guessed', [])
    lives = session.get('lives', 10)

    if letter not in guessed:
        guessed.append(letter)
        if letter not in word:
            lives -= 1

    session['guessed'] = guessed
    session['lives'] = lives

    display = [l if l in guessed else "_" for l in word]
    won = "_" not in display
    lost = lives <= 0

    return jsonify({
        'display': " ".join(display),
        'lives': lives,
        'guessed': guessed,
        'won': won,
        'lost': lost,
        'word': word if lost else None
    })

if __name__ == '__main__':
    app.run(debug=True)
