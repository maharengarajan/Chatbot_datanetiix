import mysql.connector as conn
import datetime
import sys
from config import DATABASE_CONFIG, DATABASE_CONNECTION_CONFIG


def create_database():
    # Connection from Python to MySQL
    mydb = conn.connect(**DATABASE_CONNECTION_CONFIG)

    # Creating a pointer to the MySQL database
    cursor = mydb.cursor()

    # Create database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS Chatbot_Datanetiix")

    # Create tables and columns if they don't exist
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Chatbot_Datanetiix.new_client(ID INT AUTO_INCREMENT PRIMARY KEY, DATE DATE, TIME TIME, IP_ADDRESS VARCHAR(45), NAME VARCHAR(255), EMAIL_ID VARCHAR(255), CONTACT_NUMBER VARCHAR(255), COMPANY_NAME VARCHAR(500), INDUSTRY VARCHAR(255), VERTICAL VARCHAR(255), REQUIREMENTS VARCHAR(255), KNOWN_SOURCE VARCHAR(255))"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Chatbot_Datanetiix.existing_client(ID INT AUTO_INCREMENT PRIMARY KEY, DATE DATE, TIME TIME, IP_ADDRESS VARCHAR(45), NAME VARCHAR(255), EMAIL_ID VARCHAR(255), CONTACT_NUMBER VARCHAR(255), COMPANY_NAME VARCHAR(500), VERTICAL VARCHAR(255), ISSUE_ESCALATION VARCHAR(255), ISSUE_TYPE VARCHAR(255))"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Chatbot_Datanetiix.job_seeker(ID INT AUTO_INCREMENT PRIMARY KEY, DATE DATE, TIME TIME, IP_ADDRESS VARCHAR(45), NAME VARCHAR(255), EMAIL_ID VARCHAR(255), CONTACT_NUMBER VARCHAR(255), CATEGORY VARCHAR(255), VERTICAL VARCHAR(255), INTERVIEW_AVAILABLE VARCHAR(255), TIME_AVAILABLE VARCHAR(255), NOTICE_PERIOD VARCHAR(255))"
    )

    # Get current date and time
    current_date = datetime.datetime.now().date()
    current_time = datetime.datetime.now().time()

    cursor.close()
    mydb.close()


def insert_new_client(
    ip_address,
    name,
    email,
    contact,
    company,
    industry_options,
    vertical_options,
    requirement_option,
    known_source,
):
    # Connection from Python to MySQL
    mydb = conn.connect(**DATABASE_CONFIG)

    # Creating a pointer to the MySQL database
    cursor = mydb.cursor()

    # Get current date and time
    current_date = datetime.datetime.now().date()
    current_time = datetime.datetime.now().time()

    # Convert lists to strings
    industry_str = ",".join(industry_options)
    vertical_str = ",".join(vertical_options)

    # Prepare the SQL query to insert data into the table
    query = "INSERT INTO new_client (DATE, TIME, IP_ADDRESS, NAME, EMAIL_ID, CONTACT_NUMBER, COMPANY_NAME, INDUSTRY, VERTICAL, REQUIREMENTS, KNOWN_SOURCE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (
        current_date,
        current_time,
        ip_address,
        name,
        email,
        contact,
        company,
        industry_str,
        vertical_str,
        requirement_option,
        known_source,
    )

    # Execute the query
    cursor.execute(query, values)

    # Commit the changes to the database
    mydb.commit()

    # Close the cursor and connection
    cursor.close()
    mydb.close()


def insert_existing_client(
    ip_address,
    name,
    email,
    contact,
    company, 
    vertical_options, 
    issue_escalation, 
    issue_type
):
    # Connection from Python to MySQL
    mydb = conn.connect(**DATABASE_CONFIG)

    # Creating a pointer to the MySQL database
    cursor = mydb.cursor()

    # Get current date and time
    current_date = datetime.datetime.now().date()
    current_time = datetime.datetime.now().time()

    # Convert lists to strings
    vertical_str = ",".join(vertical_options)

    # Prepare the SQL query to insert data into the table
    query = "INSERT INTO existing_client(DATE, TIME, IP_ADDRESS, NAME, EMAIL_ID, CONTACT_NUMBER, COMPANY_NAME, VERTICAL, ISSUE_ESCALATION, ISSUE_TYPE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (
        current_date,
        current_time,
        ip_address,
        name,
        email,
        contact,
        company,
        vertical_str,
        issue_escalation,
        issue_type,
    )

    # Execute the query
    cursor.execute(query, values)

    # Commit the changes to the database
    mydb.commit()

    # Close the cursor and connection
    cursor.close()
    mydb.close()


def insert_job_seeker(
    ip_address,
    name,
    email,
    contact,
    user_category,
    vertical_options,
    is_available,
    interview_date,
    joining_date,
):
    # Connection from Python to MySQL
    mydb = conn.connect(**DATABASE_CONFIG)

    # Creating a pointer to the MySQL database
    cursor = mydb.cursor()

    # Get current date and time
    current_date = datetime.datetime.now().date()
    current_time = datetime.datetime.now().time()

    # Convert lists to strings
    vertical_str = ",".join(vertical_options)

    # Prepare the SQL query to insert data into the table
    query = "INSERT INTO job_seeker(DATE, TIME, IP_ADDRESS, NAME, EMAIL_ID, CONTACT_NUMBER, CATEGORY, VERTICAL, INTERVIEW_AVAILABLE, TIME_AVAILABLE, NOTICE_PERIOD) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (
        current_date,
        current_time,
        ip_address,
        name,
        email,
        contact,
        user_category,
        vertical_str,
        is_available,
        interview_date,
        joining_date,
    )

    # Execute the query
    cursor.execute(query, values)

    # Commit the changes to the database
    mydb.commit()

    # Close the cursor and connection
    cursor.close()
    mydb.close()


def extract_new_client_details():
    # Connection from Python to MySQL
    mydb = conn.connect(**DATABASE_CONFIG)

    # Creating a pointer to the MySQL database
    cursor = mydb.cursor()

    # execute sql query to retrive new_client details
    query = "SELECT * FROM new_client ORDER BY id DESC LIMIT 1"  # we can get the row with highest id value
    cursor.execute(query)

    # Fetch the result
    result = cursor.fetchone()  # getting only one row

    if result:
        # Extract the columns from the result
        (
            id,
            date,
            time,
            name,
            email,
            contact,
            company,
            ip_address,
            selected_industry,
            selected_vertical,
            requirement,
            known_source,
        ) = result

        # Extracted new_client details stored in dictionary format
        new_client_details = {
            "id": id,
            "date": date,
            "time": time,
            "name": name,
            "email": email,
            "contact": contact,
            "company": company,
            "ip_address":ip_address,
            "industries_choosen": selected_industry,
            "verticals_choosen": selected_vertical,
            "requirement": requirement,
            "known_source": known_source,
        }

        return new_client_details
    else:
        print("No new client details found.")
        return None

    # Close the cursor and connection
    cursor.close()
    mydb.close()


def extract_existing_client_details():
    # connection to mysql database
    mydb = conn.connect(**DATABASE_CONFIG)

    # create cursor object to execute SQL queries
    cursor = mydb.cursor()

    # execute sql query to retrive new_client details
    query = "SELECT * FROM existing_client ORDER BY id DESC LIMIT 1"  # we can get the row with highest id value
    cursor.execute(query)

    # Fetch the result
    result = cursor.fetchone()  # getting only one row

    if result:
        # Extract the columns from the result
        (
            id,
            date,
            time,
            name,
            email,
            contact,
            company,
            ip_address,
            selected_vertical,
            issue_escalation,
            issue_type,
        ) = result

        # Extracted new_client details stored in dictionary format
        existing_client_details = {
            "id": id,
            "date": date,
            "time": time,
            "name": name,
            "email": email,
            "contact": contact,
            "company": company,
            "ip_address":ip_address,
            "verticals_choosen": selected_vertical,
            "issue_escalation": issue_escalation,
            "issue_type": issue_type,
        }

        return existing_client_details
    else:
        print("No existing client details found.")
        return None

    # Close the cursor and connection
    cursor.close()
    mydb.close()


def extract_job_seeker_details():
    # connection to mysql database
    mydb = conn.connect(**DATABASE_CONFIG)

    # create cursor object to execute SQL queries
    cursor = mydb.cursor()

    # execute sql query to retrive new_client details
    query = "SELECT * FROM job_seeker ORDER BY id DESC LIMIT 1"  # we can get the row with highest id value
    cursor.execute(query)

    # Fetch the result
    result = cursor.fetchone()  # getting only one row

    if result:
        # Extract the columns from the result
        (
            id,
            date,
            time,
            name,
            email,
            contact,
            ip_address,
            category,
            selected_vertical,
            interview_available,
            time_available,
            notice_period,
        ) = result

        # Extracted job_seeker details stored in dictionary format
        job_seeker_details = {
            "id": id,
            "date": date,
            "time": time,
            "name": name,
            "email": email,
            "contact": contact,
            "ip_address":ip_address,
            "category": category,
            "verticals_choosen": selected_vertical,
            "interview_available": interview_available,
            "time_available": time_available,
            "notice_period": notice_period,
        }

        return job_seeker_details
    else:
        print("No job seeker details found.")
        return None

    # Close the cursor and connection
    cursor.close()
    mydb.close()
