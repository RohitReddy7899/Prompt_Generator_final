from flask import Blueprint, request, jsonify
from services.prompt_service import compose_prompt, calculate_score, simulate_preview
import json, os, datetime

composer_bp = Blueprint('composer', __name__)
DATA_FILE = 'data/prompts.json'

if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f: json.dump([], f)

def read_data():
    with open(DATA_FILE) as f: return json.load(f)
def write_data(d):
    with open(DATA_FILE, 'w') as f: json.dump(d, f, indent=2)

@composer_bp.route('/compose', methods=['POST'])
def compose():
    data = request.get_json()
    prompt = compose_prompt(data)
    score = calculate_score(prompt)
    return jsonify({'prompt': prompt, 'score': score})

@composer_bp.route('/preview', methods=['POST'])
def preview():
    data = request.get_json()
    return jsonify(simulate_preview(data['prompt'], data['tone']))

@composer_bp.route('/save', methods=['POST'])
def save_prompt():
    data = request.get_json()
    all_data = read_data()
    new_entry = {
        'id': datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f'),
        **data,
        'score': data.get('score', {}),
        'timestamp': datetime.datetime.utcnow().isoformat()
    }
    all_data.append(new_entry)
    write_data(all_data)
    return jsonify({'status': 'saved', 'id': new_entry['id']})

@composer_bp.route('/recalculate_score', methods=['POST'])
def recalc_score():
    data = request.get_json()
    prompt = data.get('prompt', '')
    score = calculate_score(prompt)
    return jsonify(score)
