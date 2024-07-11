import xmltodict
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from services.bpmn_js import generate_bpmn_js
from services.bpmn_sketch_miner import generate_bpmn_sketch_miner
from services.layout import generate_layout
from services.llm_summarization import summarize_document_llm
from services.rag_llm_summarization import summarize_document_rag_llm

app = Flask(__name__)
CORS(app)

@app.route('/api/bpmn-js', methods=['POST'])
def handle_bpmn_js():
  current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
  file = request.files['file']
  summarizationType = request.form['summarizationType']
  query = request.form['query']
  file_name = f'output/{current_time}_{file.filename}'

  if summarizationType == 'RAG-LLM':
    summary = summarize_document_rag_llm(file, query)
  else:
    summary = summarize_document_llm(file, query)
  with open(f'{file_name}_summary.txt', 'w') as file:
    file.write(summary)

  bpmn = generate_bpmn_js(summary)
  with open(f'{file_name}.json', 'w') as file:
    file.write(bpmn)
  bpmn_with_layout = generate_layout(bpmn)
  bpmn_xml = xmltodict.unparse(bpmn_with_layout, pretty=True)
  with open(f'{file_name}.bpmn', 'w') as file:
    file.write(bpmn_xml)
  return jsonify(f'{file_name}.bpmn')

@app.route('/api/bpmn-sketch-miner', methods=['POST'])
def handle_bpmn_sketch_miner():
  current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
  file = request.files['file']
  summarizationType = request.form['summarizationType']
  query = request.form['query']
  file_name = f'output/{current_time}_{file.filename}'

  if summarizationType == 'RAG-LLM':
    summary = summarize_document_rag_llm(file, query)
  else:
    summary = summarize_document_llm(file, query)
  with open(f'{file_name}_summary.txt', 'w') as file:
    file.write(summary)

  bpmn_string = generate_bpmn_sketch_miner(summary)
  return jsonify(bpmn_string)
  
@app.route('/api/output/<path:filename>', methods=['GET'])
def download_file(filename):
  return send_from_directory('output', filename, as_attachment=True)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)