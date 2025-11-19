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