from flask import Flask,request,jsonify
import requests

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
    
if __name__ == '__main__':
    app.run()



    