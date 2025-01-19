import os
import json
import sqlite3
from flask import Flask, request, jsonify, send_file
from flask_httpauth import HTTPTokenAuth
import xml.etree.ElementTree as ET
from datetime import datetime
import secrets

# Initialize Flask app and auth
app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

# Database setup
db_file = 'sitemap_api.db'
def init_db():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS api_keys (
                        id INTEGER PRIMARY KEY,
                        key TEXT UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY,
                        action TEXT NOT NULL,
                        details TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                      )''')
    conn.commit()
    conn.close()

init_db()

# API Key management
@app.route('/generate_api_key', methods=['POST'])
def generate_api_key():
    key = secrets.token_hex(16)
    conn = sqlite3.connect(db_file)
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

@auth.verify_token
def verify_token(token):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT key FROM api_keys WHERE key = ?', (token,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def log_action(action, details):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO logs (action, details) VALUES (?, ?)', (action, details))
    conn.commit()
    conn.close()

# Generate Sitemap
@app.route('/generate_sitemap', methods=['POST'])
@auth.login_required

def generate_sitemap():
    try:
        data = request.json
        urls = data.get('urls', [])
        base_url = data.get('base_url', '')
        sitemap_file = f'sitemaps/sitemap_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xml'

        if not os.path.exists('sitemaps'):
            os.makedirs('sitemaps')

        urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')

        for url in urls:
            url_element = ET.SubElement(urlset, 'url')
            ET.SubElement(url_element, 'loc').text = f"{base_url}{url['path']}"
            if 'lastmod' in url:
                ET.SubElement(url_element, 'lastmod').text = url['lastmod']
            if 'changefreq' in url:
                ET.SubElement(url_element, 'changefreq').text = url['changefreq']
            if 'priority' in url:
                ET.SubElement(url_element, 'priority').text = str(url['priority'])

        tree = ET.ElementTree(urlset)
        tree.write(sitemap_file, encoding='utf-8', xml_declaration=True)
        log_action('Generate Sitemap', f'Sitemap generated and saved to {sitemap_file}')

        return jsonify({'message': 'Sitemap generated successfully', 'file': sitemap_file}), 201

    except Exception as e:
        log_action('Error', str(e))
        return jsonify({'error': 'An error occurred while generating the sitemap', 'details': str(e)}), 500

# Download Sitemap
@app.route('/download_sitemap', methods=['GET'])
@auth.login_required
def download_sitemap():
    file_path = request.args.get('file')
    if file_path and os.path.exists(file_path):
        log_action('Download Sitemap', f'Sitemap downloaded: {file_path}')
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

# API Key listing for admin (Optional)
@app.route('/list_api_keys', methods=['GET'])
@auth.login_required
def list_api_keys():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT key, created_at FROM api_keys')
    keys = cursor.fetchall()
    conn.close()
    return jsonify({'api_keys': [{'key': key, 'created_at': created_at} for key, created_at in keys]}), 200

if __name__ == '__main__':
    app.run(debug=True)
