from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)

# Simple chatbot logic
def get_response(user_text):
    text = user_text.lower()
    if "hello" in text or "hi" in text:
        return "Hello! How are you?"
    elif "time" in text:
        return f"Current time is {datetime.datetime.now().strftime('%I:%M %p')}"
    elif "bye" in text or "exit" in text:
        return "Goodbye! Have a nice day."
    else:
        return "You said: " + user_text

# Route for frontend
@app.route("/")
def index():
    return render_template("index.html")

# API endpoint for chatbot
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_text = data.get("message", "")
    reply = get_response(user_text)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
