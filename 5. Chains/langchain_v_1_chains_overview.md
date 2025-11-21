# LangChain v1.0 — Chains Overview

> **Contents added:** Code examples for all chain patterns, visual diagrams (ASCII + pointers), a condensed cheatsheet, a full RAG example, and a Router chain example where an LLM routes queries. There's also the screenshot you uploaded embedded below.

## 1. Sequential Chains (Pipeline Chains)

**Definition:** A linear flow of runnables connected using the `|` operator.

**Pattern:**
```
prompt | llm | parser
```

### Minimal Python example (copy-paste ready):
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{question}")
])

llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

chain = prompt | llm | parser

# invoke
resp = chain.invoke({"question": "Explain LC v1.0 in one line."})
print(resp)
```

### When to use
- Single LLM calls
- Summaries, simple transforms, text generation

---

## 2. Branching Chains (RunnableMap) — RAG pattern

**Definition:** Produce a dict of inputs (often combining user input + retrieved context) then feed into prompt → llm → parser.

**Pattern:**
```python
{
  "question": lambda x: x["question"],
  "context": retriever
} | prompt | llm | parser
```

### Practical RAG example (pseudo/ready for your environment):
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.retrievers import RunnableRetriever

# retriever should be a Runnable that accepts input and returns a string/context
retriever = RunnableRetriever(...)  # replace with your retriever implementation

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert that answers using provided context."),
    ("user", "Question: {question}

Context:
{context}")
])
llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

chain = {
    "question": lambda x: x["question"],
    "context": retriever
} | prompt | llm | parser

# invoke with: chain.invoke({"question": "What is the capital of France?"})
```

**Notes:**
- Ensure `retriever` returns concise context strings. The dict keys must match prompt placeholders.

---

## 3. Router Chains (RunnableBranch)

**Definition:** A conditional dispatcher that selects which runnable path runs based on the input.

**Pattern (conceptual):**
```python
RunnableBranch(
    (condition_fn1, chain1),
    (condition_fn2, chain2),
    default_chain
)
```

### Example where an LLM acts as router (two-step):
```python
from langchain_core.runnables import RunnableBranch
from langchain_openai import ChatOpenAI

# simple condition functions
is_math = lambda x: "math" in x.get("question", "").lower()
is_code = lambda x: "code" in x.get("question", "").lower()

# placeholder chains
math_chain = lambda inp: "Run math chain (placeholder)"
code_chain = lambda inp: "Run code chain (placeholder)"
default_chain(inp):
    return "Run default chain"

router = RunnableBranch(
    (is_math, math_chain),
    (is_code, code_chain),
    default_chain
)

# invoke: router.invoke({"question": "How to solve 2+2?"})
```

### LLM-based routing (recommended for semantic routing):
- Use a small prompt to the LLM that returns a routing tag (e.g., `math`, `code`, `general`) and then map tag → chain.

---

## 4. Diagrams (ASCII + explanation)

**Sequential chain (pipeline):**

```
user_input --> [Prompt Runnable] --> [LLM Runnable] --> [Parser Runnable] --> output
```

**Branching (RunnableMap):**

```
user_input --> { "question": fn, "context": retriever } --> [Prompt] --> [LLM] --> [Parser]
```

**Router (RunnableBranch):**

```
user_input --> [Router] --(cond1)--> chain1
                         --(cond2)--> chain2
                         --(else)--> default_chain
```

---

## 5. Condensed Cheatsheet (quick reference)

- **Make a prompt:** `ChatPromptTemplate.from_messages([...])`
- **Make an LLM:** `ChatOpenAI(model="gpt-4o-mini")`
- **Make a parser:** `StrOutputParser()` or structured parsers
- **Make a pipeline:** `prompt | llm | parser`
- **Branching:** return a dict with keys used in the prompt
- **Router:** `RunnableBranch((cond, chain), ...)`
- **Invoke:** `chain.invoke({"question": "..."})`

---

## 6. Full RAG worked example (more detailed pseudocode)

```python
# 1) Embed + vector store retriever
# 2) Retriever returns top-k docs as 'context'
# 3) prompt uses {question} and {context}
# 4) llm returns answer

from langchain_core.retrievers import RunnableRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# assume you have a VectorStore with a runnable retriever
retriever = RunnableRetriever.from_vectorstore(my_vectorstore, top_k=4)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert. Answer using the context below."),
    ("user", "Question: {question}

Context:
{context}")
])
llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

rag_chain = {
    "question": lambda x: x["question"],
    "context": retriever  # returns combined doc string
} | prompt | llm | parser

# usage:
# rag_chain.invoke({"question": "Explain HDFS replication"})
```

---

## 7. Router chain with LLM decision-making (practical pattern)

1. Small prompt to LLM asking for a route label (e.g., `math`, `code`, `research`).
2. Map label → runnable chain.

```python
# 1) Router prompt
routing_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a router that assigns the label: math, code, or general."),
    ("user", "Decide the label for: {question}")
])
router_llm = ChatOpenAI(model="gpt-4o-mini")

# 2) Compose: prompt -> router_llm -> parse label
label_parser = StrOutputParser()
label_chain = routing_prompt | router_llm | label_parser

# 3) label_map
label_map = {
    "math": math_chain,
    "code": code_chain,
    "general": default_chain
}

# 4) runnable that runs label_chain then dispatches
def llm_router(inp):
    label = label_chain.invoke({"question": inp["question"]})
    return label_map.get(label.strip().lower(), default_chain)(inp)

router = llm_router

# invoke: router({"question": "Integrate x^2"})
```

---

## 8. Tips & Best Practices

- Keep runnables small and single-purpose.
- Use parsers to make downstream code deterministic.
- For RAG, sanitize and truncate `context` to avoid token overflow.
- For routers, guard against label drift — keep a small, robust prompt + examples.
- Test each runnable individually before composing.

