from flask import Blueprint, jsonify
from app.database import get_db_connection

bp = Blueprint('logs', __name__, url_prefix='/logs')

@bp.route('/', methods=['GET'])
def list_logs():
    """Retrieve and return all logs."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT action, details, created_at FROM logs ORDER BY created_at DESC')
    logs = cursor.fetchall()
    conn.close()
    return jsonify({'logs': [{'action': action, 'details': details, 'created_at': created_at} for action, details, created_at in logs]}), 200