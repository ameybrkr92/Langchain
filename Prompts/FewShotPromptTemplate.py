'''
✅Zero-shot = You give no examples, just instructions + input.
'''
# ✅Example: Sentiment classification (Zero-Shot)

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Initialize model
model = ChatOpenAI(model="gpt-4o-mini")

# Create a zero-shot prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sentiment analysis AI that classifies text as Positive, Negative, or Neutral."),
    ("human", "Text: {text}\nClassify the sentiment.")
])

# Format and run
formatted = prompt.format_messages(text="The product quality is amazing and I'm very happy!")
response = model.invoke(formatted)

print(response.content)

'''
✅Few-Shot Example

Few-shot = You give a few examples before the actual task.

'''
#✅ Example: Sentiment classification (Few-Shot)

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,FewShotChatMessagePromptTemplate,ChatMessagePromptTemplate

# Define examples
examples = [
    {"input": "I love the new design!", "output": "Positive"},
    {"input": "The app keeps crashing and it's frustrating.", "output": "Negative"},
    {"input": "It's okay, nothing special though.", "output": "Neutral"},
]

# Define how examples are formatted
example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}"),
])

# Create few-shot template
few_shot_prompt = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
)

# Combine with main system and user messages
final_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sentiment analysis AI. Classify the sentiment as Positive, Negative, or Neutral."),
    few_shot_prompt,
    ("human", "{text}")
])

# Initialize model
model = ChatOpenAI(model="gpt-4o-mini")

# Format and run
formatted = final_prompt.format_messages(text="The service was decent but delivery was late.")
response = model.invoke(formatted)

print(response.content)
