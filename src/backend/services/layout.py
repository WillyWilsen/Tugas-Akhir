import json

def generate_layout(data):
  data = json.loads(data)

  # Find participants with the process
  collaboration_id = None
  participants = {}
  message_flows = []
  if 'bpmn:definitions' in data:
    if 'bpmn:collaboration' in data['bpmn:definitions']:
      collaboration_id = data['bpmn:definitions']['bpmn:collaboration']['@id']
      if 'bpmn:participant' in data['bpmn:definitions']['bpmn:collaboration']:
        if 'bpmn:process' in data['bpmn:definitions']:
          # Loop through participants
          for participant in data['bpmn:definitions']['bpmn:collaboration']['bpmn:participant']:
            # Loop through processes
            for process in data['bpmn:definitions']['bpmn:process']:
              # If process id is equal to participant processRef
              if participant['@processRef'] == process['@id']:
                participants[participant['@id']] = {
                  'bpmn:task': [],
                  'bpmn:startEvent': [],
                  'bpmn:intermediateThrowEvent': [],
                  'bpmn:exclusiveGateway': [],
                  'bpmn:endEvent': [],
                  'bpmn:sequenceFlow': []
                }

                # Find start events in the process
                if 'bpmn:startEvent' in process:
                  if type(process['bpmn:startEvent']) is dict:
                    participants[participant['@id']]['bpmn:startEvent'].append({
                      'id': process['bpmn:startEvent']['@id'],
                    })
                  elif type(process['bpmn:startEvent']) is list:
                    for start_event in process['bpmn:startEvent']:
                      participants[participant['@id']]['bpmn:startEvent'].append({
                        'id': start_event['@id'],
                      })

                # Find exclusive gateways in the process
                if 'bpmn:exclusiveGateway' in process:
                  if type(process['bpmn:exclusiveGateway']) is dict:
                    participants[participant['@id']]['bpmn:exclusiveGateway'].append({
                      'id': process['bpmn:exclusiveGateway']['@id'],
                    })
                  elif type(process['bpmn:exclusiveGateway']) is list:
                    for exclusive_gateway in process['bpmn:exclusiveGateway']:
                      participants[participant['@id']]['bpmn:exclusiveGateway'].append({
                        'id': exclusive_gateway['@id'],
                      })

                # Find tasks in the process
                if 'bpmn:task' in process:
                  if type(process['bpmn:task']) is dict:
                    participants[participant['@id']]['bpmn:task'].append({
                      'id': process['bpmn:task']['@id'],
                    })
                  elif type(process['bpmn:task']) is list:
                    for task in process['bpmn:task']:
                      participants[participant['@id']]['bpmn:task'].append({
                        'id': task['@id'],
                      })

                # Find intermediate throw events in the process
                if 'bpmn:intermediateThrowEvent' in process:
                  if type(process['bpmn:intermediateThrowEvent']) is dict:
                    participants[participant['@id']]['bpmn:intermediateThrowEvent'].append({
                      'id': process['bpmn:intermediateThrowEvent']['@id'],
                    })
                  elif type(process['bpmn:intermediateThrowEvent']) is list:
                    for intermediate_throw_event in process['bpmn:intermediateThrowEvent']:
                      participants[participant['@id']]['bpmn:intermediateThrowEvent'].append({
                        'id': intermediate_throw_event['@id'],
                      })

                # Find end events in the process
                if 'bpmn:endEvent' in process:
                  if type(process['bpmn:endEvent']) is dict:
                    participants[participant['@id']]['bpmn:endEvent'].append({
                      'id': process['bpmn:endEvent']['@id'],
                    })
                  elif type(process['bpmn:endEvent']) is list:
                    for end_event in process['bpmn:endEvent']:
                      participants[participant['@id']]['bpmn:endEvent'].append({
                        'id': end_event['@id'],
                      })

                # Find sequence flows in the process
                if 'bpmn:sequenceFlow' in process:
                  if type(process['bpmn:sequenceFlow']) is dict:
                    participants[participant['@id']]['bpmn:sequenceFlow'].append({
                      'id': process['bpmn:sequenceFlow']['@id'],
                      'sourceRef': process['bpmn:sequenceFlow']['@sourceRef'],
                      'targetRef': process['bpmn:sequenceFlow']['@targetRef'],
                    })
                  elif type(process['bpmn:sequenceFlow']) is list:
                    for sequence_flow in process['bpmn:sequenceFlow']:
                      participants[participant['@id']]['bpmn:sequenceFlow'].append({
                        'id': sequence_flow['@id'],
                        'sourceRef': sequence_flow['@sourceRef'],
                        'targetRef': sequence_flow['@targetRef'],
                      })

          # Loop through message flows
          if 'bpmn:messageFlow' in data['bpmn:definitions']['bpmn:collaboration']:
            if type(data['bpmn:definitions']['bpmn:collaboration']['bpmn:messageFlow']) is dict:
              message_flows.append({
                'id': data['bpmn:definitions']['bpmn:collaboration']['bpmn:messageFlow']['@id'],
                'sourceRef': data['bpmn:definitions']['bpmn:collaboration']['bpmn:messageFlow']['@sourceRef'],
                'targetRef': data['bpmn:definitions']['bpmn:collaboration']['bpmn:messageFlow']['@targetRef'],
              })
            elif type(data['bpmn:definitions']['bpmn:collaboration']['bpmn:messageFlow']) is list:
              for message_flow in data['bpmn:definitions']['bpmn:collaboration']['bpmn:messageFlow']:
                message_flows.append({
                  'id': message_flow['@id'],
                  'sourceRef': message_flow['@sourceRef'],
                  'targetRef': message_flow['@targetRef'],
                })

  # Default BPMN Layout
  distance_each_element = 50
  participant_layout = {
    'width': 50,
    'height': 150
  }
  start_event_layout =  {
    'width': 36,
    'height': 36
  }
  task_layout = {
    'width': 100,
    'height': 80,
  }
  intermediate_throw_event_layout = {
    'width': 36,
    'height': 36
  }
  exclusive_gateway_layout = {
    'width': 50,
    'height': 50
  }
  end_event_layout =  {
    'width': 36,
    'height': 36
  }
  event_label_layout = {
    'width': 36,
    'height': 14
  }
  distance_event_label_to_layout = 7

  # Calculate participant width
  max_width = distance_each_element
  width = distance_each_element
  participant_keys = list(participants.keys())
  for participant_key in participant_keys:
    # Calculate width
    for task in participants[participant_key]['bpmn:task']:
      width += task_layout['width'] + distance_each_element
    for start_event in participants[participant_key]['bpmn:startEvent']:
      width += start_event_layout['width'] + distance_each_element
    for intermediate_throw_event in participants[participant_key]['bpmn:intermediateThrowEvent']:
      width += intermediate_throw_event_layout['width'] + distance_each_element
    for exclusive_gateway in participants[participant_key]['bpmn:exclusiveGateway']:
      width += exclusive_gateway_layout['width'] + distance_each_element
    for end_event in participants[participant_key]['bpmn:endEvent']:
      width += end_event_layout['width'] + distance_each_element
    
    if width > max_width:
      max_width = width
    width = distance_each_element

  participant_layout['width'] = max_width
    

  # Generate BPMN Layout
  x = 50
  y = 0
  BPMNShape = []
  BPMNEdge = []

  for participant_key in participant_keys:
    # Participant Layout
    BPMNShape.append({
      '@id': participant_key + '_di',
      '@bpmnElement': participant_key,
      '@isHorizontal': 'true',
      'dc:Bounds': {
        '@x': 0,
        '@y': str(y),
        '@width': str(participant_layout['width']),
        '@height': str(participant_layout['height'])
      },
      'bpmndi:BPMNLabel': None
    })

    # Start Event Layout
    for start_event in participants[participant_key]['bpmn:startEvent']:
      BPMNShape.append({
        '@id': start_event['id'] + '_di',
        '@bpmnElement': start_event['id'],
        'dc:Bounds': {
          '@x': str(x),
          '@y': str(y + (participant_layout['height'] - start_event_layout['height']) // 2),
          '@width': str(start_event_layout['width']),
          '@height': str(start_event_layout['height'])
        },
        'bpmndi:BPMNLabel': {
          'dc:Bounds': {
            '@x': str(x),
            '@y': str(y + (participant_layout['height'] - start_event_layout['height']) // 2 + start_event_layout['height'] + distance_event_label_to_layout),
            '@width': str(event_label_layout['width']),
            '@height': str(event_label_layout['height'])
          }
        }
      })
      x += start_event_layout['width'] + distance_each_element

    # Exclusive Gateway Layout
    for exclusive_gateway in participants[participant_key]['bpmn:exclusiveGateway']:
      BPMNShape.append({
        '@id': exclusive_gateway['id'] + '_di',
        '@bpmnElement': exclusive_gateway['id'],
        '@isMarkerVisible': 'true',
        'dc:Bounds': {
          '@x': str(x),
          '@y': str(y + (participant_layout['height'] - exclusive_gateway_layout['height']) // 2),
          '@width': str(exclusive_gateway_layout['width']),
          '@height': str(exclusive_gateway_layout['height'])
        }
      })
      x += exclusive_gateway_layout['width'] + distance_each_element

    # Task Layout
    for task in participants[participant_key]['bpmn:task']:
      BPMNShape.append({
        '@id': task['id'] + '_di',
        '@bpmnElement': task['id'],
        'dc:Bounds': {
          '@x': str(x),
          '@y': str(y + (participant_layout['height'] - task_layout['height']) // 2),
          '@width': str(task_layout['width']),
          '@height': str(task_layout['height'])
        },
        'bpmndi:BPMNLabel': None
      })
      x += task_layout['width'] + distance_each_element

    # Intermediate Throw Event Layout
    for intermediate_throw_event in participants[participant_key]['bpmn:intermediateThrowEvent']:
      BPMNShape.append({
        '@id': intermediate_throw_event['id'] + '_di',
        '@bpmnElement': intermediate_throw_event['id'],
        'dc:Bounds': {
          '@x': str(x),
          '@y': str(y + (participant_layout['height'] - intermediate_throw_event_layout['height']) // 2),
          '@width': str(intermediate_throw_event_layout['width']),
          '@height': str(intermediate_throw_event_layout['height'])
        },
        'bpmndi:BPMNLabel': {
          'dc:Bounds': {
            '@x': str(x),
            '@y': str(y + (participant_layout['height'] - intermediate_throw_event_layout['height']) // 2 + intermediate_throw_event_layout['height'] + distance_event_label_to_layout),
            '@width': str(event_label_layout['width']),
            '@height': str(event_label_layout['height'])
          }
        }
      })
      x += intermediate_throw_event_layout['width'] + distance_each_element

    # End Event Layout
    for end_event in participants[participant_key]['bpmn:endEvent']:
      BPMNShape.append({
        '@id': end_event['id'] + '_di',
        '@bpmnElement': end_event['id'],
        'dc:Bounds': {
          '@x': str(x),
          '@y': str(y + (participant_layout['height'] - end_event_layout['height']) // 2),
          '@width': str(end_event_layout['width']),
          '@height': str(end_event_layout['height'])
        },
        'bpmndi:BPMNLabel': {
          'dc:Bounds': {
            '@x': str(x),
            '@y': str(y + (participant_layout['height'] - end_event_layout['height']) // 2 + end_event_layout['height'] + distance_event_label_to_layout),
            '@width': str(event_label_layout['width']),
            '@height': str(event_label_layout['height'])
          }
        }
      })
      x += end_event_layout['width'] + distance_each_element

    y += participant_layout['height']
    x = distance_each_element

  # Sequence Flow Layout
  for participant_key in participant_keys:
    for sequence_flow in participants[participant_key]['bpmn:sequenceFlow']:
      edge = {
        '@id': sequence_flow['id'] + '_di',
        '@bpmnElement': sequence_flow['id'],
        'di:waypoint': []
      }
      source_element = None
      target_element = None
      for element in BPMNShape:
        if element['@bpmnElement'] == sequence_flow['sourceRef']:
          source_element = element['dc:Bounds']
        elif element['@bpmnElement'] == sequence_flow['targetRef']:
          target_element = element['dc:Bounds']

        if (source_element != None and target_element != None):
          break
      
      if (source_element != None and target_element != None):
        if int(source_element['@x']) < int(target_element['@x']):
          edge['di:waypoint'].append({
            '@x': str(int(source_element['@x']) + int(source_element['@width'])),
            '@y': str(int(source_element['@y']) + int(source_element['@height']) // 2)
          })
          edge['di:waypoint'].append({
            '@x': str(int(target_element['@x'])),
            '@y': str(int(target_element['@y']) + int(target_element['@height']) // 2)
          })
        else:
          edge['di:waypoint'].append({
            '@x': str(int(source_element['@x'])),
            '@y': str(int(source_element['@y']) + int(source_element['@height']) // 2)
          })
          edge['di:waypoint'].append({
            '@x': str(int(target_element['@x']) + int(target_element['@width'])),
            '@y': str(int(target_element['@y']) + int(target_element['@height']) // 2)
          })

        BPMNEdge.append(edge)

  # Message Flow Layout
  for message_flow in message_flows:
    edge = {
      '@id': message_flow['id'] + '_di',
      '@bpmnElement': message_flow['id'],
      'di:waypoint': []
    }
    source_element = None
    target_element = None
    for element in BPMNShape:
      if element['@bpmnElement'] == message_flow['sourceRef']:
        source_element = element['dc:Bounds']
      elif element['@bpmnElement'] == message_flow['targetRef']:
        target_element = element['dc:Bounds']

      if (source_element != None and target_element != None):
        break

    if (source_element != None and target_element != None):
      if int(source_element['@y']) < int(target_element['@y']):
        edge['di:waypoint'].append({
          '@x': str(int(source_element['@x']) + int(source_element['@width']) // 2),
          '@y': str(int(source_element['@y']) + int(source_element['@height']))
        })
        edge['di:waypoint'].append({
          '@x': str(int(target_element['@x']) + int(target_element['@width']) // 2),
          '@y': str(int(target_element['@y']))
        })
      else:
        edge['di:waypoint'].append({
          '@x': str(int(source_element['@x']) + int(source_element['@width']) // 2),
          '@y': str(int(source_element['@y']))
        })
        edge['di:waypoint'].append({
          '@x': str(int(target_element['@x']) + int(target_element['@width']) // 2),
          '@y': str(int(target_element['@y']) + int(target_element['@height']))
        })

      BPMNEdge.append(edge)

  data['bpmn:definitions']['bpmndi:BPMNDiagram'] = {
    '@id': collaboration_id + '_di',
    'bpmndi:BPMNPlane': {
      '@id': collaboration_id + '_plane',
      '@bpmnElement': collaboration_id,
      'bpmndi:BPMNShape': BPMNShape,
      'bpmndi:BPMNEdge': BPMNEdge
    }
  }

  return data