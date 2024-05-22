import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
fewshot_BPMN_JS_input1 = 'fewshot_BPMN_JS/input1.txt'
fewshot_BPMN_JS_output1 = 'fewshot_BPMN_JS/output1.txt'
fewshot_BPMN_JS_input2 = 'fewshot_BPMN_JS/input2.txt'
fewshot_BPMN_JS_output2 = 'fewshot_BPMN_JS/output2.txt'

# Generate BPMN JS
def generate_bpmn_js(summary):
  # Few-shot BPMN Learning
  with open(fewshot_BPMN_JS_input1, 'r') as file:
    fewshot_BPMN_JS_input1_text = file.read()
  with open(fewshot_BPMN_JS_output1, 'r') as file:
    fewshot_BPMN_JS_output1_text = file.read()
  with open(fewshot_BPMN_JS_input2, 'r') as file:
    fewshot_BPMN_JS_input2_text = file.read()
  with open(fewshot_BPMN_JS_output2, 'r') as file:
    fewshot_BPMN_JS_output2_text = file.read()

  # BPMN
  system_msg = 'You are an assistant who is very skilled in creating Business Process Model and Notation (BPMN) in JSON format to understand the process of a legal document. You will help me in creating a complete BPMN from the document summarization I provide.'
  user_msg = '''
  Create a BPMN in the following JSON format!

  Rules:
  1. bpmn:participant has each @processRef as a swimlane
  2. bpmn:messageFlow must connect one swimlane to another swimlane by task or event as @sourceRef and @targetRef (every task or event in the different swimlane must be connected by bpmn:messageFlow)
  3. bpmn:sequenceFlow only connect tasks or events in a swimlane as @sourceRef and @targetRef (every task or event in the same swimlane must be connected by bpmn:sequenceFlow)
  4. Each bpmn:task must have bpmn:sequenceFlow or bpmn:messageFlow element at least once as source and once as target.
  5. output can only have one bpmn:startEvent as the opening BPMN and one bpmn:endEvent as the closing BPMN

  Syntax:
  {
    bpmn:definitions: {
      @xmlns:xsi
      @xmlns:bpmn
      @xmlns:bpmndi
      @xmlns:dc
      @xmlns:di
      @id
      @targetNamespace
      @exporter
      @exporterVersion
      bpmn:collaboration: {
        @id
        bpmn:participant: [
          {
            @id
            @name
            @processRef
          }
        ]
        bpmn:messageFlow: [
          {
            @id
            @sourceRef
            @targetRef
          }
        ]
      }
      bpmn:process: [
        {
          @id
          bpmn:laneSet: {
            @id
          }
          bpmn:startEvent: {
            @id
            @name
            bpmn:outgoing:
          }
          bpmn:task: [
            {
              @id
              @name
              bpmn:incoming
              bpmn:outgoing
            }
          ]
          bpmn:sequenceFlow: {
            @id
            @sourceRef
            @targetRef
          }
          bpmn:intermediateThrowEvent: {
            @id
            @name
          }
          bpmn:exclusiveGateway: {
            @id
            bpmn:incoming
            bpmn:outgoing
          }
          bpmn:endEvent: {
            @id
            @name
            bpmn:incoming
          }
        }
      ]
    }
  }

  Text:
  ''' + summary
  
  # Get response
  response = openai.ChatCompletion.create(
    model="gpt-4-turbo",
    response_format={ "type": "json_object" },
    messages=[
      {"role": "system", "content": system_msg},
      {"role": "user", "content": fewshot_BPMN_JS_input1_text},
      {"role": "assistant", "content": fewshot_BPMN_JS_output1_text},
      {"role": "user", "content": fewshot_BPMN_JS_input2_text},
      {"role": "assistant", "content": fewshot_BPMN_JS_output2_text},
      {"role": "user", "content": user_msg}
    ]
  )
  print(response)
  result = response['choices'][0]['message']['content']

  return result