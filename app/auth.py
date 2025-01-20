from app.database import get_db_connection

def verify_token(token):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT key FROM api_keys WHERE key = ?', (token,))
    result = cursor.fetchone()
    conn.close()
    return result is not None
