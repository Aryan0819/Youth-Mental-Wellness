import streamlit as st
from groq import Groq
import os
import random

# =============================
# Groq API Configuration
# =============================
# It's better to use Streamlit secrets for this, but for a single file,
# this is a valid approach.
# For production, replace with: GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GROQ_API_KEY = "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"
if not GROQ_API_KEY:
    st.error("Please set GROQ_API_KEY environment variable or use Streamlit secrets.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)
GROQ_CHAT_MODEL = "llama-3.3-70b-versatile"

# =============================
# Quotes Text & Image URLs
# =============================
quotes_text = """
1. It’s easy to stand in the crowd but it takes courage to stand alone.
2. Loneliness is not lack of company, loneliness is lack of purpose.
3. The woman who follows the crowd will usually go no further than the crowd. The woman who walks alone is likely to find herself in places no one has ever been before.
4. The thing that makes you exceptional, if you are at all, is inevitably that which makes you lonely.
5. Time spent undistracted and alone, in self-examination, journaling, meditation, resolves the unresolved and takes us from mentally fat to fit.
6. When they are alone they want to be with others, and when they are with others they want to be alone. After all, human beings are like that.
7. The price of being a sheep is boredom. The price of being a wolf is loneliness. Choose one or the other with great care.
8. Loneliness is a tax we have to pay to atone for a certain complexity of mind.
9. If you are never alone, you cannot know yourself.
10. By all means use sometimes to be alone. Salute thyself; see what thy soul doth wear.
11. We feel alone, and in this we are connected.
12. Every single human being who is alive has felt this kind of pain, hopelessness, and loneliness at one time or another. We are all connected through this shared pain and struggle.
13. Our great depression is our lives. We’ve all been raised on television to believe that one day we’d all be millionaires, and movie gods, and rock stars, but we won’t. We’re slowly learning that fact. And we’re very, very pissed off.
14. The worst part of holding the memories is not the pain. It’s the loneliness of it. Memories need to be shared.
15. Remember never to say that you are alone, for you are not alone; nay, God is within, and your genius is within.
16. Lonely is not being alone, it’s the feeling that no one cares.
17. What a lovely surprise to discover how unlonely being alone can be.
18. If you are afraid of being lonely, don’t try to be right.
19. After 10 years of depression and loneliness, I realized the person I missed the most was not another, but myself.
20. The reality is life is a single-player game. You’re born alone. You’re going to die alone. All of your interpretations are alone. All your memories are alone. You’re gone in three generations and nobody cares. Before you showed up, nobody cared. It’s all single-player.
21. Loneliness isn’t the physical absence of other people, he said – it’s the sense that you’re not sharing anything that matters with anyone else.
22. You cannot be lonely if you like the person you’re alone with.
23. I don’t mind being alone. I just don’t want to be part of the crowd.
24. It is an interesting paradox. Despite the fact that people today are rarely alone, we are increasingly lonely. Michael Easter.
25. He who’s mind is not steady does not find happiness either amongst the people or in the solitude of the forest. When alone, he longs for company, and when in company, he longs for solitude.
26. Although I am a typical loner in my daily life, my awareness of belonging to the invisible community of those who strive for truth, beauty, and justice has prevented me from feelings of isolation.
"""

# Filter out empty lines and whitespace to create a clean list
quotes_list = [line.strip() for line in quotes_text.strip().split('\n') if line.strip()]

# Mood-to-Quote Mapping
# Corrected indices to avoid IndexError
mood_to_quotes = {
    "calm": [quotes_list[4], quotes_list[9], quotes_list[16], quotes_list[21]],
    "sad": [quotes_list[11], quotes_list[13], quotes_list[18]],
    "anxious": [quotes_list[24], quotes_list[6]],
    "stressed": [quotes_list[5], quotes_list[18]],
    "lonely": [quotes_list[1], quotes_list[3], quotes_list[4]],
    "grateful": [quotes_list[9], quotes_list[13]],
    "energized": [quotes_list[0], quotes_list[22], quotes_list[25]],
}

# Mood-to-Image Mapping (Use public URLs)
mood_to_images = {
    "calm": "image/anxiety.jpg",
    "sad": "image/sad.jpeg",
    "anxious": "image/calm 2.jpg",
    "stressed": "image/loneliness.jpg",
    "lonely": "image/loneliness.jpg",
    "grateful": "image/grateful.jpg",
    "energized": "image/eneegized.jpg",
}

# =============================
# Utility Functions
# =============================
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

# =============================
# Streamlit App
# =============================
st.set_page_config(page_title="MindMate AI", layout="wide")
st.title("MindMate AI")

# Added unique keys to prevent StreamlitDuplicateElementId error
mood = st.radio(
    "How are you feeling today?",
    ['calm', 'sad', 'anxious', 'stressed', 'lonely', 'grateful', 'energized'],
    key="mood_radio"
)
text = st.text_area("Write a few lines about your day...", key="day_text_area")

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

        st.subheader("Poem")
        st.text_area("", value=poem, height=150, key="poem_output")

        st.subheader("Calming Image")
        if img_url:
            st.image(img_url, use_container_width=True)
        else:
            st.write("No image available for this mood.")








