import smtplib


gmail_user = 'alvaradolayonardo@gmail.com'
gmail_password = 'patito.Local1999'

sent_from = gmail_user
to = ['torresleonardo@gmail.com']
subject = 'mensaje de testeo perro'
body = 'Hey hey hey :v'

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, body)
    server.close()
    print('Email sent!')
except:
    pass
