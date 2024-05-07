import json
import xmltodict

# Path to your JSON file
json_file_path = 'jsontoxml2.json'

# Read the JSON file
with open(json_file_path, 'r') as file:
    json_data = file.read()

# Convert JSON to Python dictionary
data_dict = json.loads(json_data)

# Convert dictionary to XML
xml_data = xmltodict.unparse(data_dict, pretty=True)

with open("data.bpmn", "w") as xml_file:
	xml_file.write(xml_data)