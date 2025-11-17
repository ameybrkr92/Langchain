from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("Data Connections\Attention is all you need - Research paper.pdf")

docs = loader.load()

print(docs[1])
print(len(docs))
print(docs[0].page_content)
print(docs[1].metadata)

#A Document Loader is simply a tool that brings your data into Python in a consistent format.