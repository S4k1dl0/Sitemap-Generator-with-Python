from flask import Blueprint, request, jsonify, send_file
from datetime import datetime
import os
import xml.etree.ElementTree as ET
from app.utils import log_action

bp = Blueprint('sitemap', __name__)

@bp.route('/generate_sitemap', methods=['POST'])
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

@bp.route('/download_sitemap', methods=['GET'])
def download_sitemap():
    file_path = request.args.get('file')
    if file_path and os.path.exists(file_path):
        log_action('Download Sitemap', f'Sitemap downloaded: {file_path}')
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404
