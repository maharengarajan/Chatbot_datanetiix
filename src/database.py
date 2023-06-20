import mysql.connector as conn

def create_database():
    # Connection from Python to MySQL
    mydb = conn.connect(host='localhost', user='root', password='M18ara10@')

    # Creating a pointer to the MySQL database
    cursor = mydb.cursor()

    # Create database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS chatbot_yoga")

    # Create tables and columns if they don't exist
    cursor.execute('CREATE TABLE IF NOT EXISTS chatbot_yoga.New_Client(ID INT AUTO_INCREMENT PRIMARY KEY, NAME VARCHAR(255), EMAIL_ID VARCHAR(255), CONTACT_NUMBER BIGINT(255), INDUSTRY VARCHAR(255), VERTICAL VARCHAR(255), REQUIREMENTS VARCHAR(255), KNOWN_SOURCE VARCHAR(255))')
    cursor.execute('CREATE TABLE IF NOT EXISTS chatbot_yoga.Existing_Client(ID INT AUTO_INCREMENT PRIMARY KEY, NAME VARCHAR(255), EMAIL_ID VARCHAR(255), CONTACT_NUMBER BIGINT(255), VERTICAL VARCHAR(255), ISSUE_ESCALATION VARCHAR(255), ISSUE_TYPE VARCHAR(255))')
    cursor.execute('CREATE TABLE IF NOT EXISTS chatbot_yoga.Job_Seeker(ID INT AUTO_INCREMENT PRIMARY KEY, NAME VARCHAR(255), EMAIL_ID VARCHAR(255), CONTACT_NUMBER BIGINT(255), CATEGORY VARCHAR(255), VERTICAL VARCHAR(255), INTERVIEW_AVAILABLE VARCHAR(255), TIME_AVAILABLE VARCHAR(255), NOTICE_PERIOD VARCHAR(255))')

    cursor.close()
    mydb.close()

def insert_new_client(name, email, contact, industry_options, vertical_options, requirement_options, known_source):
    # Connect to the MySQL database
    connection = conn.connect(host='localhost', user='root', password='M18ara10@', database='chatbot_yoga')

    # Create a cursor to execute SQL queries
    cursor = connection.cursor()

    # Define the SQL query to insert the user details
    details = "INSERT INTO chatbot_yoga.New_Client(NAME, EMAIL_ID, CONTACT_NUMBER, INDUSTRY, VERTICAL, REQUIREMENTS, KNOWN_SOURCE) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    
    # Convert lists to strings
    industry_str = ','.join(industry_options)
    vertical_str = ','.join(vertical_options)
    requirements_str = ','.join(requirement_options)
    
    # Execute the query with the user details
    cursor.execute(details, (name, email, contact, industry_str, vertical_str, requirements_str, known_source))

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()

def insert_existing_client(name, email, contact, vertical_options, issue_escalation, issue_type):
    # Connect to the MySQL database
    connection = conn.connect(host='localhost', user='root', password='M18ara10@', database='chatbot_yoga')

    # Create a cursor to execute SQL queries
    cursor = connection.cursor()

    # Define the SQL query to insert the user details
    details = "INSERT INTO chatbot_yoga.Existing_Client(NAME, EMAIL_ID, CONTACT_NUMBER, VERTICAL, ISSUE_ESCALATION, ISSUE_TYPE) VALUES (%s, %s, %s, %s, %s, %s)"
    
    # Convert lists to strings
    vertical_str = ','.join(vertical_options)
    issue_escalation_str = ','.join(issue_escalation)
    issue_type_str = '.'.join(issue_option)
    
    # Execute the query with the user details
    cursor.execute(details, (name, email, contact, vertical_str, issue_escalation_str, issue_type_str))

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()

def insert_job_seeker(name, email, contact,user_category, vertical_options, interview_avail, time_avail, joining_date):
    # Connect to the MySQL database
    connection = conn.connect(host='localhost', user='root', password='M18ara10@', database='chatbot_yoga')

    # Create a cursor to execute SQL queries
    cursor = connection.cursor()

    # Define the SQL query to insert the user details
    details = "INSERT INTO chatbot_yoga.Job_Seeker(NAME, EMAIL_ID, CONTACT_NUMBER, CATEGORY, VERTICAL, INTERVIEW_AVAILABLE, TIME_AVAILABLE, NOTICE_PERIOD) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    
    # Convert lists to strings
    vertical_str = ','.join(vertical_options)
    #availability_check_str = ','.join()
    
    # Execute the query with the user details
    cursor.execute(details, (name, email, contact,user_category, vertical_str, interview_avail, time_avail, joining_date))

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()
