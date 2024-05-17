import speech_recognition as sr
import os
import win32com.client
from dotenv import load_dotenv
from nltk.sentiment.vader import SentimentIntensityAnalyzer  # for sentiment analysis

speaker = win32com.client.Dispatch("SAPI.SpVoice")

chatStr = ""

load_dotenv()
# Access Gemini API key from environment variable (more secure)
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
    prompt = f"User: {query}\n  Therapist: {chatStr.split('Therapist: ')[-1]}"  # Get latest therapist response
    if sentiment['compound'] < 0:  # Negative sentiment
      prompt += "\n Therapist: It sounds like you're feeling down. Can you tell me more about what's bothering you?"
    elif any(word in query.lower() for word in ["failure", "worthless"]):  # Negative thoughts
      prompt += "\n Therapist: You mentioned feeling like a failure. Is there evidence to support that thought entirely? Perhaps there are things you're good at that you're not considering."
    else:
      prompt += "\n Therapist: Remember, you're not alone. Talking about how you feel can be helpful. Is there anything you'd like to share?"

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
    chatStr += f"{model_response}\n"

    # Print sentiment polarity
    print(f"Sentiment Polarity: {polarity:.2f}")  # Format polarity to two decimal places

def generate_response(prompt, temperature, max_tokens, top_p, frequency_penalty, presence_penalty):
  # Replace this function with your actual implementation for making a Gemini API call
  # This example function just returns a placeholder message
  # Refer to Gemini API documentation for actual implementation
  return {"choices": [{"text": "Replace this with your Gemini API call"}]}

def takeCommand():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    # Removed noise reduction 
    audio = r.listen(source)
  try:
    print("Listening...")
    query = r.recognize_google(audio, language="en-in")
    return query
  except Exception as e:
    return ""

if __name__ == '__main__':
  print('Welcome to A I Therapist \n I am Danny')
  speaker.Speak("Welcome to A I Therapist \n I am Danny")

  # Check if Gemini API key is set in environment variable
  if not gemini_api_key:
    print("Error: Please set the GEMINI_API_KEY environment variable.")
    exit()

  print("Listening...")

  while True:

    query = takeCommand()

    # Check for exit command
    if "goodbye" in query.lower():
      print("Therapist: Goodbye! Take care.")
      speaker.Speak("Goodbye! Take care.")
      break

    elif "reset chat".lower() in query.lower():
      chatStr = ""

    else:
      chat(query)
