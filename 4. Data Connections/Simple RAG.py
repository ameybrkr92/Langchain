#Load → Split → Embed → Store → Retrieve → RAG Chain → Query

#1. Document Loader
from langchain_community.document_loaders import PyPDFLoader,CSVLoader, WebBaseLoader


pdf_docs = PyPDFLoader("Data Connections\Attention is all you need - Research paper.pdf").load()
csv_docs = CSVLoader("Data Connections\penguins.csv").load()
web_docs = WebBaseLoader("https://docs.langchain.com/").load()

all_docs = pdf_docs + csv_docs + web_docs
    
#2. Text Splitting
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 200,
    chunk_overlap = 50
)

chunks = splitter.split_documents(all_docs)

#3. embeddings + vector store
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

embedding_model = OpenAIEmbeddings()

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="Data Connections/chroma_db_all_docs"
) 

#4. retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

# 5. PROMPT TEMPLATE
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
Use ONLY the following context to answer the question.
If the answer is not in the context, say "I don't know".

{format_instructions}

Context:
{context}

Question:
{question}
""")

# 6. OUTPUT PARSER (Pydantic)

from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser

class Answer(BaseModel):
    summary: str
    sources: list[str]

parser = PydanticOutputParser(pydantic_object=Answer)

# 7. LLM + FINAL RAG CHAIN

from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough

llm = ChatOpenAI()

rag_chain = (
    {"context": retriever,
     "question": RunnablePassthrough(),
     "format_instructions": lambda x : parser.get_format_instructions()}
    | prompt
    | llm
    | parser
)

# 8. RUN QUERY

result = rag_chain.invoke("What is the documemt about")
print(result)
