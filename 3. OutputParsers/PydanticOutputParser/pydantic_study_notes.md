# Pydantic – Complete Study & Revision Notes

# 1. **What is Pydantic?**

Pydantic is a Python library used to:

- Validate data
- Enforce types
- Parse JSON
- Build structured models (similar to dataclasses, but stricter)
- Automatically throw errors when data is invalid

Pydantic is used heavily with:

- FastAPI
- LangChain
- Data pipelines
- AI/LLM structured responses

Current version used by LangChain: **Pydantic v2**.

---

# 2. **Basic Pydantic Model**

```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
    city: str
```

Now you can create objects AND validate:

```python
p = Person(name="Amey", age=25, city="Pune")
```

Invalid values cause automatic validation errors.

---

# 3. **Automatic Data Conversion (Type Coercion)**

Pydantic tries to convert values where possible:

```python
Person(name="Amey", age="25", city="Pune")
```

✔️ age becomes int 25.

But impossible conversions fail:

```python
Person(name="Amey", age="twenty", city="Pune")
```

❌ ValidationError

---

# 4. **Validation Errors Examples**

## 4.1 Missing field

```python
Person(name="Amey", age=25)
```

❌ city is required

## 4.2 Wrong type

```python
Person(name="Amey", age="abc", city="Pune")
```

❌ Age must be integer

## 4.3 Null not allowed

```python
Person(name=None, age=20, city="Pune")
```

❌ None not allowed for `str`

---

# 5. **Extra Fields in Pydantic v2**

By default extra fields are **allowed** and are ignored.

```python
Person(name="Rahul", age=25, city="Pune", country="India")
```

✔️ No error ✔️ `country` is silently ignored

## To forbid extra fields

```python
class Person(BaseModel):
    name: str
    age: int
    city: str

    model_config = {"extra": "forbid"}
```

Now:

```python
Person(name="Rahul", age=25, city="Pune", country="India")
```

❌ ValidationError: extra inputs not permitted

## Other options

- `extra = "ignore"` (default)
- `extra = "allow"` (keeps extra data)

---

# 6. **Working With JSON**

Pydantic can parse JSON directly:

```python
Person.model_validate_json('{"name":"Rahul", "age":30, "city":"Pune"}')
```

To dump JSON:

```python
person.model_dump()
person.model_dump_json()
```

---

# 7. **Nested Models**

Pydantic supports nesting.

```python
class Address(BaseModel):
    street: str
    city: str

class User(BaseModel):
    name: str
    address: Address
```

Input:

```python
User(
    name="Amey",
    address={"street": "MG Road", "city": "Pune"}
)
```

✔️ Pydantic automatically converts dict → Address model

---

# 8. **Custom Validators (Pydantic v2 syntax)**

Use `@field_validator`.

```python
from pydantic import field_validator

class Person(BaseModel):
    name: str
    age: int

    @field_validator("age")
    def check_age(cls, v):
        if v < 0:
            raise ValueError("Age cannot be negative")
        return v
```

Now:

```python
Person(name="Rahul", age=-5)
```

❌ Error: age cannot be negative

---

# 9. **Model Configuration (Pydantic v2)**

```python
class MyModel(BaseModel):
    model_config = {
        "extra": "forbid",         # reject extra fields
        "strict": True,              # no type coercion
        "validate_assignment": True  # validate when assigning attributes
    }
```

---

# 10. **Strict Mode**

```python
class A(BaseModel):
    x: int
    model_config = {"strict": True}
```

```python
A(x="10")
```

❌ Error (no coercion allowed)



# 11. **Schema Generation**

Generate JSON schema:

```python
Person.model_json_schema()
```

This is what LangChain uses for format instructions.



# 12. **Pydantic vs Dataclasses**

| Feature           | Dataclass | Pydantic    |
| ----------------- | --------- | ----------- |
| Type enforcement  | ❌ No      | ✔️ Yes      |
| Validation        | ❌ No      | ✔️ Yes      |
| JSON parsing      | ❌ Manual  | ✔️ Built-in |
| Used with FastAPI | ❌ Rarely  | ✔️ Standard |



# 15. **Useful Utility Methods**

```python
obj.model_dump()            # Python dict
obj.model_dump_json()       # JSON string
obj.model_copy(update=...)  # clone with changes
obj.model_validate_json()   # validate JSON input
obj.model_json_schema()     # generate schema
```



# 16. **Mini-Cheatsheet**

```python
class Model(BaseModel):
    field: type
    model_config = {
        "extra": "forbid",   # block extra
        "strict": True,        # strict typing
        "validate_assignment": True
    }

model = Model(field=value)
model.field = new_value    # validated
```

---

#
