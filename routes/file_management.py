from quart import Blueprint, jsonify, request
import os

file_management = Blueprint('file_management', __name__)

@file_management.route('/open')
async def open():
    file_path = request.args.get('file_path', default=None, type=str)
    
    if not file_path:
        return jsonify({"status": "error", "message": "No file path provided"}), 400
    
    if not os.path.exists(file_path):
        return jsonify({"status": "error", "message": "File not found"}), 404
    
    with open(file_path, 'r') as f:
        file_contents = f.read()
        
    return jsonify({"status": "success", "content": file_contents})
