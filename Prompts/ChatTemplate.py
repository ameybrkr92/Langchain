import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, AIMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

load_dotenv()

system_template="You are an AI recipe assistant that specializes in {dietary_preference} dishes that can be prepared in {cooking_time}."
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
SystemMessagePromptTemplate.
Promp