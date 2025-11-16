# PydanticOutputParser – Complete Study & Revision Notes

# 1. **What is PydanticOutputParser?**

`PydanticOutputParser` is a LangChain parser that:

- Takes JSON text (usually from LLM output)
- Validates it against a Pydantic model
- Returns a Python object if valid
- Raises detailed errors if validation fails

Useful when you want **strict structured output** from LLMs or want to **validate JSON manually**.

---

# 2. **Correct Syntax for LangChain 1.x**

LangChain 1.x **removed** `from_model()` method. The correct usage is:

```python
parser = PydanticOutputParser(pydantic_object=Person)
```

This is the only valid way in LangChain 1.x.

---

# 3. **Common PydanticOutputParser Workflow**

## 3.1 Create a Pydantic model

```python
class Person(BaseModel):
    name: str
    age: int
    city: str
```

## 3.2 Create parser

```python
parser = PydanticOutputParser(pydantic_object=Person)
```

## 3.3 Insert format instructions into prompt safely

Use a variable placeholder:

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "Return ONLY valid JSON.\n\n{instructions}")
])
```

Inject instructions:

```python
chain = prompt.partial(instructions=parser.get_format_instructions()) | llm | parser
```

---

# 4. **Why you must NOT directly embed format instructions**

If you put:

```python
("human", f"{parser.get_format_instructions()}")
```

LangChain sees `{key}` patterns inside JSON schema and treats them as **template variables**, causing errors like:

```
KeyError: missing variable 'foo'
```

So always use `{instructions}` + `.partial()`.

---

# 5. **PydanticOutputParser Without LLM (validation examples)**

## 5.1 Valid JSON

```python
parser.parse('{"name": "Amey", "age": 25, "city": "Pune"}')
```

→ Works.

---

## 5.2 Missing fields

```python
{"name": "Amey", "age": 25}
```

❗ Error: `city is required`

---

## 5.3 Wrong types

```python
{"name": "Amey", "age": "twenty", "city": "Pune"}
```

❗ Error: "age must be integer"

---

## 5.4 Invalid JSON

```python
{name: "Amey"}
```

❗ JSONDecodeError

---

## 5.5 Malformed JSON

Missing closing brace generates decode error.

---

# 6. **Extra Fields in Pydantic v2**

By default, extra fields are **allowed** and silently ignored.

Example:

```python
{"name":"Amey", "age":25, "city":"Pune", "country":"India"}
```

Output ignores `country`.

## To forbid extra fields

```python
class Person(BaseModel):
    name: str
    age: int
    city: str
    model_config = {"extra": "forbid"}
```

Now extra fields raise:

```
ValidationError: Extra inputs are not permitted
```

---

# 7. **Recommended Alternative in LangChain 1.x**

Use:

```python
model = ChatOpenAI().with_structured_output(Person)
```

Then:

```python
result = model.invoke("Generate a person")
```

Advantages:

- No prompt engineering

- No format instructions

- No parser chaining

- Auto-validation



# 8. **When to Use PydanticOutputParser**

- When LLM output must follow **strict schema**
- When building **APIs** or **production systems**
- When validating user or model input
- When converting raw JSON into Python objects



# **Advanced Tips**

- Combine with retry logic for invalid JSON
- Use nested Pydantic models to parse complex LLM outputs
- Use custom validators for domain-specific rules

Example custom validator:

```python
class Person(BaseModel):
    name: str
    age: int
    city: str

    @field_validator("age")
    def check_age(cls, v):
        if v < 0:
            raise ValueError("Age cannot be negative")
        return v
```

---

#

---



