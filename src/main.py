import requests
import re
from datetime import datetime
from database import insert_new_client, insert_existing_client, insert_job_seeker, create_database
from database import extract_new_client_details, extract_existing_client_details, extract_job_seeker_details
from config import email_alert_config
from alert import send_email
from dotenv import load_dotenv
import os


create_database()

def configure():
    load_dotenv()

def get_ip_address():
    response = requests.get('https://api.ipify.org').text #completely free 
    return response

def get_location():
    ip_address = get_ip_address()
    response = requests.get(f'https://ipapi.co/{ip_address}/city/').text #Up-to 30000 free requests per month (1000 in 24 hours)
    city = response
    return city

def get_weather():
    city = get_location()
    configure()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('weather_api_key')}"
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
    
def get_valid_name():
    while True:
        name = input('Please enter your name: ')
        if re.match(r'^[A-Za-z\s]+$', name.strip()):
            return name
        else:
            print("Please enter a valid name")
            
def get_valid_email():
    while True:
        email = input('Please enter your email: ')
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            return email
        else:
            print('Please enter a valid email address')
            
def get_valid_contact_number():
    while True:
        contact = input('Please enter your contact number: ')
        if re.match(r'^\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$', contact):
            return contact
        else:
            print('Please enter your contact number')
            
def get_user_details():
    name = get_valid_name()
    email = get_valid_email()
    contact = get_valid_contact_number()
    return name, email, contact

def choose_industries_option():
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
    valid_options = industries.keys()
    while True:
        print('Please choose an industry option: ')
        for option, industry in industries.items():
            print(f"{option}.{industry}")
        option = input("Enter your option(s) separated by commas: ")
        options = [opt.strip() for opt in option.split(',') if opt.strip() in valid_options]
        if options:
            return [industries[opt] for opt in options]
        else:
            print("Please choose valid option(s)")
            
def choose_vertical_option():
    verticals = {
        '1': 'ML/DS/AI',
        '2': 'Sales force',
        '3': 'Microsoft dynamics',
        '4': 'Custom app',
        '5': 'Others'
    }
    valid_options = verticals.keys()
    while True:
        print("Please choose a vertical option:")
        for option, vertical in verticals.items():
            print(f"{option}. {vertical}")
        option = input("Enter your option(s) separated by commas: ")
        options = [opt.strip() for opt in option.split(',') if opt.strip() in valid_options]
        if options:
            return [verticals[opt] for opt in options]
        else:
            print("Please choose valid option(s)")
            
def choose_requirement():
    requirements = {
        '1': 'Start the project from scratch',
        '2': 'Require support from existing project',
        '3': 'Looking for some kind of solutions',
        '4': 'Others'
    }
    
    while True:
        print("Please choose your requirement:")
        for option, requirement in requirements.items():
            print(f"{option}. {requirement}")
            
        option = input("Enter your option: ")
        
        if option.strip() in requirements:
            return requirements[option.strip()]
        else:
            print("Please choose a valid option.")
            
def choose_known_source():
    known_sources = {
        '1': 'Google',
        '2': 'LinkedIn',
        '3': 'Email Campaign',
        '4': 'Known resources',
        '5': 'Others'
    }

    while True:
        print("How did you hear about us?")
        for option, known_source in known_sources.items():
            print(f"{option}. {known_source}")

        option = input("Enter your option: ")

        if option.strip() in known_sources:
            if option.strip() in ['4', '5']:
                source_specification = input("Please specify: ")
                return known_sources[option.strip()] + " : " + source_specification
            else:
                return known_sources[option.strip()]
        else:
            print("Please choose a valid option.")
            
def issue_escalation():
    issue_escalation_options = {
        '1': 'Team Lead',
        '2': 'Sales Person',
        '3': 'Escalate Issue'
    }
    
    while True:
        print("Who would you like to speak to?")
        for option, person in issue_escalation_options.items():
            print(f"{option}. {person}")
            
        option = input("Your choice: ")
        
        if option.strip() in issue_escalation_options:
            return issue_escalation_options[option.strip()]
        else:
            print("Please choose valid option(s)")
            
def issue_type():
    while True:
        print("Is your issue normal or urgent?")
        issue_type_options = ['1. normal', '2. urgent']
        response = input("Enter '1' for normal or '2' for urgent: ")
        if response == "1":
            print("Thank you. We have saved your issue and will contact you as soon as possible.")
            return "normal"  # Return as a string
        elif response == "2":
            print("Thank you. We have saved your issue as urgent and will contact you immediately.")
            return "urgent"  # Return as a string
        else:
            print("Please choose a valid option.")
            
def category():
    while True:
        user_type = input("Are you an experienced or fresher? (Enter 1 for experienced, 2 for fresher): ")
        if user_type == "1":
            user_category = "experienced"
            break  # Exit the loop when a valid option is chosen
        elif user_type == "2":
            user_category = "fresher"
            break  # Exit the loop when a valid option is chosen
        else:
            print("Invalid input. Please try again.")
    return user_category

def interview_available_check():
    while True:
        interview_avail = input("Are you available for an interview? (1 for yes, 2 for no): ")
        if interview_avail == "1":
            interview_available = "yes"
            return interview_available
        elif interview_avail == "2":
            interview_available = "no"
            print("Thank you for your time. We will get in touch with you later.")
            return interview_available
        else:
            print("Invalid input. Please select a valid option.")
            
def date_of_interview():
    while True:
        try:
            time_avail = input("What is your time availability for an interview? (Please enter a date in dd/mm/yyyy format): ")
            datetime.strptime(time_avail, "%d/%m/%Y")
            if datetime.strptime(time_avail, "%d/%m/%Y").date() < datetime.now().date():
                print("Please enter a valid future date")
            else:
                return time_avail
        except ValueError:
            print("Invalid date format. Please enter the date in dd/mm/yyyy format.")
            
def notice_period():
    while True:
        joining_date = input("When can you join? (1 for 30 days/2 for 60 days/3 for 90 days): ")
        if joining_date == '1':
            joining_date = '30 days'
            return joining_date
        elif joining_date == '2':
            joining_date = '60 days'
            return joining_date
        elif joining_date == '3':
            joining_date = '90 days'
            return joining_date
        else:
            print("Invalid input. Please select a valid option.")
            
ip_location = get_location()
weather_info = get_weather()
weather_info_greet = get_weather_greeting()

greeting = "Hello, buddy! Welcome to Datanetiix! We hope you're connecting from"
print(greeting, ip_location, weather_info_greet)

            
client_type = input("Can you please let me know if you are a? (Enter 1 for new client, 2 for existing client, 3 for job seeker, 4 to exit): ")

if client_type == '1':
    print("Welcome, New client!")
    try:
        name, email, contact = get_user_details()
        industry_options = choose_industries_option()
        vertical_options = choose_vertical_option()
        requirement_option = choose_requirement()
        known_source = choose_known_source()
        
        # Insert new client into the database
        insert_new_client(name, email, contact, industry_options, vertical_options, requirement_option, known_source)

        # Extract the new client details from the database
        new_client_details = extract_new_client_details()
        
        if new_client_details:
            # Send email with the new client details
            sender_email = email_alert_config['sender_email']
            receiver_emails = email_alert_config['receiver_emails']
            cc_email = email_alert_config['cc_email']
            subject = 'Datanetiix chatbot project Email alert testing demo'
            email_message = f"Hi, new user logged in our chatbot, Find the below details for your reference:\n\n" \
                            f"New client details:\n\n" \
                            f"Date: {new_client_details['date']}\n" \
                            f"Time: {new_client_details['time']}\n" \
                            f"Name: {new_client_details['name']}\n" \
                            f"Email: {new_client_details['email']}\n" \
                            f"Contact: {new_client_details['contact']}\n" \
                            f"Industries: {new_client_details['industries_choosen']}\n" \
                            f"Verticals: {new_client_details['verticals_choosen']}\n" \
                            f"Requirements: {new_client_details['requirement']}\n" \
                            f"Known Source: {new_client_details['known_source']}"
            send_email(sender_email, receiver_emails, cc_email, subject, email_message)


    except Exception as e:
        print(str(e))

elif client_type == '2':
    print("Welcome, existing client!")
    try:
        name, email, contact = get_user_details()
        vertical_options = choose_vertical_option()
        issue_escalation = issue_escalation()
        issue_type = issue_type()
        
        # Insert existing client into the database
        insert_existing_client(name, email, contact, vertical_options, issue_escalation , issue_type)

        # Extract the new client details from the database
        existing_client_details = extract_existing_client_details()

        if existing_client_details:
            # Send email with the existing client details
            sender_email = email_alert_config['sender_email']
            receiver_emails = email_alert_config['receiver_emails']
            cc_email = email_alert_config['cc_email']
            subject = 'Datanetiix chatbot project Email alert testing demo'
            email_message = f"Hi, one of our client logged in our chatbot, Find the below details for your reference:\n\n" \
                            f"Existing client details:\n\n" \
                            f"Date: {existing_client_details['date']}\n" \
                            f"Time: {existing_client_details['time']}\n" \
                            f"Name: {existing_client_details['name']}\n" \
                            f"Email: {existing_client_details['email']}\n" \
                            f"Contact: {existing_client_details['contact']}\n" \
                            f"Verticals: {existing_client_details['verticals_choosen']}\n" \
                            f"Escalating issue to: {existing_client_details['issue_escalation']}\n" \
                            f"Type of issue: {existing_client_details['issue_type']}"
            send_email(sender_email, receiver_emails, cc_email, subject, email_message)
   
    except Exception as e:
        print(str(e))
        
elif client_type == '3':
    print("Welcome, Job seeker!")
    try:
        name, email, contact = get_user_details()
        user_category = category()
        vertical_options = choose_vertical_option()
        is_available = interview_available_check()
        if is_available == "yes":
            interview_date = date_of_interview()
        else:
            interview_date = None
        joining_date =notice_period()
        
        # Insert existing client into the database
        insert_job_seeker(name, email, contact,user_category, vertical_options, is_available, interview_date, joining_date)

        # Extract the new client details from the database
        job_seeker_details = extract_job_seeker_details()

        if job_seeker_details:
            # Send email with the job seeker details
            sender_email = email_alert_config['sender_email']
            receiver_emails = email_alert_config['receiver_emails']
            cc_email = email_alert_config['cc_email']
            subject = 'Datanetiix chatbot project Email alert testing demo'
            email_message = f"Hi, New job seeker logged in our chatbot, Find the below details for your reference:\n\n" \
                            f"Job Seeker details:\n\n" \
                            f"Date: {job_seeker_details['date']}\n" \
                            f"Time: {job_seeker_details['time']}\n" \
                            f"Name: {job_seeker_details['name']}\n" \
                            f"Email: {job_seeker_details['email']}\n" \
                            f"Contact: {job_seeker_details['contact']}\n" \
                            f"User category: {job_seeker_details['category']}\n" \
                            f"Verticals: {job_seeker_details['verticals_choosen']}\n" \
                            f"Available for Interview: {job_seeker_details['interview_available']}\n" \
                            f"Available date for interview: {job_seeker_details['time_available']}\n" \
                            f"Notice period: {job_seeker_details['notice_period']}"
            send_email(sender_email, receiver_emails, cc_email, subject, email_message)
        
    except Exception as e:
        print(str(e))

elif client_type == '4':
    print("Bye!")
                
else:
    print("Invalid option. Please choose a valid option.")

