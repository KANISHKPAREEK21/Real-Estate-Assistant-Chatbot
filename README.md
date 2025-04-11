# Real Estate Assistant Chatbot

A multi-agent intelligent chatbot that understands both text and images to help with real estate conversations — powered by OpenAI's GPT-4o (vision) model and built using Streamlit.

🔗 Live App: https://real-estate-assistant-chatbot.streamlit.app/  
📦 GitHub Repo: https://github.com/KANISHKPAREEK21/Real-Estate-Assistant-Chatbot

---

##  Features

-  Chat-based interface
-  Multi-Agent Threaded Conversations (persistent history)
-  Image Upload & Interpretation (property images, blueprints, etc.)
-  Dynamic File Uploads (even mid-conversation)
-  Code Interpreter (via OpenAI Assistant API)
-  Sidebar Session History (continue past chats)

---

## Tech Stack

| Tool               | Purpose                               |
|--------------------|----------------------------------------|
| Streamlit          | UI frontend (chat app, file upload)    |
| OpenAI GPT-4o      | LLM + Vision + Code Interpreter        |
| Assistant API v2   | Agent orchestration and thread mgmt    |
| Python (OpenAI SDK)| API interactions and stream handling   |

---

## Agent Switching Logic

This app uses OpenAI’s Assistant API with GPT-4o (vision enabled). Here's how agent logic is managed:

- Each new conversation creates a new thread using Assistant API.
- You can switch between threads using the sidebar (just like ChatGPT).
- File uploads (images) are added to the assistant’s code interpreter.
- The assistant dynamically understands text + image context and generates output accordingly.
- If a new image is uploaded mid-conversation, it’s immediately uploaded to OpenAI and the assistant is informed.

---

## 🖼️ Image-Based Issue Detection

When a user uploads a real estate-related image like:

- Property photos
- Floor plans
- Site maps
- Blueprints
- Damage spots (e.g., damp walls, cracks)

The assistant:

1. Uploads the file to OpenAI using their file endpoint.
2. Assigns it to the assistant’s code interpreter.
3. Processes the image context via GPT-4o Vision model.
4. Provides insights, suggestions, or analysis.

This enables contextual replies like:

> “The uploaded image appears to show water damage in the left corner. You may need structural inspection.”

---

## Use Case Examples

- Get insights on an uploaded property image
- Ask for price trends in a region
- Upload blueprint and ask about room dimensions
- Upload image mid-conversation and ask “What does this issue indicate?”
- Continue an earlier conversation from the sidebar

---

## How to Access

Visit the live app here:

https://real-estate-assistant-chatbot.streamlit.app/

Or run it locally:

1. Clone the repo:
   git clone https://github.com/KANISHKPAREEK21/Real-Estate-Assistant-Chatbot

2. Install requirements:
   pip install -r requirements.txt

3. Add your OpenAI API key inside main.py or use environment variable.

4. Run the app:
   streamlit run main.py

---

## Contact

Created by Kanishk Pareek  
Feel free to connect or contribute via issues & PRs on GitHub!
Email : kanishkpareek26@gmail.com