# LangChain Prompt Methods Explained

This document summarizes the full conversation about LangChain prompt handling, including:
- Differences between `from_template` and `from_messages`
- Why `format_messages` is needed
- Difference between `format_prompt().to_messages()` and `format_messages()`
- How to inspect what type of message (Human, System) gets returned

---

## 1. Why We Use `format_messages()`
LLM models like `ChatOpenAI` expect **chat messages**, not raw variables.

Example: The model requires something like:
```
[HumanMessage(content="final formatted prompt")]
```
But your dictionary:
```
{"topic": "Mars", "level": "Graduate"}
```
is *not* a valid message.

`format_messages()` converts:
- your template
- your variables

into actual **HumanMessage/SystemMessage objects**.

---

## 2. `from_template` vs `from_messages`

### `from_template()`
Creates a single **HumanMessage** template using one string with placeholders.

Example:
```
prompt = ChatPromptTemplate.from_template(
    "Tell me a fact about {topic} for a {level} student."
)
```
Output becomes:
```
[HumanMessage(...)]
```
Use this for simple prompts.

---

### `from_messages()`
Allows multiple messages with roles:
```
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert tutor."),
    ("human", "Teach {topic} at a {level} level")
])
```
Produces:
```
[SystemMessage(...), HumanMessage(...)]
```
Use this for:
- system + human separation
- agents
- tools
- multi-turn prompts

---

## 3. `format_prompt().to_messages()` vs `format_messages()`
Both produce **the same final message list**, but the process differs.

### `format_prompt()`
Returns a `PromptValue` object.
```
value = prompt.format_prompt(...)
messages = value.to_messages()
```
You can also do:
```
value.to_string()
```
Which gives plain text output.

### `format_messages()`
Direct shortcut:
```
prompt.format_messages(...)
```
Returns `List[BaseMessage]` directly.

**TL;DR**
- `format_prompt()` → for debugging / when you want both `.to_string()` and `.to_messages()`.
- `format_messages()` → when you just want to call the model.

---

## 4. How To Check What Type of Message Is Returned
You can inspect messages using:
```
msgs = prompt.format_messages(...)
print(type(msgs[0]))
```
You will see:
```
<class 'langchain_core.messages.HumanMessage'>
```
If your prompt uses `from_messages()` with a system role, then you will also see:
```
SystemMessage
```

---

## 5. Why chains (`prompt | model`) don't require formatting
When using:
```
chain = prompt | model
chain.invoke(inputs)
```
LangChain *automatically* performs:
```
prompt.format_messages(inputs)
model.invoke(...)
```
So chain syntax hides the formatting steps.

---

Below are expanded examples added throughout the document for deeper clarity.

---

## ✔️ Additional Detailed Examples

### **Example A: Using `from_template()`**
```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "Tell me a fact about {topic} for a {level} student."
)

messages = prompt.format_messages(topic="Jupiter", level="Graduate")
print(messages)
```
**Output:**
```
[HumanMessage(content='Tell me a fact about Jupiter for a Graduate student.')]
```
Here, the message role is always **human**.

---

### **Example B: Using `from_messages()`**
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a science expert. Answer clearly."),
    ("human", "Explain {topic} to a {level} student.")
])

messages = prompt.format_messages(topic="Black Holes", level="Beginner")
print(messages)
```
**Output:**
```
[
  SystemMessage(content='You are a science expert. Answer clearly.'),
  HumanMessage(content='Explain Black Holes to a Beginner student.')
]
```
This shows role separation.

---

### **Example C: `format_prompt().to_messages()`**
```python
value = prompt.format_prompt(topic="Mars", level="Intermediate")
print(value.to_string())
print(value.to_messages())
```
**Output:**
```
Explain Mars to an Intermediate student.
[HumanMessage(content='Explain Mars to an Intermediate student.')]
```
This demonstrates that `.to_string()` gives plain text, `.to_messages()` converts to LLM-ready format.

---

### **Example D: Manual Messages (No Template)**
```python
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")

messages = [
    SystemMessage(content="You are a poet."),
    HumanMessage(content="Write a short poem about rain.")
]

response = model.invoke(messages)
print(response.content)
```
This bypasses templates completely and sends raw messages.

---

### **Example E: Without Chains**
```python
prompt = ChatPromptTemplate.from_template(
    "Give a {adjective} recipe involving {ingredient}."
)

messages = prompt.format_messages(adjective="spicy", ingredient="tofu")
response = model.invoke(messages)
print(response.content)
```
Demonstrates formatting + manual model invocation.

---

### **Example F: With Chains (`|`)**
```python
chain = prompt | model
response = chain.invoke({"adjective": "sweet", "ingredient": "mango"})
print(response.content)
```
Shows how chains automatically apply formatting under the hood.

---

### **Example G: Inspecting Message Types**
```python
msgs = prompt.format_messages(adjective="crispy", ingredient="paneer")
print(type(msgs))        # list
print(type(msgs[0]))     # HumanMessage or SystemMessage
print(msgs[0].__class__)
```
This confirms the message role and class.

---

### **Example H: Complex Multi-message Prompt**
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an interview assistant."),
    ("human", "Ask me an interview question about {topic}.")
])

msgs = prompt.format_messages(topic="Data Structures")
print(msgs)
```
This shows the structure used commonly in agents.

---

This expanded version now includes practical examples demonstrating every concept in a hands-on, ready-to-run format.

