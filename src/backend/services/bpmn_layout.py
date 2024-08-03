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
  distance_each_element = {
    'x': 50,
    'y': 10
  }
  start_event_layout = {
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

  # Calculate width
  x = distance_each_element['x']
  for node in data['nodes']:
    if node['node_type'] == 'startEvent':
      x += start_event_layout['width'] + distance_each_element['x']
    elif node['node_type'] == 'task':
      x += task_layout['width'] + distance_each_element['x']
    elif node['node_type'] == 'intermediateThrowEvent':
      x += intermediate_throw_event_layout['width'] + distance_each_element['x']
    elif node['node_type'] == 'exclusiveGateway':
      x += exclusive_gateway_layout['width'] + distance_each_element['x']
    elif node['node_type'] == 'endEvent':
      x += end_event_layout['width'] + distance_each_element['x']

  # Calculate height
  participants = {}
  for node in data['nodes']:
    if node['node_participant'] not in participants:
      participants[node['node_participant']] = {
        'height': distance_each_element['y']
      }

    if node['node_type'] == 'startEvent':
      participants[node['node_participant']]['height'] += start_event_layout['height'] + distance_each_element['y']
    elif node['node_type'] == 'task':
      participants[node['node_participant']]['height'] += task_layout['height'] + distance_each_element['y']
    elif node['node_type'] == 'intermediateThrowEvent':
      participants[node['node_participant']]['height'] += intermediate_throw_event_layout['height'] + distance_each_element['y']
    elif node['node_type'] == 'exclusiveGateway':
      participants[node['node_participant']]['height'] += exclusive_gateway_layout['height'] + distance_each_element['y']
    elif node['node_type'] == 'endEvent':
      participants[node['node_participant']]['height'] += end_event_layout['height'] + distance_each_element['y']
    
  # Participants
  y = 0
  for participant in participants:
    bpmn['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']['bpmndi:BPMNShape'].append({
      '@id': f'Participant_{participant}_di',
      '@bpmnElement': f'Participant_{participant}',
      '@isHorizontal': 'true',
      'dc:Bounds': {
        '@x': 0,
        '@y': str(y),
        '@width': str(x),
        '@height': str(participants[participant]['height'])
      },
      'bpmndi:BPMNLabel': None
    })

    participants[participant]['current_y'] = y + distance_each_element['y']
    y += participants[participant]['height']

  # Process & Sequence Flow
  x = distance_each_element['x']
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
          '@y': str(participants[node['node_participant']]['current_y']),
          '@width': str(start_event_layout['width']),
          '@height': str(start_event_layout['height'])
        },
        'bpmndi:BPMNLabel': {
          'dc:Bounds': {
            '@x': str(x),
            '@y': str(participants[node['node_participant']]['current_y'] + start_event_layout['height'] + distance_event_label_to_layout),
            '@width': str(event_label_layout['width']),
            '@height': str(event_label_layout['height'])
          }
        }
      })
      x += start_event_layout['width'] + distance_each_element['x']
      participants[node['node_participant']]['current_y'] += start_event_layout['height'] + distance_each_element['y']
    elif node['node_type'] == 'task':
      bpmn['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']['bpmndi:BPMNShape'].append({
        '@id': f'{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}_di',
        '@bpmnElement': f'{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}',
        'dc:Bounds': {
          '@x': str(x),
          '@y': str(participants[node['node_participant']]['current_y']),
          '@width': str(task_layout['width']),
          '@height': str(task_layout['height'])
        },
        'bpmndi:BPMNLabel': None
      })
      x += task_layout['width'] + distance_each_element['x']
      participants[node['node_participant']]['current_y'] += task_layout['height'] + distance_each_element['y']
    elif node['node_type'] == 'intermediateThrowEvent':
      bpmn['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']['bpmndi:BPMNShape'].append({
        '@id': f'{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}_di',
        '@bpmnElement': f'{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}',
        'dc:Bounds': {
          '@x': str(x),
          '@y': str(participants[node['node_participant']]['current_y']),
          '@width': str(intermediate_throw_event_layout['width']),
          '@height': str(intermediate_throw_event_layout['height'])
        },
        'bpmndi:BPMNLabel': {
          'dc:Bounds': {
            '@x': str(x),
            '@y': str(participants[node['node_participant']]['current_y'] + intermediate_throw_event_layout['height'] + distance_event_label_to_layout),
            '@width': str(event_label_layout['width']),
            '@height': str(event_label_layout['height'])
          }
        }
      })
      x += intermediate_throw_event_layout['width'] + distance_each_element['x']
      participants[node['node_participant']]['current_y'] += intermediate_throw_event_layout['height'] + distance_each_element['y']
    elif node['node_type'] == 'exclusiveGateway':
      bpmn['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']['bpmndi:BPMNShape'].append({
        '@id': f'{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}_di',
        '@bpmnElement': f'{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}',
        '@isMarkerVisible': 'true',
        'dc:Bounds': {
          '@x': str(x),
          '@y': str(participants[node['node_participant']]['current_y']),
          '@width': str(exclusive_gateway_layout['width']),
          '@height': str(exclusive_gateway_layout['height'])
        }
      })
      x += exclusive_gateway_layout['width'] + distance_each_element['x']
      participants[node['node_participant']]['current_y'] += exclusive_gateway_layout['height'] + distance_each_element['y']
    elif node['node_type'] == 'endEvent':
      bpmn['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']['bpmndi:BPMNShape'].append({
        '@id': f'{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}_di',
        '@bpmnElement': f'{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}',
        'dc:Bounds': {
          '@x': str(x),
          '@y': str(participants[node['node_participant']]['current_y']),
          '@width': str(end_event_layout['width']),
          '@height': str(end_event_layout['height'])
        },
        'bpmndi:BPMNLabel': {
          'dc:Bounds': {
            '@x': str(x),
            '@y': str(participants[node['node_participant']]['current_y'] + end_event_layout['height'] + distance_event_label_to_layout),
            '@width': str(event_label_layout['width']),
            '@height': str(event_label_layout['height'])
          }
        }
      })
      x += end_event_layout['width'] + distance_each_element['x']
      participants[node['node_participant']]['current_y'] += end_event_layout['height'] + distance_each_element['y']

    # Edge Layout
    if node['node_parent_id'] != [0]:
      node_parents = [node_parent for node_parent in data['nodes'] if node_parent['node_id'] in node['node_parent_id']]
      for node_parent in node_parents:
        edge = {
          '@id': f'Flow_{node_parent["node_type"]}_{node_parent["node_participant"]}_{node_parent["node_id"]}_{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}_di',
          '@bpmnElement': f'Flow_{node_parent["node_type"]}_{node_parent["node_participant"]}_{node_parent["node_id"]}_{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}',
          'di:waypoint': []
        }
        source_shapes = [shape for shape in bpmn['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']['bpmndi:BPMNShape'] if shape['@bpmnElement'] == f'{node_parent["node_type"]}_{node_parent["node_participant"]}_{node_parent["node_id"]}']
        target_shapes = [shape for shape in bpmn['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']['bpmndi:BPMNShape'] if shape['@bpmnElement'] == f'{node["node_type"]}_{node["node_participant"]}_{node["node_id"]}']
        if len(source_shapes) > 0 and len(target_shapes) > 0:
          source_shape = source_shapes[0]
          target_shape = target_shapes[0]
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