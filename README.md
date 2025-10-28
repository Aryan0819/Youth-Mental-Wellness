💡 Overview & Purpose
MindMate AI is a compassionate and innovative web application designed to support youth mental wellness. In a world where emotional struggles are often faced alone, MindMate offers a safe, private, and accessible space for users to reflect on their feelings.

By providing personalized feedback, inspirational quotes, and calming visuals, it aims to foster a sense of connection and hope. This project was created for the Gen AI Hackathon.

✨ Features
🧠 Mood-Based Reflections: Get an empathetic response from an AI assistant tailored to your specific mood.

📜 Inspirational Quotes: Receive a thoughtfully selected quote that provides encouragement and perspective.

✍️ Personalized Poems: Generate a short, hopeful poem about your day to help you process your emotions.

🖼️ Dynamic Visuals: View a calming image that matches your current emotional state, promoting relaxation.

🛠️ Tech Stack
Frontend: Streamlit - For the interactive web interface.

AI/LLM: Groq API - For high-speed, real-time text generation.

Language: Python

The application’s logic is self-contained in a single app.py file, simplifying deployment and removing the need for a separate backend server.

🚀 Getting Started: Run Locally
You can run this project on your local machine by following these steps.

Prerequisites
Python 3.8 or newer

A Groq API Key. You can get one for free from GroqCloud.

Installation
Clone the repository:

Bash

git clone https://github.com/Aryan0819/Youth-Mental-Wellness.git
(Note: Update the URL if your repository is named differently or under a different user.)

Navigate to the project directory:

Bash

cd Youth-Mental-Wellness
Install the required dependencies:

Bash

pip install -r requirements.txt
Set up your API Key:

Create a folder named .streamlit in the root of your project directory.

Inside that folder, create a file named secrets.toml.

Add your Groq API key to this file:

Ini, TOML

GROQ_API_KEY = "your-api-key-goes-here"
Run the Streamlit app:

Bash

streamlit run app.py
Your app will now be running at http://localhost:8501!

🧑‍💻 About the Developers
This project was built with ❤️ by:

Aryan Raj

Poonam Kashyap

Feel free to connect with us!

GitHub: https://github.com/Aryan0819
        https://github.com/Poonam-Kashyap12
# Youth-Mental-Wellness
