import mysql.connector as conn
import datetime
import sys

def create_database():
    # Connection from Python to MySQL
    mydb = conn.connect(host='localhost', user='root', password='M18ara10@')

    # Creating a pointer to the MySQL database
    cursor = mydb.cursor()

    # Create database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS chatbot_priya")

    # Create tables and columns if they don't exist
    cursor.execute('CREATE TABLE IF NOT EXISTS chatbot_priya.New_Client(ID INT AUTO_INCREMENT PRIMARY KEY, DATE DATE, TIME TIME, NAME VARCHAR(255), EMAIL_ID VARCHAR(255), CONTACT_NUMBER VARCHAR(255), INDUSTRY VARCHAR(255), VERTICAL VARCHAR(255), REQUIREMENTS VARCHAR(255), KNOWN_SOURCE VARCHAR(255))')
    cursor.execute('CREATE TABLE IF NOT EXISTS chatbot_priya.Existing_Client(ID INT AUTO_INCREMENT PRIMARY KEY, DATE DATE, TIME TIME, NAME VARCHAR(255), EMAIL_ID VARCHAR(255), CONTACT_NUMBER VARCHAR(255), VERTICAL VARCHAR(255), ISSUE_ESCALATION VARCHAR(255), ISSUE_TYPE VARCHAR(255))')
    cursor.execute('CREATE TABLE IF NOT EXISTS chatbot_priya.Job_Seeker(ID INT AUTO_INCREMENT PRIMARY KEY, DATE DATE, TIME TIME, NAME VARCHAR(255), EMAIL_ID VARCHAR(255), CONTACT_NUMBER VARCHAR(255), CATEGORY VARCHAR(255), VERTICAL VARCHAR(255), INTERVIEW_AVAILABLE VARCHAR(255), TIME_AVAILABLE VARCHAR(255), NOTICE_PERIOD VARCHAR(255))')
    
    # Get current date and time
    current_date = datetime.datetime.now().date()
    current_time = datetime.datetime.now().time()
    
    cursor.close()
    mydb.close()
    
def insert_new_client(name, email, contact, industry_options, vertical_options, requirement_option, known_source):
    mydb = conn.connect(host='localhost', user='root', password='M18ara10@', database='chatbot_priya')
    cursor = mydb.cursor()

    # Get current date and time
    current_date = datetime.datetime.now().date()
    current_time = datetime.datetime.now().time()
    
     # Convert lists to strings
    industry_str = ','.join(industry_options)
    vertical_str = ','.join(vertical_options)

    # Prepare the SQL query to insert data into the table
    query = "INSERT INTO New_Client (DATE, TIME, NAME, EMAIL_ID, CONTACT_NUMBER, INDUSTRY, VERTICAL, REQUIREMENTS, KNOWN_SOURCE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (current_date, current_time, name, email, contact, industry_str, vertical_str, requirement_option, known_source)

    
    # Execute the query
    cursor.execute(query, values)
    
    # Commit the changes to the database
    mydb.commit()
    
    # Close the cursor and connection
    cursor.close()
    mydb.close() 
    
def insert_existing_client(name, email, contact, vertical_options, issue_escalation, issue_type):
    mydb = conn.connect(host='localhost', user='root', password='M18ara10@', database='chatbot_priya')
    cursor = mydb.cursor()
    
    # Get current date and time
    current_date = datetime.datetime.now().date()
    current_time = datetime.datetime.now().time()
    
    # Convert lists to strings
    vertical_str = ','.join(vertical_options)
    
    # Prepare the SQL query to insert data into the table
    query = "INSERT INTO Existing_Client(DATE, TIME, NAME, EMAIL_ID, CONTACT_NUMBER, VERTICAL, ISSUE_ESCALATION, ISSUE_TYPE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (current_date, current_time, name, email, contact, vertical_str, issue_escalation, issue_type)
    
    # Execute the query
    cursor.execute(query, values)
    
    # Commit the changes to the database
    mydb.commit()
    
    # Close the cursor and connection
    cursor.close()
    mydb.close()
    
def insert_job_seeker(name, email, contact, user_category, vertical_options, is_available, interview_date, joining_date):
    mydb = conn.connect(host='localhost', user='root', password='M18ara10@', database='chatbot_priya')
    cursor = mydb.cursor()
    
    # Get current date and time
    current_date = datetime.datetime.now().date()
    current_time = datetime.datetime.now().time()
    
    # Convert lists to strings
    vertical_str = ','.join(vertical_options)
    
    # Prepare the SQL query to insert data into the table
    query = "INSERT INTO job_seeker(DATE, TIME, NAME, EMAIL_ID, CONTACT_NUMBER, CATEGORY, VERTICAL, INTERVIEW_AVAILABLE, TIME_AVAILABLE, NOTICE_PERIOD) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (current_date, current_time, name, email, contact, user_category, vertical_str, is_available, interview_date, joining_date)
    
    # Execute the query
    cursor.execute(query, values)
    
    # Commit the changes to the database
    mydb.commit()
    
    # Close the cursor and connection
    cursor.close()
    mydb.close()

def extract_new_client_details():
    #connection to mysql database
    mydb = conn.connect(host='localhost', user='root', password='M18ara10@', database='chatbot_priya')
    
    #create cursor object to execute SQL queries
    cursor = mydb.cursor()
    
    #execute sql query to retrive new_client details
    query = "SELECT * FROM New_client ORDER BY id DESC LIMIT 1" #we can get the row with highest id value 
    cursor.execute(query)
    
    # Fetch the result
    result = cursor.fetchone() #getting only one row
    
    if result:
        # Extract the columns from the result
        id, date, time, name, email, contact, selected_industry, selected_vertical, requirement, known_source = result 
        
        # Extracted new_client details stored in dictionary format
        new_client_details = {
            'id': id,
            'date': date,
            'time': time,
            'name': name,
            'email': email,
            'contact': contact,
            'industries_choosen': selected_industry,
            'verticals_choosen': selected_vertical,
            'requirement': requirement,
            'known_source': known_source
        }
        
        return new_client_details
    else:
        print("No new client details found.")
        return None 
    
    # Close the cursor and connection
    cursor.close()
    mydb.close()
    