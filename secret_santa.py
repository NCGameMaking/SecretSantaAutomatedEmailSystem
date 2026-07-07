import os
import random
import smtplib
import ssl
from dotenv import load_dotenv


load_dotenv()

def send_email(sender, reciever, recipient):
    password = os.getenv('password')

    body_msg = f'''\
From: {sender}
To:{reciever}
Subject: Your Secret Santa Assignment

Hello! Your secret santa is: {recipient}!
Remember to spend $10-$20 on your gift, but don't stress about it being the perfect gift!
'''
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, reciever, body_msg.encode('utf-8'))

names_list = ['Subject A', 'Subject B', 'Subject C', 'Subject D']
participants = [
  ['Subject A', 'subjectA@gmail.com'],
  ['Subject B', 'subjectB@gmail.com'],
  ['Subject C', 'subjectC@gmail.com'],
  ['Subject D', 'subjectD@eq.edu.au']
  ]

if len(names_list) <= 1:
    print('not enough people to start secret santa!')
    quit()

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

sender_email = 'neil726345@gmail.com'

for i in range(len(participants)):
    giver_name = participants[i][0]
    giver_email = participants[i][1]
    reciever_name = targets[i][0]

    print(f"Sending email to {giver_name}...")
    send_email(sender_email, giver_email, reciever_name)
print("All secret santas emails sent successfully")