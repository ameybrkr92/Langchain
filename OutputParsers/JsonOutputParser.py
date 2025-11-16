import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

#Create a model
llm_model = ChatOpenAI()

#Create a Json Parser
parser = JsonOutputParser()
'''
#Create a prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("human", """
     Provide details of a person in the following JSON format:
     {{
         "name":string,
         "age": number,
         "city":string
    
     }}
     Return ONLY valid JSON. No extra text.
     """
     )
])

#chain = prompt | llm_model | parser
#result = chain.invoke({})
#print(result)
'''

text = """
Here is some JSON:
name: Amey, age: 30, city: Pune
"""

#parser.parse(text)
#langchain_core.exceptions.OutputParserException: Invalid json output

text1 = """
Your result is ready:
{
    "name": "Amey",
    "age": 30,
    "city": "Pune"
}

Thanks!
"""
#parsed = parser.parse(text1)
#print(parsed)
#langchain_core.exceptions.OutputParserException: Invalid json output
#👉 Anything before { causes JSONDecodeError

gd_text = """
{
    "name": "Amey",
    "age": 30,
    "city": "Pune"
}

Thanks!
"""
#parsed = parser.parse(gd_text)
#print(parsed)
#Outpu: {'name': 'Amey', 'age': 30, 'city': 'Pune'}


# Instead of manually writin "Return ONLY valid JSON. No extra text."
#You should let the parser generate its own instructions using ".get_format_instructions" & passing format instruction input variable
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", """
     Provide details of a person.

     {format_instructions}
     """)
]).partial(format_instructions=parser.get_format_instructions())

chain = prompt | llm_model | parser
result = chain.invoke({})
print(result)


'''
Output :
{'name': 'Jane Doe', 'age': 30, 'occupation': 'Software Engineer', 'location': 'San Francisco, CA', 'hobbies': ['reading', 'hiking', 'photography'], 'education': {'degree': "Bachelor's in Computer Science", 'school': 'University of California, Berkeley'}, 'skills': ['Java', 'Python', 'JavaScript', 'SQL'], 'languages': ['English', 'Spanish']}

JsonOutputParser → Forces valid JSON + converts to Python dict

You must instruct LLM: “Return ONLY valid JSON”

Works best with a clear schema (name, age, city)

Final chain: prompt | model | parser


👉 LLMs ALWAYS output plain text.
They never output a real JSON object or any real data structure.

When you parse LLM output with a JSON parser, it converts the LLM’s JSON text into a real programming-language object.
'''