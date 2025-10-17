from flask import Flask, render_template, request, jsonify
import datetime
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)


db_config = {
    'host': 'localhost',
    'user': 'root',          
    'password': 'sukreen',  
    'database': 'chat_messages'
}


def create_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print("Database connection failed:", e)
        return None

def insert_chat(user_msg, bot_reply):
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO chat (user_message, bot_reply) VALUES (%s, %s)"
            cursor.execute(sql, (user_msg, bot_reply))
            conn.commit()
        except Error as e:
            print("Error inserting chat:", e)
        finally:
            cursor.close()
            conn.close()
def get_response(user_text):
    text = user_text.lower().strip()
    if any(greeting in text for greeting in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! I'm your AI assistant. How can I help you today? 😊"
    elif 'time' in text:
        return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}."
    elif 'date' in text or 'today' in text:
        return f"Today's date is {datetime.datetime.now().strftime('%B %d, %Y')}."
    elif 'weather' in text:
        return "I can't access real-time weather data. Please check a weather site."
    elif 'help' in text:
        return "I can help with time, date, greetings, and general chat!"
    elif any(bye in text for bye in ['bye', 'goodbye', 'exit', 'quit']):
        return "Goodbye! Have a nice day! 👋"
    else:
        return f"I heard you say: '{user_text}'. Can you rephrase it?"
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_text = data.get("message", "")
    reply = get_response(user_text)
    insert_chat(user_text, reply)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)

