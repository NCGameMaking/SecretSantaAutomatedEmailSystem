from dotenv import load_dotenv
import os
import random
import smtplib
import ssl

load_dotenv()

def send_email(sender, reciever, recipient):
    password = os.environ['password']
    body_msg = f'''\
From: {sender}
Subject: Your Secret Santa Present

Hello! Your secret santa is: {recipient}!
Remember to spend $10-$20 on your gift, but don't stress about it being the perfect gift!
'''
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, reciever, body_msg)

names_list = ['Mum', 'alt neil', 'main neil']
names_and_emails = [
  ['mum', 'ddc2010@gmail.com'],
  ['2020Neilrishi', '2020neilrishi@gmail.com'],
  ['Neil', 'neil726345@gmail.com']
  ]

if len(names_list) <= 1:
    print('not enough people to start secret santa!')
    quit()

first_name = names_and_emails[0][0]

while len(names_list) >=2:
    send_email('<neil726345@gmail.com>', names_and_emails[0][1], names_and_emails[1][0])
    names_and_emails.pop(0)
    random.shuffle(names_and_emails)
send_email('neil726345@gmail.com', names_and_emails[0][1], first_name)