from flask import Flask, redirect, render_template, request
from dotenv import load_dotenv
import os
from flask_cors import CORS
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

load_dotenv()
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")

app = Flask(__name__, static_url_path='/static')
CORS(app)

app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    global smtp_username, smtp_password
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        smtp_server = 'smtp.ionos.co.uk'
        smtp_port = 587

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = 'koziol95@yahoo.com'
        msg['Subject'] = f'Wiadomość od {name}'

        email_content = f"""
        Wiadomość od: {name}
        Email: {email}
        Wiadomość: {message}
        """

        msg.attach(MIMEText(email_content, 'plain'))

        try:
            server.sendmail(smtp_username, 'koziol95@yahoo.com', msg.as_string())
            server.quit()
            return render_template('mail_send.html')
        except smtplib.SMTPException as e:
            print(f"Error occurred while sending email: {e}")
            return 'An error occurred while sending the email. Please try again later..'

    else:
        return 'Błąd: Nieprawidłowe żądanie'

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run()
