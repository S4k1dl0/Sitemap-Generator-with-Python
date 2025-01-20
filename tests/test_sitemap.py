import pytest
from app import create_app
from app.database import init_db
import os

def setup_module(module):
    """Setup the app and database for testing"""
    init_db()
    global app
    app = create_app()
    app.testing = True

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_generate_sitemap(client):
    data = {
        "base_url": "https://example.com",
        "urls": [
            {"path": "/home", "lastmod": "2025-01-20", "changefreq": "daily", "priority": 1.0}
        ]
    }
    response = client.post('/generate_sitemap', json=data, headers={"Authorization": "Bearer TEST_API_KEY"})
    assert response.status_code == 201
    json_data = response.get_json()
    assert 'file' in json_data

    # Cleanup the generated file
    sitemap_file = json_data['file']
    if os.path.exists(sitemap_file):
        os.remove(sitemap_file)

def test_download_sitemap(client):
    sitemap_path = "sitemaps/test_sitemap.xml"
    os.makedirs(os.path.dirname(sitemap_path), exist_ok=True)
    with open(sitemap_path, "w") as f:
        f.write("<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"></urlset>")

    response = client.get(f'/download_sitemap?file={sitemap_path}', headers={"Authorization": "Bearer TEST_API_KEY"})
    assert response.status_code == 200

    # Cleanup
    if os.path.exists(sitemap_path):
        os.remove(sitemap_path)