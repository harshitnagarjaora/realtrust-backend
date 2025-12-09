"""
Real Trust - Backend API 
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGTEXT
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# MySQL Configuration for Railway
DATABASE_URL = os.environ.get('DATABASE_URL') or os.environ.get('MYSQL_URL')

if not DATABASE_URL:
    MYSQL_HOST = os.environ.get('MYSQLHOST', os.environ.get('MYSQL_HOST', 'localhost'))
    MYSQL_PORT = os.environ.get('MYSQLPORT', os.environ.get('MYSQL_PORT', '3306'))
    MYSQL_USER = os.environ.get('MYSQLUSER', os.environ.get('MYSQL_USER', 'root'))
    MYSQL_PASSWORD = os.environ.get('MYSQLPASSWORD', os.environ.get('MYSQL_PASSWORD', ''))
    MYSQL_DATABASE = os.environ.get('MYSQLDATABASE', os.environ.get('MYSQL_DATABASE', 'railway'))
    
    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

if DATABASE_URL and DATABASE_URL.startswith('mysql://'):
    DATABASE_URL = DATABASE_URL.replace('mysql://', 'mysql+pymysql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ==================== MODELS ====================

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(LONGTEXT, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    designation = db.Column(db.String(200), nullable=False)
    image = db.Column(LONGTEXT, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'designation': self.designation,
            'image': self.image,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'mobile': self.mobile,
            'city': self.city,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Newsletter(db.Model):
    __tablename__ = 'newsletters'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ==================== PROJECT ROUTES ====================

@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return jsonify([p.to_dict() for p in projects])


@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.json
    
    if not all(k in data for k in ['name', 'description', 'image']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    project = Project(
        name=data['name'],
        description=data['description'],
        image=data['image']
    )
    
    db.session.add(project)
    db.session.commit()
    
    return jsonify(project.to_dict()), 201


@app.route('/api/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted'})


# ==================== CLIENT ROUTES ====================

@app.route('/api/clients', methods=['GET'])
def get_clients():
    clients = Client.query.order_by(Client.created_at.desc()).all()
    return jsonify([c.to_dict() for c in clients])


@app.route('/api/clients', methods=['POST'])
def create_client():
    data = request.json
    
    if not all(k in data for k in ['name', 'description', 'designation', 'image']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    client = Client(
        name=data['name'],
        description=data['description'],
        designation=data['designation'],
        image=data['image']
    )
    
    db.session.add(client)
    db.session.commit()
    
    return jsonify(client.to_dict()), 201


@app.route('/api/clients/<int:id>', methods=['DELETE'])
def delete_client(id):
    client = Client.query.get_or_404(id)
    db.session.delete(client)
    db.session.commit()
    return jsonify({'message': 'Client deleted'})


# ==================== CONTACT ROUTES ====================

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return jsonify([c.to_dict() for c in contacts])


@app.route('/api/contacts', methods=['POST'])
def create_contact():
    data = request.json
    
    if not all(k in data for k in ['full_name', 'email', 'mobile', 'city']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    contact = Contact(
        full_name=data['full_name'],
        email=data['email'],
        mobile=data['mobile'],
        city=data['city']
    )
    
    db.session.add(contact)
    db.session.commit()
    
    return jsonify(contact.to_dict()), 201


# ==================== NEWSLETTER ROUTES ====================

@app.route('/api/newsletter', methods=['GET'])
def get_newsletters():
    newsletters = Newsletter.query.order_by(Newsletter.created_at.desc()).all()
    return jsonify([n.to_dict() for n in newsletters])


@app.route('/api/newsletter', methods=['POST'])
def subscribe_newsletter():
    data = request.json
    
    if 'email' not in data:
        return jsonify({'error': 'Email is required'}), 400
    
    existing = Newsletter.query.filter_by(email=data['email']).first()
    if existing:
        return jsonify({'message': 'Already subscribed'}), 200
    
    newsletter = Newsletter(email=data['email'])
    
    db.session.add(newsletter)
    db.session.commit()
    
    return jsonify(newsletter.to_dict()), 201


# ==================== DATABASE MANAGEMENT ====================

@app.route('/api/reset-db', methods=['GET', 'POST'])
def reset_db():
    """Reset database tables with LONGTEXT columns"""
    db.drop_all()
    db.create_all()
    return jsonify({'message': 'Database tables recreated with LONGTEXT!'})


@app.route('/api/seed', methods=['GET', 'POST'])
def seed_data():
    """Seed initial data"""
    db.create_all()
    
    if Project.query.count() == 0:
        projects = [
            Project(name='Consultation', description='Project Name, Location', image='https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=450&h=350&fit=crop'),
            Project(name='Design', description='Project Name, Location', image='https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=450&h=350&fit=crop'),
            Project(name='Marketing & Design', description='Project Name, Location', image='https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=450&h=350&fit=crop'),
            Project(name='Consultation & Marketing', description='Project Name, Location', image='https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=450&h=350&fit=crop'),
            Project(name='Consultation', description='Project Name, Location', image='https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=450&h=350&fit=crop'),
        ]
        db.session.add_all(projects)
    
    if Client.query.count() == 0:
        clients = [
            Client(name='Rowhan Smith', description='Real Trust helped us sell our home 20% above asking price. Their marketing strategy made all the difference!', designation='CEO, Foreclosure', image='https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200&h=200&fit=crop&crop=face'),
            Client(name='Shipra Kayak', description='From consultation to closing, the team was incredibly professional. They found our dream home within two weeks!', designation='Brand Designer', image='https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=200&h=200&fit=crop&crop=face'),
            Client(name='John Lepore', description='Outstanding service! Their design recommendations transformed our property and attracted multiple offers.', designation='CEO, Foreclosure', image='https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200&h=200&fit=crop&crop=face'),
            Client(name='Marry Freeman', description='The best real estate experience we have ever had. They truly understand the market and deliver exceptional results.', designation='Marketing Manager', image='https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200&h=200&fit=crop&crop=face'),
            Client(name='Lucy Chen', description='Highly recommend Real Trust! They made buying our first home stress-free and guided us through every step.', designation='Sales Rep', image='https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=200&h=200&fit=crop&crop=face'),
        ]
        db.session.add_all(clients)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Database initialized and seeded!',
        'projects': Project.query.count(),
        'clients': Client.query.count()
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Real Trust API is running!'})


@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Real Trust API - Visit /api/health for status'})


# ==================== MAIN ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
