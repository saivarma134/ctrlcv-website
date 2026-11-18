from flask import Blueprint, request, jsonify
from extensions import db
from models import User, Contact, DemoRequest, Product, Order
from datetime import datetime
import re
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Create blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
contact_bp = Blueprint('contact', __name__, url_prefix='/api/contact')
demo_bp = Blueprint('demo', __name__, url_prefix='/api/demo')
product_bp = Blueprint('product', __name__, url_prefix='/api/products')
order_bp = Blueprint('order', __name__, url_prefix='/api/orders')
user_bp = Blueprint('user', __name__, url_prefix='/api/users')
project_bp = Blueprint('project', __name__, url_prefix='/api/projects')

PROJECTS = {
    'e-commerce-demo': {
        'slug': 'e-commerce-demo',
        'name': 'E-commerce Demo',
        'service_type': 'website',
        'description': 'Online store with product pages, cart and checkout.'
    },
    'admin-dashboard': {
        'slug': 'admin-dashboard',
        'name': 'Admin Dashboard',
        'service_type': 'dashboard',
        'description': 'Firebase based product and order management.'
    },
    'shopos-system': {
        'slug': 'shopos-system',
        'name': 'ShopOS System',
        'service_type': 'shopos',
        'description': 'Billing, stock tracking and sales report system.'
    }
}

# Helper function for email validation
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@project_bp.route('/<string:slug>', methods=['GET'])
def get_project(slug):
    """Return the project selected by a visitor."""
    project = PROJECTS.get(slug)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    return jsonify(project), 200

# Helper function to send email (configure with your SMTP settings)
def send_email(to_email, subject, body):
    """Send email notification"""
    try:
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('SENDER_PASSWORD')

        if not all([smtp_server, sender_email, sender_password]):
            print('Email skipped: SMTP settings are not configured')
            return False
        
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'html'))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        return True
    except Exception as e:
        print(f"Email sending failed: {str(e)}")
        return False


# ==================== AUTHENTICATION ROUTES ====================
@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password') or not data.get('username'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not is_valid_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 409
    
    user = User(
        email=data['email'],
        username=data['username'],
        full_name=data.get('full_name', '')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'user': user.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is inactive'}), 403
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict()
    }), 200


# ==================== CONTACT FORM ROUTES ====================
@contact_bp.route('/submit', methods=['POST'])
def submit_contact():
    """Submit a contact form"""
    data = request.get_json()
    
    required_fields = ['name', 'email', 'subject', 'message']
    if not all(data.get(field) for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not is_valid_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    
    contact = Contact(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone', ''),
        subject=data['subject'],
        message=data['message']
    )
    
    db.session.add(contact)
    db.session.commit()
    
    # Send confirmation email
    email_body = f"""
    <h2>Thank you for contacting CtrlSCV!</h2>
    <p>We received your message and will get back to you soon.</p>
    <hr>
    <p><strong>Your Message:</strong></p>
    <p>{data['message']}</p>
    """
    confirmation_sent = send_email(data['email'], 'CtrlSCV - Message Received', email_body)
    owner_email = os.getenv('CONTACT_EMAIL')
    owner_notification_sent = send_email(owner_email, f"New contact: {data['subject']}", email_body) if owner_email else False
    
    return jsonify({
        'message': 'Contact form submitted successfully',
        'contact_id': contact.id,
        'email_sent': confirmation_sent,
        'owner_notification_sent': owner_notification_sent
    }), 201


@contact_bp.route('/list', methods=['GET'])
def list_contacts():
    """List all contacts (admin only)"""
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return jsonify([contact.to_dict() for contact in contacts]), 200


@contact_bp.route('/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    """Get specific contact"""
    contact = Contact.query.get(contact_id)
    
    if not contact:
        return jsonify({'error': 'Contact not found'}), 404
    
    return jsonify(contact.to_dict()), 200


@contact_bp.route('/<int:contact_id>/status', methods=['PATCH'])
def update_contact_status(contact_id):
    """Update contact status"""
    contact = Contact.query.get(contact_id)
    
    if not contact:
        return jsonify({'error': 'Contact not found'}), 404
    
    data = request.get_json()
    if 'status' in data:
        contact.status = data['status']
    
    db.session.commit()
    return jsonify(contact.to_dict()), 200


# ==================== DEMO REQUEST ROUTES ====================
@demo_bp.route('/request', methods=['POST'])
def request_demo():
    """Submit a demo/quote request"""
    data = request.get_json()
    
    required_fields = ['name', 'email', 'service_type']
    if not all(data.get(field) for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not is_valid_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    
    demo = DemoRequest(
        name=data['name'],
        email=data['email'],
        company=data.get('company', ''),
        service_type=data['service_type'],
        budget=data.get('budget', ''),
        timeline=data.get('timeline', ''),
        description=data.get('description', '')
    )
    
    db.session.add(demo)
    db.session.commit()
    
    # Send confirmation email
    email_body = f"""
    <h2>Demo Request Received!</h2>
    <p>Thank you for your interest in our {data['service_type']} service.</p>
    <p>We'll contact you within 24 hours to schedule your demo.</p>
    <hr>
    <p><strong>Request Details:</strong></p>
    <p>Service: {data['service_type']}</p>
    <p>Company: {data.get('company', 'N/A')}</p>
    <p>Budget: {data.get('budget', 'Not specified')}</p>
    """
    send_email(data['email'], 'CtrlSCV - Demo Request Confirmed', email_body)
    
    return jsonify({
        'message': 'Demo request submitted successfully',
        'demo_id': demo.id
    }), 201


@demo_bp.route('/list', methods=['GET'])
def list_demos():
    """List all demo requests"""
    demos = DemoRequest.query.order_by(DemoRequest.created_at.desc()).all()
    return jsonify([demo.to_dict() for demo in demos]), 200


@demo_bp.route('/<int:demo_id>', methods=['GET'])
def get_demo(demo_id):
    """Get specific demo request"""
    demo = DemoRequest.query.get(demo_id)
    
    if not demo:
        return jsonify({'error': 'Demo request not found'}), 404
    
    return jsonify(demo.to_dict()), 200


@demo_bp.route('/<int:demo_id>/status', methods=['PATCH'])
def update_demo_status(demo_id):
    """Update demo request status"""
    demo = DemoRequest.query.get(demo_id)
    
    if not demo:
        return jsonify({'error': 'Demo request not found'}), 404
    
    data = request.get_json()
    if 'status' in data:
        demo.status = data['status']
    if 'scheduled_date' in data:
        demo.scheduled_date = datetime.fromisoformat(data['scheduled_date'])
    
    db.session.commit()
    return jsonify(demo.to_dict()), 200


# ==================== PRODUCT ROUTES ====================
@product_bp.route('', methods=['GET'])
def list_products():
    """List all products"""
    category = request.args.get('category')
    query = Product.query.filter_by(is_active=True)
    
    if category:
        query = query.filter_by(category=category)
    
    products = query.all()
    return jsonify([product.to_dict() for product in products]), 200


@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get specific product"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify(product.to_dict()), 200


@product_bp.route('', methods=['POST'])
def create_product():
    """Create new product (admin only)"""
    data = request.get_json()
    
    required_fields = ['name', 'slug', 'category']
    if not all(data.get(field) for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if Product.query.filter_by(slug=data['slug']).first():
        return jsonify({'error': 'Product slug already exists'}), 409
    
    product = Product(
        name=data['name'],
        slug=data['slug'],
        description=data.get('description', ''),
        category=data['category'],
        price=data.get('price'),
        features=data.get('features', [])
    )
    
    db.session.add(product)
    db.session.commit()
    
    return jsonify({
        'message': 'Product created successfully',
        'product': product.to_dict()
    }), 201


@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update product (admin only)"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        product.price = data['price']
    if 'features' in data:
        product.features = data['features']
    if 'is_active' in data:
        product.is_active = data['is_active']
    
    db.session.commit()
    return jsonify(product.to_dict()), 200


# ==================== ORDER ROUTES ====================
@order_bp.route('', methods=['POST'])
def create_order():
    """Create new order"""
    data = request.get_json()
    
    required_fields = ['customer_name', 'customer_email', 'product_id']
    if not all(data.get(field) for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not is_valid_email(data['customer_email']):
        return jsonify({'error': 'Invalid email format'}), 400
    
    product = Product.query.get(data['product_id'])
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    order = Order(
        product_id=data['product_id'],
        customer_name=data['customer_name'],
        customer_email=data['customer_email'],
        customer_phone=data.get('customer_phone', ''),
        description=data.get('description', ''),
        amount=product.price
    )
    
    db.session.add(order)
    db.session.commit()
    
    # Send confirmation email
    email_body = f"""
    <h2>Order Confirmation</h2>
    <p>Thank you for your order!</p>
    <hr>
    <p><strong>Order Details:</strong></p>
    <p>Product: {product.name}</p>
    <p>Amount: ${product.price}</p>
    <p>Order ID: {order.id}</p>
    <p>Status: {order.status}</p>
    """
    send_email(data['customer_email'], 'CtrlSCV - Order Confirmation', email_body)
    
    return jsonify({
        'message': 'Order created successfully',
        'order': order.to_dict()
    }), 201


@order_bp.route('', methods=['GET'])
def list_orders():
    """List all orders"""
    user_id = request.args.get('user_id')
    query = Order.query
    
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    orders = query.order_by(Order.created_at.desc()).all()
    return jsonify([order.to_dict() for order in orders]), 200


@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get specific order"""
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    return jsonify(order.to_dict()), 200


@order_bp.route('/<int:order_id>/status', methods=['PATCH'])
def update_order_status(order_id):
    """Update order status"""
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    data = request.get_json()
    if 'status' in data:
        order.status = data['status']
    
    db.session.commit()
    return jsonify(order.to_dict()), 200


# ==================== USER ROUTES ====================
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user profile"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user profile"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if 'full_name' in data:
        user.full_name = data['full_name']
    if 'email' in data and data['email'] != user.email:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already in use'}), 409
        user.email = data['email']
    
    db.session.commit()
    return jsonify(user.to_dict()), 200
