import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_server_settings

def send_email(sender_email, receiver_emails, cc_email , subject, message):
    # Create a multipart message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_emails)
    msg['Cc'] = cc_email
    msg['Subject'] = subject

    # Add the message body
    msg.attach(MIMEText(message, 'plain'))

    # Access the SMTP settings
    smtp_server = SMTP_server_settings['smtp_server']
    smtp_port = SMTP_server_settings['smtp_port']
    smtp_username = SMTP_server_settings['smtp_username']
    smtp_password = SMTP_server_settings['smtp_password']

    try:
        # Create a secure connection with the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Send the email
        all_recipients = receiver_emails + [cc_email]
        server.sendmail(sender_email, all_recipients, msg.as_string())

        print('Email sent successfully!')
    except Exception as e:
        print('An error occurred while sending the email:', str(e))
    finally:
        # Close the SMTP connection
        server.quit()

# Example usage
#sender_email = 'photola.datanetiix@gmail.com'
#receiver_email = 'rengarajan@datanetiix.com'
#subject = 'chatbot project'
#message = 'This is a test email sent from Rengarajan.'
