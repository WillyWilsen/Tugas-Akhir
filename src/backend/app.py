import xmltodict
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from services.summarization import summarize_document
from services.bpmn_js import generate_bpmn_js
from services.layout import generate_layout
from services.bpmn_sketch_miner import generate_bpmn_sketch_miner

app = Flask(__name__)
CORS(app)

@app.route('/api/bpmn-js', methods=['POST'])
def handle_bpmn_js():
  current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
  file = request.files['file']
  parameter = request.form['parameter']
  file_name = f'output/{current_time}_{file.filename}'
  file_summarizations = summarize_document(file)
  with open(f'{file_name}_summary.txt', 'w') as file:
    file.write(''.join(file_summarizations))
  bpmn = generate_bpmn_js(file_summarizations, parameter)
  with open(f'{file_name}.json', 'w') as file:
    file.write(bpmn)
  bpmn_with_layout = generate_layout(bpmn)
  bpmn_xml = xmltodict.unparse(bpmn_with_layout, pretty=True)
  with open(f'{file_name}.bpmn', 'w') as file:
    file.write(bpmn_xml)
  return jsonify(f'{file_name}.bpmn')

@app.route('/api/bpmn-sketch-miner', methods=['POST'])
def handle_bpmn_sketch_miner():
  file = request.files['file']
  parameter = request.form['parameter']
  file_summarizations = summarize_document(file)
  bpmn_string = generate_bpmn_sketch_miner(file_summarizations, parameter)
  return jsonify(bpmn_string)
  
@app.route('/api/output/<path:filename>', methods=['GET'])
def download_file(filename):
  return send_from_directory('output', filename, as_attachment=True)

if __name__ == '__main__':
  app.run()