import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-4.1")
response = model.invoke("What is Langchain & Langgraph")
print(response.content)

