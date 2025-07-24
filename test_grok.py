# test_groq.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("MODEL_API_KEY"),
                base_url=os.getenv("MODEL_BASE_URL"))

chat = client.chat.completions.create(
    model=os.getenv("MODEL_NAME"),
    messages=[{"role":"user","content":"Hello from Groq!"}]
)
print(chat.choices[0].message.content)