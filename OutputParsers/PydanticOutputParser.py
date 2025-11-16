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

chain = prompt | llm_model | parser

result: Person = chain.invoke({})

# 1. Pydantic object
print(result)

# 2. Convert to Python dict
print(result.model_dump())

'''
Output1
name='John Doe' age=30 city='New York'

Output2
{'name': 'John Doe', 'age': 30, 'city': 'New York'}
'''