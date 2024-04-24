from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Список для словарных слов
dict_words = [i.strip() for i in open('словарные.txt', encoding="utf-8").readline().split(',')]

# Глобальные переменные для отслеживания текущего слова и пропущенной гласной
word = ""
vowel_index = -1


@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Тест на гласные</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f0f0f0; /* Нежный серый фон */
                font-family: Arial, sans-serif;
            }
            #content {
                text-align: center;
                font-size: 24px;
                background-color: #ffffff; /* Белый фон контейнера */
                padding: 20px;
                border-radius: 10px; /* Закругленные углы */
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Тень */
            }
            button, input {
                font-size: 24px;
                margin: 10px;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover, input:hover {
                background-color: #f0f0f0; /* Нежный серый фон при наведении */
            }
            #resultMessage {
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div id="content">
            <h1>Тест на гласные</h1>
            <button onclick="startTest()">Начать тест</button><br><br>
            <div id="wordContainer"></div><br>
            <input type="text" id="answerInput" placeholder="Введите букву"><br>
            <button onclick="checkAnswer()">Проверить</button><br>
            <p id="resultMessage"></p>
        </div>
        <script>
            function startTest() {
                fetch('/get_word')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('wordContainer').innerText = data.word;
                        document.getElementById('answerInput').value = '';
                        document.getElementById('resultMessage').innerText = '';
                        document.getElementById('wordContainer').style.backgroundColor = 'white';
                    });
            }

            function checkAnswer() {
                let answer = document.getElementById('answerInput').value.toLowerCase();
                fetch('/check_answer', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({answer: answer})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.correct) {
                        document.getElementById('resultMessage').innerText = 'Верно!';
                        document.getElementById('wordContainer').style.backgroundColor = '#d4edda'; /* Нежно-зеленый */
                    } else {
                        document.getElementById('resultMessage').innerText = 'Неверно. Попробуйте еще раз.';
                        document.getElementById('wordContainer').style.backgroundColor = '#f8d7da'; /* Нежно-красный */
                    }
                });
            }
        </script>
    </body>
    </html>
    """


@app.route('/get_word')
def get_word():
    global word, vowel_index
    word = random.choice(dict_words)
    vowels = 'аеёиоуыэюя'  # Гласные буквы русского алфавита
    # Находим индекс случайно выбранной гласной в слове
    vowel_i = [i for i, letter in enumerate(word) if letter.lower() in vowels]
    vowel_index = random.choice(vowel_i)
    word_with = word[:vowel_index] + "_" + word[vowel_index + 1:]
    return jsonify({'word': word_with})


@app.route('/check_answer', methods=['POST'])
def check_answer():
    global word, vowel_index
    data = request.get_json()
    answer = data['answer']
    correct = False
    if answer == word[vowel_index]:
        correct = True
    return jsonify({'correct': correct})


if __name__ == '__main__':
    app.run(debug=True)
