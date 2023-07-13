from flask import Flask, jsonify
import requests

app = Flask(__name__)

def get_ip_address():
    response = requests.get('https://api.ipify.org').text
    return response

def get_location():
    ip_address = get_ip_address()
    response = requests.get(f'https://ipapi.co/{ip_address}/city/').text
    city = response
    return city

def get_weather():
    city = get_location()
    weather_api_key = '01e6399113b4c255c497958efccc0dc9'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}"
    response = requests.get(url).json()

    if response['cod'] == 200:
        weather_desc = response['weather'][0]['main']
        return weather_desc
    else:
        return "Sorry, I couldn't retrieve the weather information."

def get_weather_greeting():
    weather_desc = get_weather()
    if weather_desc in ['Thunderstorm', 'Drizzle', 'Rain', 'Snow']:
        return "It seems like there's {} outside. Stay safe!".format(weather_desc)
    elif weather_desc in ['Atmosphere', 'Clear', 'Clouds']:
        return "Enjoy the {} weather!".format(weather_desc)
    elif weather_desc in ['Mist', 'Smoke', 'Haze', 'Dust', 'Fog', 'Sand', 'Ash']:
        return "Be cautious as there's {} in the air.".format(weather_desc)
    elif weather_desc in ['Squall', 'Tornado']:
        return "Take extra precautions due to {} in the area.".format(weather_desc)
    else:
        return "Enjoy your time!"

@app.route('/greeting', methods=['GET'])
def get_greeting():
    ip_location = get_location()
    weather_info_greet = get_weather_greeting()
    greeting = "Hello, buddy! Welcome to Datanetiix! We hope you're connecting from"
    message = "{} {}. {}".format(greeting, ip_location, weather_info_greet)
    return jsonify({'message': message})

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

if __name__ == '__main__':
    app.run()