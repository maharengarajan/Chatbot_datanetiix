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


if __name__ == '__main__':
    app.run()