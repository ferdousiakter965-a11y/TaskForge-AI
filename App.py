import os
from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise Exception("GROQ_API_KEY is missing")

client = Groq(api_key=api_key)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_ai():
    user_task = request.form.get('task')

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Break tasks into steps."},
                {"role": "user", "content": user_task}
            ],
            model="llama-3.3-70b-versatile",
        )

        response_text = chat_completion.choices[0].message.content
        return render_template('index.html', response=response_text)

    except Exception as e:
        return render_template('index.html', error=str(e))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)