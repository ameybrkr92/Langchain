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
print(len(pdf_docs))
print(len(chunks))
print(chunks[0].page_content)
print(chunks[50].page_content)
print(chunks[50].metadata)

'''
Why “Recursive”?

Because it splits in a smart way:
Try splitting by paragraph
If still too big, split by sentence
If still too big, split by characters
This avoids cutting sentences in half.

'''