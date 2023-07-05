from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/get_valid_name', methods=['POST'])
def validate_name():
    name = request.json.get('name')
    if name and re.match(r'^[A-Za-z\s]+$', name):
        return jsonify({'message': 'Name is valid'})
    else:
        return jsonify({'message': 'Please enter a valid name'})

@app.route('/get_valid_email', methods=['POST'])
def validate_email():
    email = request.json.get('email')
    if email and re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        return jsonify({'message': 'Email is valid'})
    else:
        return jsonify({'message': 'Please enter a valid email'})

@app.route('/get_valid_contact_number', methods=['POST'])
def validate_contact_number():
    contact = request.json.get('contact')
    if contact and re.match(r'^\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$', contact):
        return jsonify({'message': 'Contact number is valid'})
    else:
        return jsonify({'message': 'Please enter a valid contact number'})

if __name__ == '__main__':
    app.run(debug=True)

