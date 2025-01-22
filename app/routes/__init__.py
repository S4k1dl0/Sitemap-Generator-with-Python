from flask import Blueprint
from .api_keys import bp as api_keys_bp
from .sitemap import bp as sitemap_bp
from .logs import bp as logs_bp  # เพิ่มการนำเข้า logs

# Initialize the Blueprint for the routes
bp = Blueprint('api', __name__)

# Register the Blueprints
bp.register_blueprint(api_keys_bp)
bp.register_blueprint(sitemap_bp)
bp.register_blueprint(logs_bp)  # ลงทะเบียน Blueprint ของ logs
