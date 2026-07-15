import os
import random
import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template, request
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")


def send_email(reciever, recipient, budget, party_date):
    html_body = f"""
<html>
<body style="font-family: 'Courier New', Courier, monospace; background-color: #f0f0f0; padding: 20px; color: #000000;">
    <div style="background-color: #ffffff; border: 3px solid #000000; padding: 20px; max-width: 500px; margin: 0 auto;">
        
        <h1 style="text-align: center; color: #ff0000; text-decoration: underline; margin-bottom: 5px;">
            !!! SECRET SANTA ASSIGNMENT !!!
        </h1>
        <p style="text-align: center; font-style: italic; margin-top: 0;">
            (Keep this a secret or the surprise is ruined!)
        </p>
        
        <hr style="border: 1px solid #000000;">
        
        <p style="font-size: 18px; text-align: center; margin: 25px 0;">
            YOU ARE BUYING A GIFT FOR:
            <br><br>
            <span style="font-size: 24px; background-color: #ffff00; padding: 5px; border: 1px dashed black;">
                <b><u>{recipient}</u></b>
            </span>
        </p>
        
        <hr style="border: 1px solid #000000;">
        
        <h3 style="margin-bottom: 5px;">Event Details:</h3>
        <table border="1" cellpadding="8" style="border-collapse: collapse; width: 100%; background-color: #fafafa;">
            <tr>
                <td><b>Spending Limit</b></td>
                <td>${budget} Maximum</td>
            </tr>
            <tr>
                <td><b>Party Date</b></td>
                <td>{party_date}</td>
            </tr>
        </table>
    
    </div>
</body>
</html>
    """
    

    msg = MIMEText(html_body, 'html')
    msg['Subject'] = 'Your Secret Santa Assignment 🎅'
    msg['From'] = SENDER_EMAIL
    msg['To'] = reciever

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, reciever, msg.as_string())

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start-santa', methods=['GET', 'POST'])
def start_santa():

    if request.method == 'GET':
        return "Please submit the form from the home page!", 400

    budget = request.form.get('budget', '20')
    party_date = request.form.get('party_date', 'TBD')

    form_names = request.form.getlist('names[]')
    form_emails = request.form.getlist('emails[]')

    participants = [[form_names[i], form_emails[i]] for i in range(len(form_names))]

    if len(participants) <= 1:
      return "Not enough people to start Secret Santa!", 400

    targets = participants.copy()

    while True:
        random.shuffle(targets)
        matched_self = False
        for i in range(len(participants)):
            if participants[i][0] == targets[i][0]:
                matched_self = True
                break
        if not matched_self:
            break

    for i in range(len(participants)):
        giver_email = participants[i][1]
        reciever_name = targets[i][0]
        send_email(giver_email, reciever_name, budget, party_date)

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Secret Santa</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f6f9; color: #333333; padding: 50px; text-align: center;">
        <div style="background-color: #ffffff; border: 2px solid #333333; border-radius: 8px; padding: 40px; max-width: 500px; margin: 0 auto;">
            <h1 style="color: #2e7d32; margin-top: 0;">Success!</h1>
            <p style="font-size: 16px; line-height: 1.5; margin-bottom: 30px;">
                All of your Secret Santa pairings have been successfully generated and sent to the participants' email addresses.
            </p>

            <a href="/" style="display: inline-block; background-color: #333333; color: #ffffff; padding: 10px 20px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 14px;">
                Back to Form
            </a>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)