import re

def get_valid_name():
    name = input("Please enter your name: ")
    while not re.match(r"^[A-Za-z\s]+$", name):
        print("Please enter a valid name")
        name = input("Please enter your name: ")
    return name

def get_valid_email():
    email = input("Please enter your email address: ")
    while not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Please enter a valid email address")
        email = input("Please enter your email address: ")
    return email

def get_valid_contact():
    contact = input("Please enter your contact number: ")
    while not contact.isdigit():
        print("Please enter a valid contact number")
        contact = input("Please enter your contact number: ")
    return contact

def get_user_details():
    name = get_valid_name()
    email = get_valid_email()
    contact = get_valid_contact()
    return name, email, contact

def choose_industry_options():
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
        print("Please choose an industry option:")
        for option, industry in industries.items():
            print(f"{option}. {industry}")
        option = input("Enter your option(s) separated by commas: ")
        options = [opt.strip() for opt in option.split(',') if opt.strip() in valid_options]
        if options:
            return [industries[opt] for opt in options]
        else:
            print("Please choose valid option(s)")

def choose_vertical_option():
    verticals = ['ML/DS/AI', 'Sales force', 'Microsoft dynamics', 'Custom app', 'Others']
    print("Please choose a vertical option:")
    for i, vertical in enumerate(verticals, start=1):
        print(f"{i}. {vertical}")

    while True:
        option = input("Enter your option(s) separated by commas: ")
        options = option.split(',')
        selected_verticals = []
        invalid_options = []

        for opt in options:
            if opt.strip() not in ['1', '2', '3', '4', '5']:
                invalid_options.append(opt)
            else:
                selected_verticals.append(verticals[int(opt.strip()) - 1])

        if len(invalid_options) == 0:
            break
        else:
            print("Invalid option(s):", ", ".join(invalid_options))

    print("Thank you for choosing your vertical option(s).")
    print("Selected vertical(s):", ", ".join(selected_verticals))

def choose_requirements():
    requirements = ["Start the project from scratch", "Require support from existing project", "Looking for some kind of solutions", "Others"]
    print("Please choose your requirements:")
    for i, requirement in enumerate(requirements, start=1):
        print(f"{i}. {requirement}")

    while True:
        option = input("Enter your option(s) separated by commas: ")
        options = option.split(',')
        selected_requirements = []
        invalid_options = []

        for opt in options:
            if opt.strip() not in ['1', '2', '3', '4']:
                invalid_options.append(opt)
            else:
                selected_requirements.append(requirements[int(opt.strip()) - 1])

        if len(invalid_options) == 0:
            break
        else:
            print("Invalid option(s):", ", ".join(invalid_options))

    print("Thank you for choosing your requirement(s).")
    print("Selected requirement(s):", ", ".join(selected_requirements))

def choose_known_source():
    known_sources = [
        "Google",
        "LinkedIn",
        "Email Campaign",
        "Known resources",
        "Others"
    ]

    print("How did you hear about us?")
    for i, source in enumerate(known_sources, start=1):
        print(f"{i}. {source}")

    while True:
        option = input("Choose an option (1-5): ")
        if option.isdigit() and 1 <= int(option) <= 5:
            option = int(option)
            if option == 4:
                specification = input("Please specify: ")
                known_source_str = f"{known_sources[option - 1]}: {specification}"
            elif option == 5:
                specification = input("Please specify: ")
                known_source_str = f"{known_sources[option - 1]}: {specification}"
            else:
                known_source_str = known_sources[option - 1]
            return known_source_str
        else:
            print("Invalid option. Please choose a valid option.")
            
            
def issue_escalation_options():
    issue_escalation = {
        '1': 'Team Lead',
        '2': 'Sales Person',
        '3': 'Escalate Issue'
    }
    valid_options = issue_escalation.keys()
    while True:
        print("Who would you like to speak to?")
        for option, person in issue_escalation.items():
            print(f"{option}. {person}")
        option = input("Your choice: ")
        options = [opt.strip() for opt in option.split(',') if opt.strip() in valid_options]
        if options:
            return [issue_escalation[opt] for opt in options]
        else:
            print("Please choose valid option(s)")
            
def issue_type():
    while True:
        print("Is your issue normal or urgent?")
        issue_type_options = ['1. normal', '2. urgent']
        response = input("Enter '1' for normal or '2' for urgent: ")
        if response == "1":
            print("Thank you. We have saved your issue and will contact you as soon as possible.")
            break  # Exit the loop when a valid option is chosen
        elif response == "2":
            print("Thank you. We have saved your issue as urgent and will contact you immediately.")
            break  # Exit the loop when a valid option is chosen
        else:
            print("Sorry, I didn't understand your response. Please try again.")

client_type = input("Can you please let me know if you are a? (Enter 1 for new client, 2 for existing client, 3 for job seeker): ")

if client_type == '1':
    print("Welcome, New client!")
    try:
        name, email, contact = get_user_details()
        print('Thanks for your details')
        industry_options = choose_industry_options()
        choose_vertical_option()
        choose_requirements()
        known_source = choose_known_source()
    except Exception as e:
        print(str(e))

elif client_type == '2':
    print("Welcome, existing client!")
    try:
        name, email, contact = get_user_details()
        print('Thanks for updating your details')
        choose_vertical_option()
        selected_issue_escalation = issue_escalation_options()
        print("Thank you for choosing option(s).")
        print("Selected option(s):", ", ".join(selected_issue_escalation))
        issue_type()
    except Exception as e:
        print(str(e))

elif client_type == '3':
    print("Welcome, Job seeker!")
    try:
        name, email, contact = get_user_details()
        print('Thanks for providing your details')
    except Exception as e:
        print(str(e))

else:
    print("Invalid option. Please choose a valid option.")
