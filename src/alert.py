import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, receiver_email, subject, message):
    # Create a multipart message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Add the message body
    msg.attach(MIMEText(message, 'plain'))

    # SMTP server settings
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'photola.datanetiix@gmail.com'
    smtp_password = 'uloxazedvwjjkafl'

    try:
        # Create a secure connection with the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())

        print('Email sent successfully!')
    except Exception as e:
        print('An error occurred while sending the email:', str(e))
    finally:
        # Close the SMTP connection
        server.quit()

# Example usage
sender_email = 'photola.datanetiix@gmail.com'
receiver_email = 'rengarajan@datanetiix.com'
subject = 'chatbot project'
message = 'This is a test email sent from Rengarajan.'
