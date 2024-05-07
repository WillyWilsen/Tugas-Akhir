import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
fewshot_BPMN_JS_input1 = 'fewshot_BPMN_JS/input1.txt'
fewshot_BPMN_JS_output1 = 'fewshot_BPMN_JS/output1.txt'
fewshot_BPMN_JS_input2 = 'fewshot_BPMN_JS/input2.txt'
fewshot_BPMN_JS_output2 = 'fewshot_BPMN_JS/output2.txt'

# Generate BPMN JS
def generate_bpmn_js(file_summarizations):
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
  1. bpmn:participant has each @processRef as a pool
  2. bpmn:messageFlow must connect one pool to another pool by task or event as @sourceRef and @targetRef (every task or event in the different pool must be connected by bpmn:messageFlow)
  3. bpmn:sequenceFlow only connect tasks or events in a pool as @sourceRef and @targetRef (every task or event in the same pool must be connected by bpmn:sequenceFlow)

  Syntax:
  {
    bpmn:definitions: {
      @xmlns:xsi: string | required
      @xmlns:bpmn: string | required
      @xmlns:bpmndi: string | required
      @xmlns:dc: string | required
      @xmlns:di: string | required
      @id: string | required
      @targetNamespace: string | required
      @exporter: string | required
      @exporterVersion: string | required
      bpmn:collaboration: {
        @id: string | required
        bpmn:participant: [
          {
            @id: string | required
            @name: string | required
            @processRef: string | required
          } | required
        ] | required
        bpmn:messageFlow: [
          {
            @id: string | required
            @sourceRef: string | required
            @targetRef: string | required
          } | required
        ] | required
      } | required
      bpmn:process: [
        {
          @id: string | required
          bpmn:laneSet: {
            @id: string | required
          } | required
          bpmn:startEvent: {
            @id: string | required
            @name: string | required
            bpmn:outgoing: string | string[] | required
          } | optional
          bpmn:task: [
            {
              @id: string | required
              @name: string | required
              bpmn:incoming: string | string[] | optional
              bpmn:outgoing: string | string[] | optional
            } | required
          ] | required
          bpmn:sequenceFlow: {
            @id: string | required
            @sourceRef: string | required
            @targetRef: string | required
          } | optional
          bpmn:intermediateThrowEvent: {
            @id: string | required
            @name: string | required
          } | optional
          bpmn:exclusiveGateway: {
            @id: string | required
            bpmn:incoming: string | required
            bpmn:outgoing: string[] | required
          } | optional
          bpmn:endEvent: {
            @id: string | required
            @name: string | required
            "bpmn:incoming": string | string[] | required
          }
        } | required
      ] | required
    } | required
  } | required

  Text:
  ''' + ''.join(file_summarizations)

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

  # Validate BPMN JSON
  bpmn_json = json.loads(response['choices'][0]['message']['content'])
  bpmn_participants_ids = []
  bpmn_message_flows_ids = []
  bpmn_start_events_ids = []
  bpmn_tasks_ids = []
  bpmn_sequence_flows_ids = []
  bpmn_intermediate_throw_events_ids = []
  bpmn_exclusive_gateways_ids = []
  bpmn_end_events_ids = []
  if 'bpmn:participant' in bpmn_json['bpmn:definitions']['bpmn:collaboration']:
    # Participants
    bpmn_participants = bpmn_json['bpmn:definitions']['bpmn:collaboration']['bpmn:participant']
    bpmn_participants_ids.extend([participant['@id'] for participant in bpmn_participants])
  if 'bpmn:messageFlow' in bpmn_json['bpmn:definitions']['bpmn:collaboration']:
    # Message Flows
    bpmn_message_flows = bpmn_json['bpmn:definitions']['bpmn:collaboration']['bpmn:messageFlow']
    bpmn_message_flows_ids.extend([message_flow['@id'] for message_flow in bpmn_message_flows])

  for process in bpmn_json['bpmn:definitions']['bpmn:process']:
    # Start Events
    if 'bpmn:startEvent' in process and type(process['bpmn:startEvent']) is dict:
      bpmn_start_events_ids.append(process['bpmn:startEvent']['@id'])
    elif 'bpmn:startEvent' in process and type(process['bpmn:startEvent']) is list:
      bpmn_start_events_ids.extend([start_event['@id'] for start_event in process['bpmn:startEvent']])
    # Tasks
    if 'bpmn:task' in process and type(process['bpmn:task']) is dict:
      bpmn_tasks_ids.append(process['bpmn:task']['@id'])
    elif 'bpmn:task' in process and type(process['bpmn:task']) is list:
      bpmn_tasks_ids.extend([task['@id'] for task in process['bpmn:task']])
    # Sequence Flows
    if 'bpmn:sequenceFlow' in process and type(process['bpmn:sequenceFlow']) is dict:
      bpmn_sequence_flows_ids.append(process['bpmn:sequenceFlow']['@id'])
    elif 'bpmn:sequenceFlow' in process and type(process['bpmn:sequenceFlow']) is list:
      bpmn_sequence_flows_ids.extend([sequence_flow['@id'] for sequence_flow in process['bpmn:sequenceFlow']])
    # Intermediate Throw Events
    if 'bpmn:intermediateThrowEvent' in process and type(process['bpmn:intermediateThrowEvent']) is dict:
      bpmn_intermediate_throw_events_ids.append(process['bpmn:intermediateThrowEvent']['@id'])
    elif 'bpmn:intermediateThrowEvent' in process and type(process['bpmn:intermediateThrowEvent']) is list:
      bpmn_intermediate_throw_events_ids.extend([intermediate_throw_event['@id'] for intermediate_throw_event in process['bpmn:intermediateThrowEvent']])
    # Exclusive Gateways
    if 'bpmn:exclusiveGateway' in process and type(process['bpmn:exclusiveGateway']) is dict:
      bpmn_exclusive_gateways_ids.append(process['bpmn:exclusiveGateway']['@id'])
    elif 'bpmn:exclusiveGateway' in process and type(process['bpmn:exclusiveGateway']) is list:
      bpmn_exclusive_gateways_ids.extend([exclusive_gateway['@id'] for exclusive_gateway in process['bpmn:exclusiveGateway']])
    # End Events
    if 'bpmn:endEvent' in process and type(process['bpmn:endEvent']) is dict:
      bpmn_end_events_ids.append(process['bpmn:endEvent']['@id'])
    elif 'bpmn:endEvent' in process and type(process['bpmn:endEvent']) is list:
      bpmn_end_events_ids.extend([end_event['@id'] for end_event in process['bpmn:endEvent']])

  bpmn_shapes_bpmn_elements = []
  bpmn_edges_bpmn_elements = []
  if 'bpmndi:BPMNDiagram' in bpmn_json['bpmn:definitions']:
    # BPMN Shapes
    if 'bpmndi:BPMNShape' in bpmn_json['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']:
      bpmn_shapes = bpmn_json['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']['bpmndi:BPMNShape']
      bpmn_shapes_bpmn_elements.extend([shape['@bpmnElement'] for shape in bpmn_shapes])
    # BPMN Edges
    if 'bpmndi:BPMNEdge' in bpmn_json['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']:
      bpmn_edges = bpmn_json['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']['bpmndi:BPMNEdge']
      bpmn_edges_bpmn_elements.extend([edge['@bpmnElement'] for edge in bpmn_edges])
  
  # Get bpmn ids that are not in bpmn elements
  bpmn_all_ids = bpmn_participants_ids + bpmn_message_flows_ids + bpmn_start_events_ids + bpmn_tasks_ids + bpmn_sequence_flows_ids + bpmn_intermediate_throw_events_ids + bpmn_exclusive_gateways_ids + bpmn_end_events_ids
  bpmn_all_bpmn_elements = bpmn_shapes_bpmn_elements + bpmn_edges_bpmn_elements  
  bpmn_ids_not_in_bpmn_elements = [bpmn_id for bpmn_id in bpmn_all_ids if bpmn_id not in bpmn_all_bpmn_elements]

  return result