import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

#Create a model
llm_model = ChatOpenAI()

#class Person
class Person(BaseModel):
    name:str
    age:int
    city:str
#Create a Json Parser
parser = PydanticOutputParser(pydantic_object=Person)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", """
Return the person details in JSON format matching this schema:

{format_instructions}

""")
]).partial(format_instructions=parser.get_format_instructions())
'''
chain = prompt | llm_model | parser

result: Person = chain.invoke({})

# 1. Pydantic object
print(result)

# 2. Convert to Python dict
print(result.model_dump())
'''
'''
Output1
name='John Doe' age=30 city='New York'

Output2
{'name': 'John Doe', 'age': 30, 'city': 'New York'}
'''
'''
1. VALID CASE (no error)
json_text = '{"name": "Rahul", "age": 25, "city": "Pune"}'

result = parser.parse(json_text)
print(result)

Output
name='Rahul' age=25 city='Pune'

2. Missing field → PydanticError
json_text = '{"name": "Rahul", "age": 25}'

parser.parse(json_text)

Output
langchain_core.exceptions.OutputParserException: Failed to parse Person from completion {"name": "Rahul", "age": 25}. Got: 1 validation error for Person    
city Field required [type=missing, input_value={'name': 'Rahul', 'age': 25}, input_type=dict]

3. Wrong type → Pydantic validation error

json_text = '{"name": "Rahul", "age": "twenty", "city": "Pune"}'

parser.parse(json_text)

Output
langchain_core.exceptions.OutputParserException: Failed to parse Person from completion {"name": "Rahul", "age": "twenty", "city": "Pune"}. Got: 1 validation error for Person
age Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='twenty', input_type=str]


#4. Extra fields → Error (because model doesn't allow)
                         
json_text = '{"name": "Rahul", "age": 30, "city": "Pune", "country": "India"}'

print(parser.parse(json_text))
Output
name='Rahul' age=30 city='Pune'

Pydantic v2 ALLOWS extra fields by default

That means:
Extra fields are silently ignored
No validation error is raised

To get an error for extra field you will have to update model_congif

class Person(BaseModel):
    name: str
    age: int
    city: str

    model_config = {
        "extra": "forbid"   # 👈 prevents extra fields
    }

'''
