# app.py
import streamlit as st
import requests
import os

# --- Backend API URL ---
# Note: You cannot run the FastAPI backend on Streamlit Cloud like you did in Colab.
# The backend needs to be deployed separately, and its URL hardcoded or fetched.
# For a hackathon, you can deploy the backend (FastAPI + ngrok) on a separate
# machine or service and paste the persistent URL here.
# For this example, let's assume a hardcoded public URL.
# Replace this with your actual, persistent backend URL.
# If you are running both frontend and backend on the same service (e.g. Render, Heroku),
# you would not use ngrok.

# For a Streamlit Cloud deployment, the FastAPI server must be running and exposed
# from a different service. You need to get the public URL from that other service.
# If you want to deploy a single app with both, you'd need a more advanced setup.
# Let's assume you've used your Colab + ngrok to get a URL that you can use for the hackathon.

# A better way would be to create a single app.py that runs all your logic
# instead of having a separate FastAPI backend.
# The following code assumes the API calls are made to an external service.
BACKEND_URL = os.getenv("BACKEND_URL", "https://your-ngrok-backend-url.ngrok-free.app")

st.title("MindMate AI")

mood = st.radio(
    "How are you feeling today?",
    ['calm', 'sad', 'anxious', 'stressed', 'lonely', 'grateful', 'energized']
)
text = st.text_area("Write a few lines about your day...")

# app.py
import streamlit as st
from groq import Groq
import os
import random

# For your hackathon, you can directly set your keys here.
# For best practice, use a secrets file with Streamlit Community Cloud.
GROQ_API_KEY = "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"

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Model to use
GROQ_CHAT_MODEL = "llama-3.3-70b-versatile"

# Quotes Text
quotes_text = """
1. It’s easy to stand in the crowd but it takes courage to stand alone.
2. Loneliness is not lack of company, loneliness is lack of purpose.
... (all your quotes)
"""

# Mood-to-Quote Mapping
mood_to_quotes = {
    "calm": [quotes_text.split('\n')[4], quotes_text.split('\n')[9]],
    "sad": [quotes_text.split('\n')[11], quotes_text.split('\n')[13]],
    "anxious": [quotes_text.split('\n')[24], quotes_text.split('\n')[7]],
    "stressed": [quotes_text.split('\n')[6], quotes_text.split('\n')[19]],
    "lonely": [quotes_text.split('\n')[1], quotes_text.split('\n')[3]],
    "grateful": [quotes_text.split('\n')[10], quotes_text.split('\n')[14]],
    "energized": [quotes_text.split('\n')[0], quotes_text.split('\n')[22]],
}

# Mood-to-Image Mapping (Use public URLs)
mood_to_images = {
    "calm": "https://images.unsplash.com/photo-1549488344-934d402b11e2?q=80&w=1740&auto=format&fit=crop",
    "sad": "https://images.unsplash.com/photo-1534043464124-3be32fe00c02?q=80&w=1740&auto=format&fit=crop",
    "anxious": "https://images.unsplash.com/photo-1549488344-934d402b11e2?q=80&w=1740&auto=format&fit=crop",
    "stressed": "https://images.unsplash.com/photo-1549488344-934d402b11e2?q=80&w=1740&auto=format&fit=crop",
    "lonely": "https://images.unsplash.com/photo-1549488344-934d402b11e2?q=80&w=1740&auto=format&fit=crop",
    "grateful": "https://images.unsplash.com/photo-1549488344-934d402b11e2?q=80&w=1740&auto=format&fit=crop",
    "energized": "https://images.unsplash.com/photo-1549488344-934d402b11e2?q=80&w=1740&auto=format&fit=crop",
}

# Utility Functions
def get_quote_for_mood(mood: str) -> str:
    quotes = mood_to_quotes.get(mood.lower(), [])
    return random.choice(quotes).strip() if quotes else "It's okay to feel what you are feeling."

def groq_text(prompt, model=GROQ_CHAT_MODEL, max_tokens=150, temperature=0.7):
    messages = [
        {"role": "system", "content": "You are MindMate, an empathetic companion for youth mental wellness. Validate feelings in plain language. Offer one small actionable step. Keep under 120 words. Avoid medical claims."},
        {"role": "user", "content": prompt}
    ]
    try:
        response = client.chat.completions.create(
            model=model, messages=messages, max_tokens=max_tokens, temperature=temperature
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error with AI generation: {e}"

# Streamlit App
st.set_page_config(page_title="MindMate AI", layout="wide")
st.title("MindMate AI")

mood = st.radio(
    "How are you feeling today?",
    ['calm', 'sad', 'anxious', 'stressed', 'lonely', 'grateful', 'energized']
)
text = st.text_area("Write a few lines about your day...")

if st.button("Reflect with AI"):
    feelings = text.strip() or f"I'm feeling {mood}"
    with st.spinner("Generating..."):
        # Make direct function calls, no need for API requests
        quote = get_quote_for_mood(mood)
        reply = groq_text(f"Here are some quotes:\n{quotes_text}\nUser says: {feelings}")
        poem = groq_text(f"Write a poem for someone feeling {mood}. Context: {feelings}", max_tokens=200, temperature=0.8)
        img_url = mood_to_images.get(mood.lower(), "")

        st.subheader("MindMate says")
        st.write(reply)

        st.subheader(f"Inspirational Quote for Mood: {mood.capitalize()}")
        st.markdown(f"> {quote}")

        st.subheader("Your Thoughts")
        st.text_area("", value=poem, height=150)

        st.subheader("Calming Image")
        if img_url:
            st.image(img_url, use_container_width=True)
        else:
            st.write("No image available for this mood.")