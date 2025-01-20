from flask import Blueprint, request, jsonify
from app.database import get_db_connection
from app.utils import log_action
import secrets

bp = Blueprint('api_keys', __name__)

@bp.route('/generate_api_key', methods=['POST'])
def generate_api_key():
    key = secrets.token_hex(16)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO api_keys (key) VALUES (?)', (key,))
        conn.commit()
        log_action('Generate API Key', f'API Key {key} created')
        return jsonify({'message': 'API Key generated successfully', 'key': key}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'API Key already exists'}), 400
    finally:
        conn.close()
