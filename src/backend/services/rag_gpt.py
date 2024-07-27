import openai
import os
import re
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
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
def get_relevant_texts_rag_gpt(file, query):
  # Extract file to text
  raw_text = extract_text_from_pdf(file)

  # Split the text into chunks
  pattern = r"\nPasal \d+\b"
  texts = re.split(pattern, raw_text)

  # Create the document search engine and the QA chain
  embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
  )
  docsearch = FAISS.from_texts(texts, embeddings)
  retriever = docsearch.as_retriever()
  relevant_texts = retriever.get_relevant_documents(query)
  
  texts = ""
  for text in relevant_texts:
    texts += text.page_content + "\n"

  words_to_replace = {
    r'\bPP\s+K\b': 'PPK',
    r'.*www\.peraturan\.go\.id.*\n': ''
  }

  for pattern, replacement in words_to_replace.items():
    texts = re.sub(pattern, replacement, texts)

  return texts