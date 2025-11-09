# (1) Verbose / role-based templates — older but explicit.
# Use when you need fine-grained control of system/AI/human messages
# (different templates per role) or want to inspect/modify messages before sending.
# Slightly more boilerplate; .to_messages() produces the messages list for model.invoke().

""""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, AIMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

load_dotenv()
model = ChatOpenAI()

system_template="You are an AI recipe assistant that specializes in {dietary_preference} dishes that can be prepared in {cooking_time}."
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
human_template="{recipe_request}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
# get a chat completion from the formatted messages

prompt = chat_prompt.format_prompt(cooking_time="15 min", dietary_preference="Vegan", recipe_request="Quick Snack").to_messages()
response=model.invoke(prompt)
print(response.content)
"""

#Above LangChain code is outdated compared to the latest LangChain and best practices.
#You can now directly use ChatPromptTemplate with placeholders and pass it to the model without manually creating individual message templates(like systemtemplate, humantemplate, AItemplate).

#from_messages() → structured, multi-role, your case 
#from_template() → simple, single message

#Below we have used .from_template()



# (2) Single-template + composable pipeline (ChatPromptTemplate.from_template).
# Modern, compact pattern. Great for simple prompts and reuse.
# Works well with the `prompt | model` pipeline for clean composition.
# Use this for most simple use-cases where per-role customization isn't needed.

""""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")  # or gpt-4-turbo, gpt-3.5-turbo, etc.

prompt = ChatPromptTemplate.from_template(
    "You are an AI recipe assistant that specializes in {dietary_preference} dishes "
    "that can be prepared in {cooking_time}. "
    "Suggest a recipe for {recipe_request}."
)

chain = prompt | model  # composable pipeline
response = chain.invoke({
    "cooking_time": "15 min",
    "dietary_preference": "Vegan",
    "recipe_request": "Quick Snack"
})

print(response.content)

"""



# (3) Hybrid: define multi-role template then format to messages.
# Cleaner than (1) because you don't manually create System/AI/Human templates,
# but still explicit — useful if you want to format and then inspect messages.
# Good for debugging or when you need the messages object for other tooling.

""""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()

model = ChatOpenAI()

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI recipe assistant specializing in {dietary_preference} dishes that can be made in {cooking_time}."),
    ("human", "{recipe_request}")
])

messages = chat_prompt.format_messages(
    cooking_time="15 min",
    dietary_preference="Vegan",
    recipe_request="Quick Snack"
)

response = model.invoke(messages)
print(response.content)
"""




# (4) Recommended modern pattern: multi-role prompt + pipeline composition.
# Combines clarity of role-based prompts with the brevity and composability of `|`.
# Best for production: pass a dict to chain.invoke(), less boilerplate, easy to extend.

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI recipe assistant specializing in {dietary_preference} dishes that can be made in {cooking_time}."),
    ("human", "{recipe_request}")
])

chain = chat_prompt | model

response = chain.invoke({
    "cooking_time": "15 min",
    "dietary_preference": "Vegan",
    "recipe_request": "Quick Snack"
})

print(response.content)
