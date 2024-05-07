import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
fewshot_BPMN_Sketch_Miner_input1 = 'fewshot_BPMN_Sketch_Miner/input1.txt'
fewshot_BPMN_Sketch_Miner_output1 = 'fewshot_BPMN_Sketch_Miner/output1.txt'
fewshot_BPMN_Sketch_Miner_input2 = 'fewshot_BPMN_Sketch_Miner/input2.txt'
fewshot_BPMN_Sketch_Miner_output2 = 'fewshot_BPMN_Sketch_Miner/output2.txt'

# Generate BPMN Sketch Miner
def generate_bpmn_sketch_miner(file_summarizations):
  # Few-shot BPMN Learning
  with open(fewshot_BPMN_Sketch_Miner_input1, 'r') as file:
    fewshot_BPMN_Sketch_Miner_input1_text = file.read()
  with open(fewshot_BPMN_Sketch_Miner_output1, 'r') as file:
    fewshot_BPMN_Sketch_Miner_output1_text = file.read()
  with open(fewshot_BPMN_Sketch_Miner_input2, 'r') as file:
    fewshot_BPMN_Sketch_Miner_input2_text = file.read()
  with open(fewshot_BPMN_Sketch_Miner_output2, 'r') as file:
    fewshot_BPMN_Sketch_Miner_output2_text = file.read()

  # BPMN
  system_msg = 'You are an assistant who is very skilled in creating Business Process Model and Notation (BPMN) in string format to understand the process of a legal document. You will help me in creating a complete BPMN from the document summarization I provide.'
  user_msg = '''
  Create a BPMN in the following format!

  BPMN Syntax Rules:
  1. One Line One Element: Every element of the diagram corresponds to a line of your text.
  2. First Word is the Element Type: To refine elements, specify their type at the beginning of their line.
  3. Each Element Once: The same element (task or event) only appears once in the visual model, even if it may be repeated in multiple sequences of your text.
  4. Events are in ( ).
  5. Data objects are in [ ].
  6. Pool is a subject that performs actions.

  BPMN Element Mapping:
  Character => BPMN Element
  :         => Pool (Pools visually describe the independent actors and subjects participating in the collaboration. They capture who is involved in the processes and who is in charge of executing each task.)
  ?         => Exclusive Gateway Labels (At a more precise level of details, exclusive gateways may be refined to describe under which conditions their outgoing paths may be taken.)
  |         => Parallel Gateways (Parallel branches indicate where multiple tasks can be concurrently executed.)
  ()        => Events (While tasks represent what needs to be done to achieve the goal of a process, events describe asynchronous interactions between the process and the external world.)
  []        => Data (Data objects represent the input or output of activities.)
  //        => Text Annotations (You can draw text annotation by prefixing them with two slashes //.)
  ///       => Comments (If you use instead three slashes (///) you will be commenting out the line of your text. Commented out lines are ignored by BPMN Sketch Miner and do not affect the diagram.)
  ...       => Fragments (Fragments are used to list incomplete task sequences which should be attached to other task sequences. Use fragments to avoid repeating too many lines in your text.)

  Output Rules:
  1. Output must have only 1 (start Start)
  2. Output must be ended by (finish End)

  Text:
  ''' + ''.join(file_summarizations)

  # Get response
  response = openai.ChatCompletion.create(
    model="gpt-4-turbo",
    messages=[
      {"role": "system", "content": system_msg},
      {"role": "user", "content": fewshot_BPMN_Sketch_Miner_input1_text},
      {"role": "assistant", "content": fewshot_BPMN_Sketch_Miner_output1_text},
      {"role": "user", "content": fewshot_BPMN_Sketch_Miner_input2_text},
      {"role": "assistant", "content": fewshot_BPMN_Sketch_Miner_output2_text},
      {"role": "user", "content": user_msg}
    ]
  )
  print(response)
  result = response['choices'][0]['message']['content']

  return result