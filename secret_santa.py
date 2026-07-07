import os
import random
import resend
import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template, request
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

resend.api_key = os.getenv("RESEND_API_KEY")

def send_email(reciever, recipient):
    
    params = {
        "from": "Secret Santa <onboarding@resend.dev>",  
        "to": [reciever],
        "subject": "Your Secret Santa Assignment",
        "html": f"""
        <h3>Hello! Your Secret Santa assignment is here!</h3>
        <p>Your target assignment is: <strong>{recipient}</strong>!</p>
        <p>Remember to spend $10-$20 on your gift, but don't stress about it being perfect!</p>
        """
    }
    
    resend.Emails.send(params)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start-santa', methods=['GET', 'POST'])
def start_santa():

    if request.method == 'GET':
        return "Please submit the form from the home page!", 400

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
        send_email(giver_email, reciever_name)
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Success!</title>
        <style>
            body {font-family: Arial, sans-serif; background-color: f4f7f6; padding 40px; text-align: center;}
            .card { background:white; max-width: 500px; margin: 0 auto; padding: 40px; border-radius: 10px; box-shadow:0 4px 15px rgba(0,0,0,0.1);}
            h1 {color: #5cb85c; margin_bottom: 20px;}
            p {color:#555; font-size: 1.1em; line-height:1.6;}
            .back-btn { display: inline-block; margin-top:25px; padding: 10px 20px; background-color: #d9534f; color:white; text-decoration:none; font-weight: bold; border_radius: 5px;}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Success!</h1>
            <p>All Secret Santa pairings have been assorted and have been sent to participants's email safely.</p>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)