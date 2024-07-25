import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
fewshot_BPMN_JSON_Generator_input_full = 'fewshot_BPMN_JSON_Generator/input_full.txt'

# Generate BPMN JS
def generate_bpmn_json(texts):
  # Few-shot BPMN Learning
  with open(fewshot_BPMN_JSON_Generator_input_full, 'r') as file:
    fewshot_BPMN_JSON_Generator_input_full_text = file.read()

  # Actors
  system_msg = 'You are an assistant who is very skilled in finding actors of a legal document.'
  user_msg = f'''
  Find the actors in the following sentences!

  ###
  Sentences: """
  (1) InnovateTech discovered information theft. 
  (2) CEO Alex Miller recruits Laura Davis and Michael Turner. 
  (3) CEO Alex Miller founded TechInnovate. 
  (4) TechInnovate mimicked InnovateTech's product and strategy. 
  (5) InnovateTech felt aggrieved and filed a lawsuit. 
  (6) InnovateTech Legal Team involved and court processed law. 
  (7) If TechInnovate is found guilty, court convicts TechInnovate of intellectual property theft.
  """
  Output:
  InnovateTech, CEO Alex Miller, TechInnovate, InnovateTech Legal Team, Court.

  ###
  Sentences: """
  (1) Maju Bangun practice corruption. 
  (2) Budi Santoso persuaded Andi Wijaya. 
  (3) Andi Wijaya accepted bribes. 
  (4) Linda Setiawan becomes a intermediary. 
  (5) Linda Setiawan distributed the bribe money and made transfers to fake companies. 
  (6) Maju Bangun violates construction material standards. 
  (7) Dian Prasetyo knows and being silenced by internal pressure. 
  (8) Rini Susanti as a whistleblower report to Corruption Eradication Commission.
  """
  Output:
  Maju Bangun, Budi Santoso, Andi Wijaya, Linda Setiawan, Dian Prasetyo, Rini Susanti.

  ###
  Sentences: """
  {texts}
  """
  Output:
  '''
  
  # Get response
  response = openai.ChatCompletion.create(
    model="gpt-4-turbo",
    messages=[
      {"role": "system", "content": system_msg},
      {"role": "user", "content": user_msg}
    ]
  )
  print(response)
  actors = response['choices'][0]['message']['content']

  # BPMN
  system_msg = 'You are an assistant who is very skilled in creating Business Process Model and Notation (BPMN) in JSON format to understand the process of a legal document.'
  user_msg = f'''
  {fewshot_BPMN_JSON_Generator_input_full_text}
  Actors: """
  {actors}
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
      {"role": "user", "content": user_msg}
    ]
  )
  print(response)
  result = response['choices'][0]['message']['content']

  return result