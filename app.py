import os
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import speech_recognition as sr
import win32com.client
from dotenv import load_dotenv
from nltk.sentiment.vader import SentimentIntensityAnalyzer  # for sentiment analysis

app = Flask(__name__)
app.secret_key = 'AIzaSyD56PiCHgh4vQp92q60UPnlSKXkLHuzdug'  # Change this to your desired secret key

speaker = win32com.client.Dispatch("SAPI.SpVoice")
chatStr = ""

load_dotenv()
gemini_api_key = os.getenv("API_KEY")

def chat(query):
    global chatStr
    print(chatStr)

    if chatStr:
        # Analyze conversation history and user query for potential techniques
        sentiment_analyzer = SentimentIntensityAnalyzer()
        sentiment = sentiment_analyzer.polarity_scores(query)
        polarity = sentiment['compound']

        # Craft prompt based on conversation history, user query, and sentiment
        prompt = f"User: {query}\nTherapist: {chatStr.split('Therapist: ')[-1]}"  # Get latest therapist response
        if sentiment['compound'] < 0:  # Negative sentiment
            prompt += "\nTherapist: It sounds like you're feeling down. Can you tell me more about what's bothering you?"
        elif any(word in query.lower() for word in ["failure", "worthless"]):  # Negative thoughts
            prompt += "\nTherapist: You mentioned feeling like a failure. Is there evidence to support that thought entirely? Perhaps there are things you're good at that you're not considering."
        else:
            prompt += "\nTherapist: Remember, you're not alone. Talking about how you feel can be helpful. Is there anything you'd like to share?"

        temperature = 0.7
        max_tokens = 256
        top_p = 1.0
        frequency_penalty = 0.0
        presence_penalty = 0.0

        # Make the API call with Gemini specific details (replace with actual implementation)
        response = generate_response(prompt, temperature, max_tokens, top_p, frequency_penalty, presence_penalty)
        model_response = response.get("choices", [{"text": "Consider consulting a licensed therapist for depression management."}])[0]["text"]
        print(f"Therapist: {model_response}")
        speaker.Speak(model_response)
        chatStr += f"Therapist: {model_response}\n"

        # Print sentiment polarity
        print(f"Sentiment Polarity: {polarity:.2f}")  # Format polarity to two decimal places

        return {
            "response": model_response,
            "polarity": polarity
        }

def generate_response(prompt, temperature, max_tokens, top_p, frequency_penalty, presence_penalty):
 
    return {"choices": [{"text": "Replace this with your Gemini API call"}]}

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        print("Listening...")
        query = r.recognize_google(audio, language="en-in")
        return query
    except Exception as e:
        return ""

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat_page():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        user_input = request.form.get('user_input')
        response_data = chat(user_input)
        return render_template('chat.html', response=response_data["response"], polarity=response_data["polarity"])

    return render_template('chat.html', response=None)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    session['username'] = username
    return redirect(url_for('chat_page'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    print('Welcome to AI Therapist\nI am Danny')
    speaker.Speak("Welcome to AI Therapist\nI am Danny")

    # Check if Gemini API key is set in environment variable
    if not gemini_api_key:
        print("Error: Please set the GEMINI_API_KEY environment variable.")
        exit()

    print("Listening...")
    app.run(debug=True)
