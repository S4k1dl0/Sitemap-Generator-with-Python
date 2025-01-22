# Sitemap API

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Build Status](https://img.shields.io/badge/build-passing-brightgreen)

A simple Flask application for generating and managing sitemaps with API key authentication.

## Features
- Generate API keys for authentication
- Create sitemaps dynamically
- Download generated sitemaps
- Log all actions (e.g., key generation, sitemap creation)

## Setup

1. Clone the repository: 
   ```bash
   git clone <repository_url>
   cd project

2. Create a virtual environment and install dependencies:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

3. Run the application:
    ```bash
    python run.py

4. Test the APIs using tools like Postman or curl.


## API Endpoints

1. Generate API Key
    ```bash
    POST /generate_api_key

2. Generate Sitemap
    ```bash
    POST /generate_sitemap

3. Download Sitemap
    ```bash
    GET /download_sitemap?file=<file_path>