# Merge BPMN JS
def merge_bpmn_json(data):
  bpmn = {
    "bpmn:definitions": {
      "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
      "@xmlns:bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
      "@xmlns:bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
      "@xmlns:dc": "http://www.omg.org/spec/DD/20100524/DC",
      "@xmlns:di": "http://www.omg.org/spec/DD/20100524/DI",
      "@id": "Definitions_1xh4b31",
      "@targetNamespace": "http://bpmn.io/schema/bpmn",
      "@exporter": "bpmn-js (https://demo.bpmn.io)",
      "@exporterVersion": "16.4.0",
      "bpmn:collaboration": {
        "@id": "Collaboration_1",
        "bpmn:participant": [],
        "bpmn:messageFlow": [],
      },
      "bpmn:process": []
    }
  }

  processed_nodes = []
  node_queue = [node for node in data['nodes'] if 0 in node['node_parent_id']]
  while len(node_queue) > 0:
    node = node_queue.pop(0)
    if node['node_id'] in processed_nodes:
      break
    processed_nodes.append(node['node_id'])
    node_queue = [child for child in data['nodes'] if node['node_id'] in child['node_parent_id']] + node_queue

    participant_id = [participant["@id"] for participant in bpmn["bpmn:definitions"]["bpmn:collaboration"]["bpmn:participant"]]
    if f"Participant_{node['node_participant']}" not in participant_id:
      bpmn["bpmn:definitions"]["bpmn:collaboration"]["bpmn:participant"].append({
        "@id": f"Participant_{node['node_participant']}",
        "@name": node['node_participant'],
        "@processRef": f"Process_{node['node_participant']}"
      })

      bpmn["bpmn:definitions"]["bpmn:process"].append({
        "@id": f"Process_{node['node_participant']}",
        "bpmn:laneSet": { "@id": f"LaneSet_{node['node_participant']}" },
        "bpmn:startEvent": [],
        "bpmn:task": [],
        "bpmn:intermediateThrowEvent": [],
        "bpmn:exclusiveGateway": [],
        "bpmn:endEvent": [],
        "bpmn:sequenceFlow": []
      })

    idx_process = [idx for idx, process in enumerate(bpmn["bpmn:definitions"]["bpmn:process"]) if process["@id"] == f"Process_{node['node_participant']}"][0]
    bpmn["bpmn:definitions"]["bpmn:process"][idx_process][f"bpmn:{node['node_type']}"].append({
      "@id": f"{node['node_type']}_{node['node_participant']}_{node['node_id']}",
      "@name": node['node_name']
    })
    for node_child in node_queue:
      if node['node_id'] in node_child['node_parent_id']:
        if node_child['node_participant'] == node['node_participant']:
          bpmn["bpmn:definitions"]["bpmn:process"][idx_process]["bpmn:sequenceFlow"].append({
            "@id": f"Flow_{node['node_type']}_{node['node_participant']}_{node['node_id']}_{node_child['node_type']}_{node_child['node_participant']}_{node_child['node_id']}",
            "@sourceRef": f"{node['node_type']}_{node['node_participant']}_{node['node_id']}",
            "@targetRef": f"{node_child['node_type']}_{node_child['node_participant']}_{node_child['node_id']}"
          })
        else:
          bpmn["bpmn:definitions"]["bpmn:collaboration"]["bpmn:messageFlow"].append({
            "@id": f"Flow_{node['node_type']}_{node['node_participant']}_{node['node_id']}_{node_child['node_type']}_{node_child['node_participant']}_{node_child['node_id']}",
            "@sourceRef": f"{node['node_type']}_{node['node_participant']}_{node['node_id']}",
            "@targetRef": f"{node_child['node_type']}_{node_child['node_participant']}_{node_child['node_id']}"
          })

  return bpmn