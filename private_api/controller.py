import smtplib

gmail_user = 'alvaradolayonardo@gmail.com'
gmail_password = 'mqjjqbpmctkleorb'

sent_from = gmail_user
to = ['calvaradot1@est.ups.edu.ec']
body = """
si vale vrg
"""

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, body)
    server.close()
    print('Email sent!')
except Exception as e:
    print(e)
    pass
