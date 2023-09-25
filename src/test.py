from flask import Flask, jsonify, request
from datetime import datetime
import re
import mysql.connector as conn
from config import DATABASE_CONFIG

app = Flask(__name__)

mydb = conn.connect(**DATABASE_CONFIG)
cursor = mydb.cursor()

current_date = datetime.now().date()
current_time = datetime.now().time()

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

    query = "INSERT INTO new_client (DATE, TIME, NAME, EMAIL_ID, CONTACT_NUMBER) VALUES (%s, %s, %s, %s, %s)"
    values = (current_date, current_time, name, email, contact)
    cursor.execute(query, values)
    row_id = cursor.lastrowid # Get the ID (primary key) of the inserted row
    mydb.commit()  # Commit the changes to the database

    return jsonify({'message': 'User details collected successfully.', 'row_id': row_id})

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
    data = request.get_json()
    row_id = data.get('row_id')  # Get the user ID from the request

    selected_options = request.get_json().get('selected_options', [])
    selected_industries = [industries[opt] for opt in selected_options if opt in industries]

    industry_str = ','.join(selected_industries) # Convert lists to strings

    query = "UPDATE new_client SET INDUSTRY = %s WHERE ID = %s"
    values = (industry_str,row_id)
    cursor.execute(query, values)
    mydb.commit()

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

    data = request.get_json()
    row_id = data.get('row_id')  # Get the user ID from the request

    selected_options = request.get_json().get('selected_options', [])
    selected_verticals = [verticals[opt] for opt in selected_options if opt in verticals]

    vertical_str = ','.join(selected_verticals)

    query = "UPDATE new_client SET VERTICAL = %s WHERE ID = %s"
    values = (vertical_str,row_id)
    cursor.execute(query, values)
    mydb.commit()

    # Close the cursor and connection
    #cursor.close()
    #mydb.close()

    return jsonify({'selected_verticals': selected_verticals})


if __name__ == '__main__':
    app.run()