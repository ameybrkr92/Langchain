from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import CSVLoader
from langchain_community.document_loaders import WebBaseLoader

pdf_loader = PyPDFLoader("Data Connections\Attention is all you need - Research paper.pdf")

pdf_docs = pdf_loader.load()

print(pdf_docs)
#print(len(pdf_docs))
#print(pdf_docs[0].page_content)
#print(pdf_docs[1].metadata)

#A Document Loader is simply a tool that brings your data into Python in a consistent format.
'''
Output
[
  Document(page_content="Page 1 text...", metadata={"page": 0}),
  Document(page_content="Page 2 text...", metadata={"page": 1}),
  ...
]

A PDF loader does two simple things:

Opens the PDF

Extracts text page-by-page

LangChain wraps this into a clean API so you don’t worry about PDF internals.

Here is the actual mental model:

📄 PDF → 🔍 Extract text → 📦 Create list of Document objects

Think of each Document as:

page_content: the text

metadata: extra info (page number, file name, etc.)

This is all you need before splitting, embedding, or retrieval.
'''

csv_loader = CSVLoader("Data Connections\penguins.csv")

csv_docs = csv_loader.load()

#print(csv_docs)
#print(len(csv_docs))
#print(csv_docs[0].page_content)
#print(csv_docs[1].metadata)

'''
Each row becomes one Document.

So if your CSV has 100 rows → you get 100 Documents.


'''

web_loader = WebBaseLoader("https://docs.langchain.com/")
web_docs = web_loader.load()

#print(web_docs)
#print(len(web_docs))
#print(web_docs[0].page_content)
#print(web_docs[0].metadata)

'''
Usually you get one Document per webpage.

Super Important Pattern Now

You’ve now learned 3 different loaders, but all of them follow the same flow:

Data Type	  Loader	          What It Produces
PDF	          PyPDFLoader	      Document per page
CSV	          CSVLoader	          Document per row
Website	      WebBaseLoader	      Document per webpage

And all output the same format:
👉 a list of Document objects
'''