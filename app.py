from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__, static_folder='build', static_url_path='/')
CORS(app, resources={r"/api/*": {"origins": os.getenv('REACT_APP_API_BASE_URL', '*')}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    details = db.Column(db.String(200), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'Email already exists'}), 400
    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    } for user in users])

@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    })

@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get_or_404(id)
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']
    user.password = data['password']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.password == data['password']:
        return jsonify({'message': 'Login successful', 'redirect': '/events'}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.get_json()
    try:
        event_datetime = datetime.strptime(data['datetime'], '%Y-%m-%dT%H:%M')
    except ValueError:
        return jsonify({'message': 'Invalid datetime format. Use YYYY-MM-DD HH:MM'}), 400
    new_event = Event(
        title=data['title'],
        details=data['details'],
        datetime=event_datetime,
        location=data['location']
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message': 'Event created successfully'}), 201

@app.route('/api/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([{
        'id': event.id,
        'title': event.title,
        'details': event.details,
        'datetime': event.datetime.strftime('%Y-%m-%dT%H:%M'),
        'location': event.location
    } for event in events])

@app.route('/api/events/<int:id>', methods=['GET'])
def get_event(id):
    event = Event.query.get_or_404(id)
    return jsonify({
        'title': event.title,
        'details': event.details,
        'datetime': event.datetime,
        'location': event.location
    })

@app.route('/api/events/<int:id>', methods=['PUT'])
def update_event(id):
    data = request.get_json()
    event = Event.query.get_or_404(id)
    event.title = data['title']
    event.details = data['details']
    event.datetime = data['datetime']
    event.location = data['location']
    db.session.commit()
    return jsonify({'message': 'Event updated successfully'})

@app.route('/api/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully'})

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/login', defaults={'path': '/login'})
@app.route('/register', defaults={'path': '/register'})
@app.route('/events', defaults={'path': '/events'})
def serve_react_app(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)