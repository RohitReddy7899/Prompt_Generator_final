from flask import Blueprint, jsonify, request, send_file
from services.search_service import search_prompts
import json, os

library_bp = Blueprint('library', __name__)
DATA_FILE = 'data/prompts.json'

def read_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f: return json.load(f)

@library_bp.route('/library', methods=['GET'])
def library():
    return jsonify(read_data())

@library_bp.route('/library/search', methods=['POST'])
def library_search():
    data = request.get_json()
    keyword = data.get('keyword', '')
    results = search_prompts(read_data(), keyword)
    return jsonify(results)

@library_bp.route('/library/export')
def export():
    return send_file(DATA_FILE, as_attachment=True)
