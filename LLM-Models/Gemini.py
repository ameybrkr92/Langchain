import os
from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model

llm = init_chat_model("google_genai:gemini-2.5-flash-lite")
response = llm.invoke("What is Langchain & Langgraph")
print(response.content)