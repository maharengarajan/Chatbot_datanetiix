from flask import Flask, jsonify, request
from datetime import datetime
import requests
import re
import mysql.connector as conn
from config import DATABASE_CONFIG, DATABASE_CONNECTION_CONFIG

app = Flask(__name__)

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
    
    mydb = conn.connect(**DATABASE_CONFIG)
    cursor = mydb.cursor()

    # Insert user details into the 'new_client' table
    insert_query = "INSERT INTO new_client (NAME, EMAIL_ID, CONTACT_NUMBER) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (name, email, contact))
    mydb.commit()

    cursor.close()
    mydb.close()

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

    mydb = conn.connect(**DATABASE_CONFIG)
    cursor = mydb.cursor()

    # Convert lists to strings
    industry_str = ','.join(selected_industries)

    query = "INSERT INTO new_client (INDUSTRY) VALUES (%s)"
    values = (industry_str,)
    
    # Execute the query
    cursor.execute(query, values)
    
    # Commit the changes to the database
    mydb.commit()
    
    # Close the cursor and connection
    cursor.close()
    mydb.close() 

    return jsonify({'selected_industries': selected_industries})
    
if __name__ == '__main__':
    app.run()
