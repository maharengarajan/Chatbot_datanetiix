from flask import Flask, jsonify, request
from datetime import datetime
import requests
import re

app = Flask(__name__)

def get_ip_address():
    try:
        response = requests.get('https://api.ipify.org').text
        return response
    except requests.RequestException:
        return None
    
def get_location():
    ip_address = get_ip_address()
    if not ip_address:
        return None
    try:
        response = requests.get(f'https://ipapi.co/{ip_address}/city/').text
        return response
    except requests.RequestException:
        return None
    
def get_weather():
    city = get_location()
    if not city:
        return None
    try:
        weather_api_key = '01e6399113b4c255c497958efccc0dc9'
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}"
        response = requests.get(url).json()

        if response.get('cod') == 200:
            weather_desc = response['weather'][0]['main'].lower()
            return weather_desc
        else:
            return None
    except requests.RequestException:
        return None
    
def weather_greeting():
    weather_desc = get_weather()
    if weather_desc is None:
        return None
    
    if weather_desc in ['thunderstorm', 'drizzle', 'rain', 'snow']:
        return f"It seems like there's {weather_desc} outside. Stay safe!"
    elif weather_desc in ['atmosphere', 'clear', 'clouds']:
        return f"Enjoy the {weather_desc} weather!"
    elif weather_desc in ['mist', 'smoke', 'haze', 'dust', 'fog', 'sand', 'ash']:
        return f"Be cautious as there's {weather_desc} in the air."
    elif weather_desc in ['squall', 'tornado']:
        return f"Take extra precautions due to {weather_desc} in the area."
    else:
        return None
    
@app.route('/greeting', methods=['GET'])
def get_greeting():
    ip_location = get_location()
    weather_info_greet = weather_greeting()
    greeting = "Hello, buddy! Welcome to Datanetiix!"
    if ip_location and weather_info_greet:
        message_1 = f"{greeting} We hope you're connecting from {ip_location}. {weather_info_greet}"
        return jsonify({'message': message_1})
    else:
        message_2 = greeting
        return jsonify({'message': message_2})
        
@app.route('/client', methods=['POST'])
def client():
    client_type = request.get_json().get('client_type')

    if client_type == '1':
        return jsonify({'message': 'Welcome, New client!'})
    elif client_type == '2':
        return jsonify({'message': 'Welcome, existing client!'})
    elif client_type == '3':
        return jsonify({'message': 'Welcome, Job seeker!'})
    elif client_type == '4':
        return jsonify({'message': 'Bye!'})
    else:
        return jsonify({'message': 'Invalid option. Please choose a valid option.'})

@app.route('/user_details', methods=['POST'])
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
    if re.match(r'^[A-Za-z\s]+$', name.strip()):
        return True
    else:
        return False

def is_valid_email(email):
    if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        return True
    else:
        return False

def is_valid_contact_number(contact):
    if re.match(r'^\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$', contact):
        return True
    else:
        return False
    
@app.route('/industries', methods=['POST'])
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

@app.route('/verticals', methods=['POST'])
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

@app.route('/requirement', methods=['POST'])
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

@app.route('/known_source', methods=['POST'])
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
    
@app.route('/issue_escalation', methods=['POST'])
def issue_escalation():
    issue_escalation_options = {
        '1': 'Team Lead',
        '2': 'Sales Person',
        '3': 'Escalate Issue'
    }
    selected_option = request.get_json().get('selected_option')
    if selected_option in issue_escalation_options:
        selected_issue_escalation = issue_escalation_options[selected_option]
        return jsonify({'selected_isse_type': selected_issue_escalation})
    else:
        return jsonify({'message': 'Please choose a valid option.'})
    
@app.route('/issue_type', methods=['POST'])
def issue_type():
    issue_type_options = {
        '1': 'Normal',
        '2': 'Urgent'
    }
    user_response = request.get_json().get('user_response')
    if user_response in issue_type_options:
        selected_issue_escalation=issue_type_options[user_response]
        return jsonify({'user_response':selected_issue_escalation})
    else:
        return jsonify({'message': 'Please choose a valid option.'})
    
@app.route('/interview_avail', methods=['POST'])
def interview_available_check():
    interview_avail_options = {
        '1': 'Yes',
        '2': 'No'
    }
    user_response = request.get_json().get('user_response')
    if user_response in interview_avail_options:
        selected_interview_avail=interview_avail_options[user_response]
        return jsonify({'selected_interview_avail':selected_interview_avail})
    else:
        return jsonify({'message': 'Please choose a valid option.'})
    
@app.route('/date-of-interview', methods=['POST'])
def date_of_interview():
    data = request.get_json()
    time_avail = data.get('time_avail')

    try:
        datetime.strptime(time_avail, "%d/%m/%Y")
        if datetime.strptime(time_avail, "%d/%m/%Y").date() < datetime.now().date():
            return jsonify({"error": "Please enter a valid future date"}), 400
        else:
            return jsonify({"time_avail": time_avail})
    except ValueError:
        return jsonify({"error": "Invalid date format. Please enter the date in dd/mm/yyyy format."}), 400
    
@app.route('/notice-period', methods=['POST'])
def notice_period():
    notice_period_options = {
        '1': '30 days',
        '2': '60 days',
        '3': '90 days'
    }
    data = request.get_json()
    joining_date = data.get('joining_date')

    if joining_date in notice_period_options:
        return jsonify({"joining_date": notice_period_options[joining_date]})
    else:
        return jsonify({"error": "Invalid input. Please select a valid option."}), 400

if __name__ == '__main__':
    app.run()