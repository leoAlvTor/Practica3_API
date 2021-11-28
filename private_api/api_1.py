# Librerias para la definición de API
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Clase para la conexión a la base de datos Mysql.
import mysql_utility
import smtplib

# Creación de instancias de FastAPI.
app = FastAPI()
db_connection = mysql_utility.DBConnector()

#Definición de CORS.
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#Metodo POST Y PATH
@app.post('/api/private/send_mail')
async def send_mail(cedula, motivo, monto):
    """
    Funcion para enviar un mail
    :param cedula: ID usuario (str)
    :param motivo: descripcion (str)
    :param monto: cantidad de dinero (str)
    :return: status successful si el case es diferente de 0
    """
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
            send_email(correo, motivo, float(monto))
            return {'status': 'successful'}


def send_email(correo, descripcion, valor):
    """
    funcion para enviar correo de una cuenta origen
    :param correo: ID usuario (str)
    :param descripcion: Descripcion (str)
    :param valor: valor monetario (str)
    :return: Email sent caso contrario devuelve exception e
    """
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
