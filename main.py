# Libraries for API definition
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Class for Mysql database connection.
import mysql_utility

# Class for request model parameters.
from pydantic import BaseModel

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


# Class for request model parameters.
class Transferencia(BaseModel):
    cedula: str
    institucion_destino: str
    origen: str
    destino: str
    monto: float
    motivo: str


@app.post('/api/login')
async def login(cedula: str, password: str):
    """
    Method for logging in.
    :param cedula: The ID of the user.
    :param password: The password of the user.
    :return: status successful if user exists otherwise raise a new Http Exception with status code 500.
    """
    query_return = db_connection.execute_query(db_connection.sql_dict.get('login'),
                                               (cedula, password))[0][0]
    match query_return:
        case 1:
            return {'status': 'successful'}
        case 0:
            return {'status': 'Cedula o Password incorrectos.'}


@app.get('/api/private/saldo_actual')
async def get_saldo(cedula: str, cuenta_id: str):
    """
    Method for checking account balance.
    :param cedula: The Id of the user.
    :param cuenta_id: The account number of the user.
    :return: the current balance according ID and account number otherwise return Http Exception if the ID or account
    number is incorrect.
    """
    query_return = db_connection.execute_query(db_connection.sql_dict.get('saldo_actual'), (cedula, cuenta_id))
    match len(query_return):
        case 0:
            return {'status': 'El # Cedula/Cuenta no es correcto.'}
        case _:
            return query_return[0][0]


@app.get('/api/private/mis_cuentas')
async def get_cuentas(cedula: str):
    """
    Function for getting all economic accounts by user.
    :param cedula: The user ID
    :return: status with data related to accounts number otherwise return an error.
    """
    query_return = db_connection.execute_query(db_connection.sql_dict.get('mis_cuentas'), (cedula,))
    match len(query_return):
        case 0:
            return {'status': 'No hay cuentas asociadas a la cedula ingresada.'}
        case _:
            return {'status': 'successful', 'data': [x[0] for x in query_return]}


@app.post('/api/private/transferencia')
async def transferir_saldo(cedula, institucion_destino, origen, destino, monto, motivo):
    """
    Method for transferring money between accounts.
    :param datos: A valid JSON containing information about the transaction to being processed.
    :return: A message containing information about the transaction (Refer to mysql_utility.py for checking messages).
    """
    print('Transferencia: ', origen, 'destino', destino)
    query_return = db_connection.execute_query(db_connection.sql_dict.get('realizar_transferencia'),
                                               (cedula, institucion_destino, origen, destino,
                                                monto, motivo))
    db_connection.db.commit()
    match len(query_return):
        case 0:
            return {'status': 'Error while trying to work with database! ??'}
        case _:
            return {'status': db_connection.messages_dict.get(query_return[0][0])}
