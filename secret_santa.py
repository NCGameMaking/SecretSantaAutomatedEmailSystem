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
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            .email-wrapper {{
                background-color: #f4f7f6;
                padding: 30px 15px;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            }}
            .card {{
                max-width: 500px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 10px rgba(0,0,0,0.08);
                border: 1px solid #eaeaea;
            }}
            .header {{
                background-color: #d9534f;
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                color: #ffffff;
                margin: 0;
                font-size: 24px;
                letter-spacing: 1px;
            }}
            .content {{
                padding: 30px;
                color: #333333;
                line-height: 1.6;
                text-align: center
            }}
            .assignment-box {{
                background-color: #fcf8e3;
                border: 1px dashed #fbeed5;
                border-radius: 8px;
                padding: 20px;
                text-align: center;
                margin: 20px 0;
            }}
            .target-name {{
                font-size: 22px;
                font-weight: bold;
                color: #d9534f;
                margin: 5px 0 0 0;
            }}
            .details-list {{
                margin-top: 20px;
                padding-left: 0;
                list-style: none;
                border-top: 1px solid #eee;
                padding-top: 15px;
            }}
            .details-list li {{
                margin-bottom: 8px;
                font-size: 14px;
                color: #666666;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                font-size: 12px;
                color: #999999;
                background-color: #fafafa;
                border-top: 1px solid #eeeeee;
            }}
        </style>
    </head>
    <body>
        <div class="email-wrapper">
            <div class="card">
                <div class="header">
                    <h1>Secret Santa Assignment 🎅</h1>
                </div>
                <div class="content">
                    <p>Hello! The generator has completed the matchmaking draw, and your secret target assignment is ready below:</p>
                    
                    <div class="assignment-box">
                        <span style="font-size: 14px; text-transform: uppercase; color: #8a6d3b; font-weight: bold; letter-spacing: 0.5px;"> 🎁 You are buying a gift for:</span>
                        <p class="target-name"> {recipient}</p>
                    </div>
                    
                    <p>Please make sure to keep this a complete secret until the party exchange so the surprise isn't ruined! 🤫</p>
                    
                    <ul class="details-list">
                        <li><strong>💰 Spending Limit:</strong> ${budget} Maximum</li>
                        <li><strong>📅 Event Date:</strong> {party_date}</li>
                    </ul>
                </div>
                <div class="footer">
                    Automated Holiday Delivery System - Please do not reply to this email.
                </div>
            </div>
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
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Success!</title>
        <style>
            body {font-family: "Segoe UI", sans-serif; background: #eef5fb; margin: 0; padding: 32px; color: #1e293b; display: flex; justify-content: center; align-items: center; min-height: 100vh;}
            .card { background: white; width: min(100%, 520px); border-radius: 24px; padding: 36px 32px; box-shadow: 0 24px 60px rgba(15, 23, 42, 0.08); text-align: center; }
            h1 { color: #2e7d32; margin: 0 0 18px; font-size: clamp(2rem, 2.5vw, 2.6rem); }
            p { color: #475569; font-size: 1.05rem; line-height: 1.75; margin: 0; }
            .back-btn { display: inline-flex; margin-top: 28px; padding: 14px 22px; background: #d9534f; color: white; text-decoration: none; border-radius: 999px; font-weight: 700; }
            .back-btn:hover { opacity: 0.94; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Pairings Sent!</h1>
            <p>All Secret Santa matches were generated and emailed privately to each participant.</p>
            <a class="back-btn" href="/">Back to the form</a>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)