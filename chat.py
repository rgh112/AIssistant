# Import the Flask class from the flask module
from flask import Flask, render_template, request, jsonify

import openai
from flask_cors import CORS
from dotenv import load_dotenv

import os
from googleapiclient.discovery import build

load_dotenv("./.env")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize the Google Search API client
def google_search(search_query, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_query, cx=cse_id, **kwargs).execute()
    return res['items']

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


# Handle requests to the home page
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/Aissistant1.html")
def index():
    return render_template("Aissistant1.html")

@app.route("/Aissistant2.html")
def fake():
    return render_template("Aissistant2.html")

@app.route("/Aissistant3.html")
def fixed2():
    return render_template("Aissistant3.html")

@app.route("/Aissistant4.html")
def fake2():
    return render_template("Aissistant4.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        # Get the question from the POST request
        question = request.form["question"]
        print(f"Received question: {question}")

        question_translated = question  # Initialize to handle cases that are not translation
        
        if question.startswith('translate to '):
            prefix, text_to_translate = question.split(": ", 1)
            language = prefix.split(" ")[2]
            question_translated = f"Translate the following text to {language}: {text_to_translate}"
            print(f"Question to be sent to API: {question_translated}")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question_translated},
            ],
        )
        
        answer = response["choices"][0]["message"]["content"]
        return jsonify({"answer": answer})

    except Exception as e:
        print(f"An exception occurred: {e}")
        return jsonify({"error": str(e)})

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)