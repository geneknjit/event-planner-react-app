from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os
import pyodbc
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='build', static_url_path='/')
CORS(app, resources={r"/api/*": {"origins": os.getenv('REACT_APP_API_BASE_URL', '*')}})

# Azure SQL Database connection string
connection_string = os.getenv('AZURE_SQL_CONNECTION_STRING')

# Create a connection to the database
def get_db_connection():
    conn = pyodbc.connect(connection_string)
    return conn

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Users (first_name, last_name, email, password)
        VALUES (?, ?, ?, ?)
    """, data['first_name'], data['last_name'], data['email'], data['password'])
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([{
        'id': user[0],
        'first_name': user[1],
        'last_name': user[2],
        'email': user[3]
    } for user in users])

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Users WHERE email = ? AND password = ?
    """, data['email'], data['password'])
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return jsonify({'message': 'Login successful', 'redirect': '/events'}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.get_json()
    # Parse the input datetime string into a Python datetime object
    event_datetime = datetime.strptime(data['datetime'], '%Y-%m-%dT%H:%M')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Events (title, details, datetime, location)
        VALUES (?, ?, ?, ?)
    """, data['title'], data['details'], event_datetime, data['location'])
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Event created successfully'}), 201

@app.route('/api/events', methods=['GET'])
def get_events():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Events")
    events = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([{
        'id': event[0],
        'title': event[1],
        'details': event[2],
        'datetime': event[3],
        'location': event[4]
    } for event in events])

@app.route('/api/events/<int:id>', methods=['GET'])
def get_event(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Events WHERE id = ?", id)
    event = cursor.fetchone()
    cursor.close()
    conn.close()
    if event:
        return jsonify({
            'id': event[0],
            'title': event[1],
            'details': event[2],
            'datetime': event[3],
            'location': event[4]
        })
    else:
        return jsonify({'message': 'Event not found'}), 404

@app.route('/api/events/<int:id>', methods=['PUT'])
def update_event(id):
    data = request.get_json()
    # Parse the input datetime string into a Python datetime object
    event_datetime = datetime.strptime(data['datetime'], '%Y-%m-%dT%H:%M')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Events
        SET title = ?, details = ?, datetime = ?, location = ?
        WHERE id = ?
    """, data['title'], data['details'], event_datetime, data['location'], id)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Event updated successfully'})

@app.route('/api/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Events WHERE id = ?", id)
    conn.commit()
    cursor.close()
    conn.close()
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
    app.run(debug=True)