import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
fewshot_BPMN_JS_input1 = 'fewshot_BPMN_JS/input1.txt'
fewshot_BPMN_JS_output1 = 'fewshot_BPMN_JS/output1.txt'
fewshot_BPMN_JS_input2 = 'fewshot_BPMN_JS/input2.txt'
fewshot_BPMN_JS_output2 = 'fewshot_BPMN_JS/output2.txt'
fewshot_BPMN_JS_input_full = 'fewshot_BPMN_JS/input_full.txt'

# Generate BPMN JS
def generate_bpmn_js(texts):
  # Few-shot BPMN Learning
  with open(fewshot_BPMN_JS_input1, 'r') as file:
    fewshot_BPMN_JS_input1_text = file.read()
  with open(fewshot_BPMN_JS_output1, 'r') as file:
    fewshot_BPMN_JS_output1_text = file.read()
  with open(fewshot_BPMN_JS_input2, 'r') as file:
    fewshot_BPMN_JS_input2_text = file.read()
  with open(fewshot_BPMN_JS_output2, 'r') as file:
    fewshot_BPMN_JS_output2_text = file.read()
  with open(fewshot_BPMN_JS_input_full, 'r') as file:
    fewshot_BPMN_JS_input_full_text = file.read()

  # BPMN
  system_msg = 'You are an assistant who is very skilled in creating Business Process Model and Notation (BPMN) in JSON format to understand the process of a legal document.'
  user_msg = f'''
  {fewshot_BPMN_JS_input_full_text}
  """
  Sentences: """
  {texts}
  """
  Output:
  '''
  
  # Get response
  response = openai.ChatCompletion.create(
    model="gpt-4-turbo",
    response_format={ "type": "json_object" },
    messages=[
      {"role": "system", "content": system_msg},
      # {"role": "user", "content": fewshot_BPMN_JS_input1_text},
      # {"role": "assistant", "content": fewshot_BPMN_JS_output1_text},
      # {"role": "user", "content": fewshot_BPMN_JS_input2_text},
      # {"role": "assistant", "content": fewshot_BPMN_JS_output2_text},
      {"role": "user", "content": user_msg}
    ]
  )
  print(response)
  result = response['choices'][0]['message']['content']

  return result