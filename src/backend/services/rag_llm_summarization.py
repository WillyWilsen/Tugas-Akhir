import openai
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from PyPDF2 import PdfReader
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

# Extract text from PDF
def extract_text_from_pdf(file):
  reader = PdfReader(file)
  text = ''
  for i, page in enumerate(reader.pages):
    text += page.extract_text()
  return text

# Summarize document
def summarize_document_rag_llm(file, query):
  # Extract file to text
  raw_text = extract_text_from_pdf(file)
  
  # Split the text into chunks
  text_splitter = CharacterTextSplitter(        
    separator = "\n",
    chunk_size = 2000,
    length_function = len,
  )
  texts = text_splitter.split_text(raw_text)

  # Create the document search engine and the QA chain
  embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
  )
  docsearch = FAISS.from_texts(texts, embeddings)
  retriever = docsearch.as_retriever()

  chain = RetrievalQA.from_chain_type(
    llm=OpenAI(model_name="gpt-3.5-turbo-instruct"), 
    chain_type="stuff", 
    retriever=retriever, 
    return_source_documents=False
  )

  # Run the QA chain
  response = chain.run({"query": query})
  print(response)

  return response