#Document Loader
from langchain_community.document_loaders import PyPDFLoader

pdf_loader = PyPDFLoader("Data Connections\Attention is all you need - Research paper.pdf")

pdf_docs = pdf_loader.load()
    
#Text Splitting
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 200,
    chunk_overlap = 50
)

chunks = splitter.split_documents(pdf_docs)

#embeddings + vector store
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

embedding_model = OpenAIEmbeddings()

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="Data Connections/chroma_db"
) 
#print(help(vectorstore))
#These 5 attributes tell you what is inside:

#✔ _collection
#This is the actual underlying Chroma database collection
#by default langchian explicity names collection as langchain, 
#you can set parameter while defining vectorestore to rename it to something else
print(vectorstore._collection)
#Output: Collection(name=langchain)

#to see documents
#This returns metadata for each stored document chunk.
#data_stored=vectorstore._collection.get()
#print(data_stored)

#If you want only embeddings:
data_stored=vectorstore._collection.get(include=["embeddings"])
#print((data_stored))

#If you want embeddings, docs & matadata:
'''
data_stored=vectorstore._collection.get(include=["embeddings", "documents", "metadatas"])
print((data_stored))
'''

#To see only the IDs
#print(vectorstore._collection.get()["ids"])

#to see how many vectors are stored
print(len(vectorstore._collection.get()["ids"]))