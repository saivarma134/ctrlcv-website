from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv
from extensions import db

load_dotenv()

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ctrlscv.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# Initialize extensions
db.init_app(app)
CORS(app)

# Import models
from models import User, Contact, DemoRequest, Product, Order

# Create tables
with app.app_context():
    db.create_all()

# Import routes
from routes import auth_bp, contact_bp, demo_bp, product_bp, order_bp, user_bp, project_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(demo_bp)
app.register_blueprint(product_bp)
app.register_blueprint(order_bp)
app.register_blueprint(user_bp)
app.register_blueprint(project_bp)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
