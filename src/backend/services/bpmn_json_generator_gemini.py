import openai
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
fewshot_BPMN_JSON_Generator_input_full = 'fewshot_BPMN_JSON_Generator/input_full.txt'

# Generate BPMN JS
def generate_bpmn_json_gemini(texts):
  # Few-shot BPMN Learning
  with open(fewshot_BPMN_JSON_Generator_input_full, 'r') as file:
    fewshot_BPMN_JSON_Generator_input_full_text = file.read()

  # Actors
  model = genai.GenerativeModel('gemini-1.5-pro')
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
  response = model.generate_content(user_msg)
  print(response)
  actors = response.text

  # BPMN
  model = genai.GenerativeModel('gemini-1.5-pro', generation_config={"response_mime_type": "application/json"})
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
  response = model.generate_content(user_msg)
  print(response)
  result = response.text

  return result