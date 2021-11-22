# Libraries for API definition
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Class for Mysql database connection.
import mysql_utility
import smtplib

# FastAPI instantiation.
app = FastAPI()
db_connection = mysql_utility.DBConnector()


# CORS definition.
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def listToStringWithoutBrackets(list1):
    return str(list1).replace('(', '').replace(')', '').replace(',', '').replace('[', '').replace(']', '').replace('{',
                                                                                                                   '').replace(
        '}', '')


@app.post('/api/private/send_mail')
async def send_mail(cedula: str, motivo: str, monto: float):
    print('cedula:', cedula, ' <---')
    query_return = db_connection.execute_query(db_connection.sql_dict.get('buscar_usuario'),
                                               (cedula,))
    print(len(query_return))
    match len(query_return):
        case 0:
            raise HTTPException(status_code=500, detail='No existe el usuario con la cedula ingresada')
        case _:
            # correo = listToStringWithoutBrackets(query_return)
            correo = query_return[0][0]
            print(correo)
            send_email(correo, motivo, monto)
            return {'status': 'successful'}


def send_email(correo: str, descripcion: str, valor: float):
    gmail_user = 'alvaradolayonardo@gmail.com'
    gmail_password = 'mqjjqbpmctkleorb'

    sent_from = gmail_user
    to = [correo]
    body = f"""{descripcion}\n
    {valor}"""

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
