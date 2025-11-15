import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

#load env variables
load_dotenv()

#initiate model
model = ChatOpenAI()

#get response by invoking the model with a query or prompt
""""
response = model.invoke("Here is a fact about Mars")
print(response.content)

"""

# Output = "Mars is home to the largest volcano in the solar system, Olympus Mons, which stands at nearly 22 kilometers (13.6 miles) high."

# Promt with "f string literal"
"""""
planet = "Pluto"
response = model.invoke(f"Here is a fact about {planet}")
print(response.content)
"""
#Output: Pluto was discovered in 1930 by American astronomer Clyde Tombaugh.

# As you can see this doesn't scale very well , we can use Prompt Template so input variable becomes a parameter call inside prompt template

from langchain_core.prompts import PromptTemplate
#PromptTemplate is used for text completion models or LLM not chatmodels for that we would be using ChatPromptTemplate
""""
prompt_no_input = PromptTemplate(input_variables=[], template= " Tell me a fact about")
print(prompt_no_input.format())
"""
#Output: Tell me a fact about

""""
response = model.invoke(prompt_no_input.format())
print(response.content)
"""
#Output: The world's largest animal is the blue whale, which can grow up to 100 feet in length and weigh over 200 tons.
""""
prompt_single_input = PromptTemplate(input_variables=['topic'], template="Tell me a fact about {topic}")
"""
#print(prompt_single_input.format(topic= "Mars"))

#formatted = prompt_single_input.format(topic = "Ocean")
#either use .format like above or .invoke like below to get formatted template
""""
formatted = prompt_single_input.invoke({"topic": "Mars"})
"""
#get response
""""
response = model.invoke(formatted)
print(response.content)
"""

prompt_multi_input = PromptTemplate(input_variables=['topic','level'], template="Tell me a fact about {topic} for a {level} student")
print(prompt_multi_input)
#input_variables=['level', 'topic'] input_types={} partial_variables={} template='Tell me a fact about {topic} for a {level} student'
print(type(prompt_multi_input))
#<class 'langchain_core.prompts.prompt.PromptTemplate'>

#using .format_prompt or .format
'''
👉 StringPromptTemplate
A base class that defines:
Formatting rules
Template types (f-string, jinja2, mustache)
String-specific behavior

👉 PromptTemplate
A higher-level wrapper that:
Adds input validation (input_variables)
Adds .format() and .format_prompt() helpers
Simplifies usage with LLMs
'''
#strictly speaking, the implementation of format_prompt lives in the base class (StringPromptTemplate). 
# But since PromptTemplate inherits from StringPromptTemplate, you use it as if it were part of PromptTemplate. It’s not exclusive to PromptTemplate, but you will call it on PromptTemplate objects in practice.

formatted_prompt_1=prompt_multi_input.format(topic="Jupiter", level="Graduate")
#or formatted_prompt=prompt_multi_input.format(topic="Jupyter", level ="graduate")
print(prompt_multi_input.format(topic="Jupiter", level="Graduate"))
#text='Tell me a fact about Jupiter for a Graduate student'
print(type(prompt_multi_input.format(topic="Jupiter", level="Graduate")))
#<class 'langchain_core.prompt_values.StringPromptValue'>


formatted_prompt=prompt_multi_input.invoke({'topic':"Jupiter", 'level':"Graduate"})
print(formatted_prompt)
#text='Tell me a fact about Jupiter for a Graduate student'
print(type(formatted_prompt))
#<class 'langchain_core.prompt_values.StringPromptValue'>

response=model.invoke(formatted_prompt)
print(response.content)