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

#this API responsible for choosing client type
@app.route('/chatbot/client', methods=['POST'])
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

#this API responsible for collecting user details from new client and save in DB
@app.route('/chatbot/new_client_details', methods=['POST'])
def new_client_details():
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

# this API is responsible for selecting industries
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

    selected_options = data.get('selected_options', [])
    selected_industries = [industries[opt] for opt in selected_options if opt in industries]

    industry_str = ','.join(selected_industries) # Convert lists to strings

    query = "UPDATE new_client SET INDUSTRY = %s WHERE ID = %s"
    values = (industry_str,row_id)
    cursor.execute(query, values)
    mydb.commit()

    return jsonify({'selected_industries': selected_industries})

# this API is responsible for selecting verticals
@app.route('/chatbot/new_client/user_details/industries/verticals', methods=['POST'])
def verticals_new_client():
    verticals = {
        '1': 'ML/DS/AI',
        '2': 'Sales force',
        '3': 'Microsoft dynamics',
        '4': 'Custom app',
        '5': 'Others'
    }

    data = request.get_json()
    row_id = data.get('row_id')  # Get the user ID from the request

    selected_options = data.get('selected_options', [])
    selected_verticals = [verticals[opt] for opt in selected_options if opt in verticals]

    vertical_str = ','.join(selected_verticals)

    query = "UPDATE new_client SET VERTICAL = %s WHERE ID = %s"
    values = (vertical_str,row_id)
    cursor.execute(query, values)
    mydb.commit()

    return jsonify({'selected_verticals': selected_verticals})

# this API is responsible for selecting requirements
@app.route('/chatbot/new_client/user_details/industries/verticals/requirement', methods=['POST'])
def requirement():
    requirements = {
        '1': 'Start the project from scratch',
        '2': 'Require support from existing project',
        '3': 'Looking for some kind of solutions',
        '4': 'Others'
    }

    data = request.get_json()
    selected_option = data.get('selected_option')
    row_id = data.get('row_id')  # Get the user ID from the request

    if selected_option in requirements:
        selected_requirement = requirements[selected_option]

        query = "UPDATE new_client SET REQUIREMENTS = %s WHERE ID = %s"
        values = (selected_requirement,row_id)
        cursor.execute(query, values)
        mydb.commit()

        return jsonify({'selected_requirement': selected_requirement})
    else:
        return jsonify({'message': 'Please choose a valid option.'})

# this API is responsible for selecting known sources    
@app.route('/chatbot/new_client/user_details/industries/verticals/requirement/known_source', methods=['POST'])
def known_source():
    known_sources = {
        '1': 'Google',
        '2': 'LinkedIn',
        '3': 'Email Campaign',
        '4': 'Known resources',
        '5': 'Others'
    }

    data = request.get_json()
    selected_option = data.get('selected_option')
    row_id = data.get('row_id')  # Get the user ID from the request

    if selected_option in known_sources:
        if selected_option in ['4', '5']:
            source_specification = request.get_json().get('source_specification')
            selected_known_source = known_sources[selected_option] + " : " + source_specification
        else:
            selected_known_source = known_sources[selected_option]

        query = "UPDATE new_client SET KNOWN_SOURCE = %s WHERE ID = %s"
        values = (selected_known_source,row_id)
        cursor.execute(query, values)
        mydb.commit()

        # Close the cursor and connection
        cursor.close()
        mydb.close()

        return jsonify({'selected_known_source': selected_known_source})
    else:
        return jsonify({'message': 'Please choose a valid option.'})
    
#this API responsible for collecting user details
@app.route('/chatbot/existing_client_details', methods=['POST'])
def existing_client_details():
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

    query = "INSERT INTO existing_client (DATE, TIME, NAME, EMAIL_ID, CONTACT_NUMBER) VALUES (%s, %s, %s, %s, %s)"
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

# this API is responsible for selecting verticals for existing client and save in DB
@app.route('/chatbot/existing_client_details/verticals', methods=['POST'])
def verticals_exixting_client():
    verticals = {
        '1': 'ML/DS/AI',
        '2': 'Sales force',
        '3': 'Microsoft dynamics',
        '4': 'Custom app',
        '5': 'Others'
    }

    data = request.get_json()
    row_id = data.get('row_id')  

    selected_options = data.get('selected_options', [])
    selected_verticals = [verticals[opt] for opt in selected_options if opt in verticals]

    vertical_str = ','.join(selected_verticals)

    query = "UPDATE existing_client SET VERTICAL = %s WHERE ID = %s"
    values = (vertical_str,row_id)
    cursor.execute(query, values)
    mydb.commit()

    return jsonify({'selected_verticals': selected_verticals})

# this API is responsible for selecting issue_escalation for existing client and save in DB
@app.route('/chatbot/existing_client_details/verticals/issue_escalation', methods=['POST'])
def issue_escalation():
    issue_escalation_options = {
        '1': 'Team Lead',
        '2': 'Sales Person',
        '3': 'Escalate Issue'
    }

    data = request.get_json()
    row_id = data.get('row_id')

    selected_option = data.get('selected_option')
    if selected_option in issue_escalation_options:
        selected_issue_escalation = issue_escalation_options[selected_option]

        query = "UPDATE existing_client SET ISSUE_ESCALATION = %s WHERE ID = %s"
        values = (selected_issue_escalation,row_id)
        cursor.execute(query, values)
        mydb.commit()

        return jsonify({'selected_isse_type': selected_issue_escalation})
    else:
        return jsonify({'message': 'Please choose a valid option.'})

# this API is responsible for selecting issue_type for existing client and save in DB    
@app.route('/chatbot/existing_client_details/verticals/issue_escalation/issue_type', methods=['POST'])
def issue_type():
    issue_type_options = {
        '1': 'Normal',
        '2': 'Urgent'
    }

    data = request.get_json()
    row_id = data.get('row_id')

    user_response = data.get('user_response')
    if user_response in issue_type_options:
        selected_issue_type=issue_type_options[user_response]

        if selected_issue_type == 'Normal':
            response_message = "Thank you. We have saved your issue and will contact you as soon as possible."
        elif selected_issue_type == 'Urgent':
            response_message = "Thank you. We have saved your issue as urgent and will contact you immediately."

        query = "UPDATE existing_client SET ISSUE_TYPE = %s WHERE ID = %s"
        values = (selected_issue_type,row_id)
        cursor.execute(query, values)
        mydb.commit()

        return jsonify({'user_response':selected_issue_type, 'message': response_message})
    else:
        return jsonify({'message': 'Please choose a valid option.'})
    
#this API responsible for collecting user details from job seeker and save in DB
@app.route('/chatbot/job_seeker_details', methods=['POST'])
def job_seeker_details():
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

    query = "INSERT INTO job_seeker (DATE, TIME, NAME, EMAIL_ID, CONTACT_NUMBER) VALUES (%s, %s, %s, %s, %s)"
    values = (current_date, current_time, name, email, contact)
    cursor.execute(query, values)
    row_id = cursor.lastrowid 
    mydb.commit()  

    return jsonify({'message': 'User details collected successfully.', 'row_id': row_id})

def is_valid_name(name):
    return bool(re.match(r'^[A-Za-z\s]+$', name.strip()))

def is_valid_email(email):
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))

def is_valid_contact_number(contact):
    return bool(re.match(r'^\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$', contact))

#this API responsible for collecting user category of job seeker and save in DB
@app.route('/chatbot/job_seeker_details/category', methods=['POST'])
def category():
    category_type = {
        '1': 'fresher',
        '2': 'experienced'
    }

    data = request.get_json()
    row_id = data.get('row_id')
    
    user_type = data.get('user_type')
    if user_type in category_type:
        selected_category_type = category_type[user_type]

        query = "UPDATE job_seeker SET category = %s WHERE ID = %s"
        values = (selected_category_type,row_id)
        cursor.execute(query, values)
        mydb.commit()

        return jsonify({'user_type': selected_category_type, 'row_id': row_id})
    else:
        return jsonify({'message': 'Please choose a valid option.'})
    
# this API is responsible for selecting verticals for job seeker and save in DB
@app.route('/chatbot/job_seeker_details/category/verticals', methods=['POST'])
def verticals_job_seeker():
    verticals = {
        '1': 'ML/DS/AI',
        '2': 'Sales force',
        '3': 'Microsoft dynamics',
        '4': 'Custom app',
        '5': 'Others'
    }

    data = request.get_json()
    row_id = data.get('row_id')  

    selected_options = data.get('selected_options', [])
    selected_verticals = [verticals[opt] for opt in selected_options if opt in verticals]

    vertical_str = ','.join(selected_verticals)

    query = "UPDATE job_seeker SET VERTICAL = %s WHERE ID = %s"
    values = (vertical_str,row_id)
    cursor.execute(query, values)
    mydb.commit()

    return jsonify({'selected_verticals': selected_verticals})

#this API responsible for checking user availability for an interview
@app.route('/chatbot/job_seeker_details/category/verticals/interview_avail', methods=['POST'])
def interview_available_check():
    interview_avail_options = {
        '1': 'Yes',
        '2': 'No'
    }

    data = request.get_json()
    row_id = data.get('row_id')

    user_response = data.get('user_response')
    if user_response in interview_avail_options:
        selected_interview_avail=interview_avail_options[user_response]

        query = "UPDATE job_seeker SET INTERVIEW_AVAILABLE = %s WHERE ID = %s"
        values = (selected_interview_avail,row_id)
        cursor.execute(query, values)
        mydb.commit()

        return jsonify({'selected_interview_avail':selected_interview_avail, 'row_id':row_id})
    else:
        return jsonify({'message': 'Please choose a valid option.'})

#this API responsible for checking date for an interview  
# in the frontend we have to provide calender    
@app.route('/chatbot/job_seeker_details/category/verticals/interview_avail/date_of_interview', methods=['POST'])
def date_of_interview():
    data = request.get_json()
    row_id = data.get('row_id')
    interview_date = data.get('interview_date')

    query = "UPDATE job_seeker SET TIME_AVAILABLE = %s WHERE ID = %s"
    values = (interview_date,row_id)
    cursor.execute(query, values)
    mydb.commit()
    return jsonify({'interview_date': interview_date, 'row_id':row_id})

@app.route('/chatbot/job_seeker_details/category/verticals/interview_avail/date_of_interview/notice_period', methods=['POST'])
def notice_period():
    notice_period_options = {
        '1': '30 days',
        '2': '60 days',
        '3': '90 days'
    }
    data = request.get_json()
    row_id = data.get('row_id')

    joining_date = data.get('joining_date')
    if joining_date in notice_period_options:
        selected_notice_period_options = notice_period_options[joining_date]

        query = "UPDATE job_seeker SET NOTICE_PERIOD = %s WHERE ID = %s"
        values = (selected_notice_period_options,row_id)
        cursor.execute(query, values)
        mydb.commit()

        return jsonify({"joining_date": selected_notice_period_options, 'row_id': row_id})
    else:
        return jsonify({"error": "Invalid input. Please select a valid option."}), 400

 
    
        
if __name__ == '__main__':
    app.run()