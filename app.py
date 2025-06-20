from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "AIzaSyCv0hP3D1TFKgzyhOFYUHBZxzEnOPSg3ag"  # Replace with your actual API key
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-email', methods=['POST'])
def generate_email():
    data = request.json
    subject = data.get('subject')
    recipient = data.get('recipient')
    purpose = data.get('purpose')
    instructions = data.get('instructions')
    tone = data.get('tone')
    model = data.get('model')

    prompt = f"""
    Write a {tone} professional email with the following details:
    - Subject: {subject}
    - Recipient: {recipient}
    - Purpose: {purpose}
    - Special Instructions: {instructions}

    The email should have a proper greeting, body, and closing.
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        url = API_URL.format(model=model, key=API_KEY)
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            try:
                email_content = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                return jsonify({"success": True, "email": email_content})
            except (KeyError, IndexError):
                return jsonify({"success": False, "error": "Error parsing response"})
        else:
            return jsonify({"success": False, "error": response.json()})
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)