#Example: Few-Shot Grammar Correction

# Goal → Model learns to fix grammar and avoid changing meaning using a few examples.
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,FewShotChatMessagePromptTemplate,ChatMessagePromptTemplate

# Provide a few examples
examples = [
    {"input": "She go to market yesterday.", "output": "She went to the market yesterday."},
    {"input": "He don't likes mangoes.", "output": "He doesn't like mangoes."},
    {"input": "I am agree with your idea.", "output": "I agree with your idea."},
]

# Define how examples are formatted
example_prompt = ChatPromptTemplate.from_messages([
    ("user", "{input}"),
    ("assistant", "{output}")
])

# Create few-shot prompt
few_shot_template = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
)

# Combine with the main system & user instruction
final_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an English grammar assistant. Correct only grammar and spelling mistakes, don't change the meaning."),
    few_shot_template,
    ("user", "{sentence}")
])

# Initialize the model and run
model = ChatOpenAI(model="gpt-4o-mini")
messages = final_prompt.format_messages(sentence="He go school every day but not on Sundays.")
response = model.invoke(messages)

print(response.content)

# Example: Few-Shot Text → SQL Query Generator

from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    ChatMessagePromptTemplate,
)

# Step 1: Give the model a few demonstrations
examples = [
    {
        "input": "Show all customers from Mumbai.",
        "output": "SELECT * FROM customers WHERE city = 'Mumbai';"
    },
    {
        "input": "List names of employees who earn more than 50000.",
        "output": "SELECT name FROM employees WHERE salary > 50000;"
    },
    {
        "input": "Find total sales for the year 2023.",
        "output": "SELECT SUM(amount) FROM sales WHERE year = 2023;"
    },
]

# Step 2: Format how examples look in chat
example_prompt = ChatPromptTemplate.from_messages([
    ("user", "{input}"),
    ("assistant", "{output}")
])

# Step 3: Create few-shot block
few_shot_template = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
)

# Step 4: Combine into final chat prompt
final_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that converts natural language into SQL queries. Use simple SQL syntax."),
    few_shot_template,
    ("user", "{question}")
])

# Step 5: Run it
model = ChatOpenAI(model="gpt-4o-mini")

messages = final_prompt.format_messages(
    question="Get names of all products priced above 1000."
)
response = model.invoke(messages)

print(response.content)
