from flask import Flask, jsonify, request
from datetime import datetime
import re
import mysql.connector as conn
from config import DATABASE_CONFIG

app = Flask(__name__)

mydb = conn.connect(**DATABASE_CONFIG)
cursor = mydb.cursor()

@app.route('/chatbot/new_client', methods=['POST'])
def client():
    client_type = request.get_json().get('client_type')
    
    welcome_messages = {
        '1': 'Welcome, New client!',
        '2': 'Welcome, existing client!',
        '3': 'Welcome, Job seeker!',
        '4': 'Bye!'
    }   
    message = welcome_messages.get(client_type, 'Invalid option. Please choose a valid option.')   
    return jsonify({'message': message})

@app.route('/chatbot/new_client/user_details', methods=['POST'])
def user_details():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    contact = data.get('contact')

    if not is_valid_name(name):
        return jsonify({'message': 'Please enter a valid name.'})

    if not is_valid_email(email):
        return jsonify({'message': 'Please enter a valid email address.'})

    if not is_valid_contact_number(contact):
        return jsonify({'message': 'Please enter a valid contact number.'})
    
    user_details = {
        'name': name,
        'email': email,
        'contact': contact
    }

    return jsonify({'message': 'User details collected successfully.', 'data': user_details})

def is_valid_name(name):
    return bool(re.match(r'^[A-Za-z\s]+$', name.strip()))

def is_valid_email(email):
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))

def is_valid_contact_number(contact):
    return bool(re.match(r'^\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$', contact))

@app.route('/chatbot/new_client/user_details/industries', methods=['POST'])
def industries():
    industries = {
        '1': 'Insurance',
        '2': 'Banking',
        '3': 'Finance',
        '4': 'IT',
        '5': 'Healthcare',
        '6': 'Internet',
        '7': 'Automobile',
        '8': 'Others'
    }

    selected_options = request.get_json().get('selected_options', [])
    selected_industries = [industries[opt] for opt in selected_options if opt in industries]

    return jsonify({'selected_industries': selected_industries})

@app.route('/chatbot/new_client/user_details/industries/verticals', methods=['POST'])
def verticals():
    verticals = {
        '1': 'ML/DS/AI',
        '2': 'Sales force',
        '3': 'Microsoft dynamics',
        '4': 'Custom app',
        '5': 'Others'
    }

    selected_options = request.get_json().get('selected_options', [])
    selected_verticals = [verticals[opt] for opt in selected_options if opt in verticals]

    return jsonify({'selected_verticals': selected_verticals})

@app.route('/chatbot/new_client/user_details/industries/verticals/requirement', methods=['POST'])
def requirement():
    requirements = {
        '1': 'Start the project from scratch',
        '2': 'Require support from existing project',
        '3': 'Looking for some kind of solutions',
        '4': 'Others'
    }

    selected_option = request.get_json().get('selected_option')

    if selected_option in requirements:
        selected_requirement = requirements[selected_option]
        return jsonify({'selected_requirement': selected_requirement})
    else:
        return jsonify({'message': 'Please choose a valid option.'})

@app.route('/chatbot/new_client/user_details/industries/verticals/requirement/known_source', methods=['POST'])
def known_source():
    known_sources = {
        '1': 'Google',
        '2': 'LinkedIn',
        '3': 'Email Campaign',
        '4': 'Known resources',
        '5': 'Others'
    }

    selected_option = request.get_json().get('selected_option')

    if selected_option in known_sources:
        if selected_option in ['4', '5']:
            source_specification = request.get_json().get('source_specification')
            selected_known_source = known_sources[selected_option] + " : " + source_specification
        else:
            selected_known_source = known_sources[selected_option]
        return jsonify({'selected_known_source': selected_known_source})
    else:
        return jsonify({'message': 'Please choose a valid option.'})
    
@app.route('/chatbot/new_client/store_conversation', methods=['POST'])
def store_conversation():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    contact = data.get('contact')
    selected_industries = data.get('selected_industries')
    selected_verticals = data.get('selected_verticals')
    selected_requirement = data.get('selected_requirement')
    selected_known_source = data.get('selected_known_source')

    # Get current date and time
    current_date = datetime.now().date()
    current_time = datetime.now().time()

    # Convert lists to strings
    industry_str = ','.join(selected_industries)
    vertical_str = ','.join(selected_verticals)

    query = "INSERT INTO new_client (DATE, TIME, NAME, EMAIL_ID, CONTACT_NUMBER, INDUSTRY, VERTICAL, REQUIREMENTS, KNOWN_SOURCE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (current_date, current_time, name, email, contact, industry_str, vertical_str, selected_requirement, selected_known_source)

    # Execute the query
    cursor.execute(query, values)
    
    # Commit the changes to the database
    mydb.commit()
    
    # Close the cursor and connection
    cursor.close()
    mydb.close() 

    return jsonify({'message': 'Conversation details stored successfully.'})


if __name__ == '__main__':
    app.run()
