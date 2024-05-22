import textwrap
import openai
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
fewshot_summarization_input1 = 'fewshot_summarization/input1.txt'
fewshot_summarization_output1 = 'fewshot_summarization/output1.txt'
fewshot_summarization_input2 = 'fewshot_summarization/input2.txt'
fewshot_summarization_output2 = 'fewshot_summarization/output2.txt'

# Extract text from PDF
def extract_text_from_pdf(file):
  reader = PdfReader(file)
  text = ''
  for i, page in enumerate(reader.pages):
    text += page.extract_text()
  return text

# Summarize document
def summarize_document_llm(file, query):
  # Extract file to text
  text = extract_text_from_pdf(file)
  
  # Few-shot Summarization Learning
  with open(fewshot_summarization_input1, 'r') as file:
    fewshot_summarization_input1_text = file.read()
  with open(fewshot_summarization_output1, 'r') as file:
    fewshot_summarization_output1_text = file.read()
  with open(fewshot_summarization_input2, 'r') as file:
    fewshot_summarization_input2_text = file.read()
  with open(fewshot_summarization_output2, 'r') as file:
    fewshot_summarization_output2_text = file.read()

  # Split text into chunks
  max_tokens = 128000 // 2
  raw_text_chunks = textwrap.wrap(text, width=max_tokens)

  # Process each chunk
  summaries = []
  for chunk in raw_text_chunks:
    system_msg = 'You are a very skilled assistant in summarizing process models from a legal document. You will help me in summarizing the process model from the document I provided.'
    user_msg = f'''
    Summarize the action process model performed by the subject without opening and closing statements from the following document!

    {chunk}

    Query:
    {query}
    '''

    # Get response
    response = openai.ChatCompletion.create(
      model="gpt-4-turbo",
      messages=[
        {"role": "system", "content": system_msg},
        {"role": "user", "content": fewshot_summarization_input1_text},
        {"role": "assistant", "content": fewshot_summarization_output1_text},
        {"role": "user", "content": fewshot_summarization_input2_text},
        {"role": "assistant", "content": fewshot_summarization_output2_text},
        {"role": "user", "content": user_msg}
      ]
    )
    print(response)
    summaries.append(response['choices'][0]['message']['content'])

  return ''.join(summaries)