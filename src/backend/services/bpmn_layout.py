def generate_layout(bpmn, data):
  bpmn['bpmn:definitions']['bpmndi:BPMNDiagram'] = {
    '@id': 'Collaboration_1_di',
    'bpmndi:BPMNPlane': {
      '@id': 'Collaboration_1_plane',
      '@bpmnElement': 'Collaboration_1',
      'bpmndi:BPMNShape': [],
      'bpmndi:BPMNEdge': []
    }
  }

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

  # Participants
  x = distance_each_element
  y = 0
  participants = {}
  for node in data['nodes']:
    # Calculate x
    if node['node_type'] == 'startEvent':
      x += start_event_layout['width'] + distance_each_element
    elif node['node_type'] == 'task':
      x += task_layout['width'] + distance_each_element
    elif node['node_type'] == 'intermediateThrowEvent':
      x += intermediate_throw_event_layout['width'] + distance_each_element
    elif node['node_type'] == 'exclusiveGateway':
      x += exclusive_gateway_layout['width'] + distance_each_element
    elif node['node_type'] == 'endEvent':
      x += end_event_layout['width'] + distance_each_element

    # Calculate y
    if node['node_participant'] not in participants:
      participants[node['node_participant']] = y
      y += participant_layout['height']
    
  for participant in participants:
    bpmn['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']['bpmndi:BPMNShape'].append({
      '@id': f'Participant_{participant}_di',
      '@bpmnElement': f'Participant_{participant}',
      '@isHorizontal': 'true',
      'dc:Bounds': {
        '@x': 0,
        '@y': str(participants[participant]),
        '@width': str(x),
        '@height': str(participant_layout['height'])
      },
      'bpmndi:BPMNLabel': None
    })

  # Process & Sequence Flow
  x = distance_each_element
  processed_nodes = []
  node_queue = [node for node in data['nodes'] if 0 in node['node_parent_id']]
  while len(node_queue) > 0:
    node = node_queue.pop(0)
    if node['node_id'] in processed_nodes:
      break
    processed_nodes.append(node['node_id'])
    node_queue = [child for child in data['nodes'] if node['node_id'] in child['node_parent_id']] + node_queue

    # Node Layout
    if node['node_type'] == 'startEvent':
      bpmn['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']['bpmndi:BPMNShape'].append({
        '@id': f'{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}_di',
        '@bpmnElement': f'{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}',
        'dc:Bounds': {
          '@x': str(x),
          '@y': str(participants[node['node_participant']] + (participant_layout['height'] - start_event_layout['height']) // 2),
          '@width': str(start_event_layout['width']),
          '@height': str(start_event_layout['height'])
        },
        'bpmndi:BPMNLabel': {
          'dc:Bounds': {
            '@x': str(x),
            '@y': str(participants[node['node_participant']] + (participant_layout['height'] - start_event_layout['height']) // 2 + start_event_layout['height'] + distance_event_label_to_layout),
            '@width': str(event_label_layout['width']),
            '@height': str(event_label_layout['height'])
          }
        }
      })
      x += start_event_layout['width'] + distance_each_element
    elif node['node_type'] == 'task':
      bpmn['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']['bpmndi:BPMNShape'].append({
        '@id': f'{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}_di',
        '@bpmnElement': f'{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}',
        'dc:Bounds': {
          '@x': str(x),
          '@y': str(participants[node['node_participant']] + (participant_layout['height'] - task_layout['height']) // 2),
          '@width': str(task_layout['width']),
          '@height': str(task_layout['height'])
        },
        'bpmndi:BPMNLabel': None
      })
      x += task_layout['width'] + distance_each_element
    elif node['node_type'] == 'intermediateThrowEvent':
      bpmn['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']['bpmndi:BPMNShape'].append({
        '@id': f'{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}_di',
        '@bpmnElement': f'{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}',
        'dc:Bounds': {
          '@x': str(x),
          '@y': str(participants[node['node_participant']] + (participant_layout['height'] - intermediate_throw_event_layout['height']) // 2),
          '@width': str(intermediate_throw_event_layout['width']),
          '@height': str(intermediate_throw_event_layout['height'])
        },
        'bpmndi:BPMNLabel': {
          'dc:Bounds': {
            '@x': str(x),
            '@y': str(participants[node['node_participant']] + (participant_layout['height'] - intermediate_throw_event_layout['height']) // 2 + intermediate_throw_event_layout['height'] + distance_event_label_to_layout),
            '@width': str(event_label_layout['width']),
            '@height': str(event_label_layout['height'])
          }
        }
      })
      x += intermediate_throw_event_layout['width'] + distance_each_element
    elif node['node_type'] == 'exclusiveGateway':
      bpmn['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']['bpmndi:BPMNShape'].append({
        '@id': f'{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}_di',
        '@bpmnElement': f'{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}',
        '@isMarkerVisible': 'true',
        'dc:Bounds': {
          '@x': str(x),
          '@y': str(participants[node['node_participant']] + (participant_layout['height'] - exclusive_gateway_layout['height']) // 2),
          '@width': str(exclusive_gateway_layout['width']),
          '@height': str(exclusive_gateway_layout['height'])
        }
      })
      x += exclusive_gateway_layout['width'] + distance_each_element
    elif node['node_type'] == 'endEvent':
      bpmn['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']['bpmndi:BPMNShape'].append({
        '@id': f'{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}_di',
        '@bpmnElement': f'{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}',
        'dc:Bounds': {
          '@x': str(x),
          '@y': str(participants[node['node_participant']] + (participant_layout['height'] - end_event_layout['height']) // 2),
          '@width': str(end_event_layout['width']),
          '@height': str(end_event_layout['height'])
        },
        'bpmndi:BPMNLabel': {
          'dc:Bounds': {
            '@x': str(x),
            '@y': str(participants[node['node_participant']] + (participant_layout['height'] - end_event_layout['height']) // 2 + end_event_layout['height'] + distance_event_label_to_layout),
            '@width': str(event_label_layout['width']),
            '@height': str(event_label_layout['height'])
          }
        }
      })
      x += end_event_layout['width'] + distance_each_element

    # Edge Layout
    if node['node_parent_id'] != [0]:
      node_parents = [node_parent for node_parent in data['nodes'] if node_parent['node_id'] in node['node_parent_id']]
      for node_parent in node_parents:
        edge = {
          '@id': f'Flow_{node_parent["node_type"]}_{node_parent["node_participant"]}_{node_parent["node_id"]}_{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}_di',
          '@bpmnElement': f'Flow_{node_parent["node_type"]}_{node_parent["node_participant"]}_{node_parent["node_id"]}_{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}',
          'di:waypoint': []
        }
        source_shape = [shape for shape in bpmn['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']['bpmndi:BPMNShape'] if shape['@bpmnElement'] == f'{node_parent["node_type"]}_{node_parent["node_participant"]}_{node_parent["node_id"]}'][0]
        target_shape = [shape for shape in bpmn['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']['bpmndi:BPMNShape'] if shape['@bpmnElement'] == f'{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}'][0]
        if node_parent['node_participant'] == node['node_participant']:
          if int(source_shape['dc:Bounds']['@x']) < int(target_shape['dc:Bounds']['@x']):
            edge['di:waypoint'].append({
              '@x': str(int(source_shape['dc:Bounds']['@x']) + int(source_shape['dc:Bounds']['@width'])),
              '@y': str(int(source_shape['dc:Bounds']['@y']) + int(source_shape['dc:Bounds']['@height']) // 2)
            })
            edge['di:waypoint'].append({
              '@x': str(int(target_shape['dc:Bounds']['@x'])),
              '@y': str(int(target_shape['dc:Bounds']['@y']) + int(target_shape['dc:Bounds']['@height']) // 2)
            })
          else:
            edge['di:waypoint'].append({
              '@x': str(int(source_shape['dc:Bounds']['@x'])),
              '@y': str(int(source_shape['dc:Bounds']['@y']) + int(source_shape['dc:Bounds']['@height']) // 2)
            })
            edge['di:waypoint'].append({
              '@x': str(int(target_shape['dc:Bounds']['@x']) + int(target_shape['dc:Bounds']['@width'])),
              '@y': str(int(target_shape['dc:Bounds']['@y']) + int(target_shape['dc:Bounds']['@height']) // 2)
            })
        else:
          if int(source_shape['dc:Bounds']['@y']) < int(target_shape['dc:Bounds']['@y']):
            edge['di:waypoint'].append({
              '@x': str(int(source_shape['dc:Bounds']['@x']) + int(source_shape['dc:Bounds']['@width']) // 2),
              '@y': str(int(source_shape['dc:Bounds']['@y']) + int(source_shape['dc:Bounds']['@height']))
            })
            edge['di:waypoint'].append({
              '@x': str(int(target_shape['dc:Bounds']['@x']) + int(target_shape['dc:Bounds']['@width']) // 2),
              '@y': str(int(target_shape['dc:Bounds']['@y']))
            })
          else:
            edge['di:waypoint'].append({
              '@x': str(int(source_shape['dc:Bounds']['@x']) + int(source_shape['dc:Bounds']['@width']) // 2),
              '@y': str(int(source_shape['dc:Bounds']['@y']))
            })
            edge['di:waypoint'].append({
              '@x': str(int(target_shape['dc:Bounds']['@x']) + int(target_shape['dc:Bounds']['@width']) // 2),
              '@y': str(int(target_shape['dc:Bounds']['@y']) + int(target_shape['dc:Bounds']['@height']))
            })
        bpmn['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']['bpmndi:BPMNEdge'].append(edge)

  return bpmn