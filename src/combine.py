from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    client_types = {
        '1': 'New client',
        '2': 'Existing client',
        '3': 'Job seeker',
        '4': 'Exit'
    }

    data = request.get_json()
    client_type = data.get('client_type')

    if client_type in client_types:
        if client_type == '1':
            response_msg = 'Welcome, New client!'
        elif client_type == '2':
            response_msg = 'Welcome, existing client!'
        elif client_type == '3':
            response_msg = 'Welcome, Job seeker!'
        elif client_type == '4':
            response_msg = 'Bye!'
        else:
            return jsonify({'message': 'Invalid option. Please choose a valid option.'})

        name = data.get('name')
        email = data.get('email')
        contact = data.get('contact')

        if not (name and email and contact):
            return jsonify({'message': 'Please provide name, email, and contact.'})

        if not is_valid_name(name):
            return jsonify({'message': 'Please enter a valid name.'})

        if not is_valid_email(email):
            return jsonify({'message': 'Please enter a valid email address.'})

        if not is_valid_contact_number(contact):
            return jsonify({'message': 'Please enter a valid contact number.'})

        return jsonify({'message': response_msg, 'user_details': {'name': name, 'email': email, 'contact': contact}})

    else:
        return jsonify({'message': 'Invalid option. Please choose a valid option.'})


def is_valid_name(name):
    return re.match(r'^[A-Za-z\s]+$', name.strip()) is not None

def is_valid_email(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is not None

def is_valid_contact_number(contact):
    return re.match(r'^\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$', contact) is not None

if __name__ == '__main__':
    app.run()
