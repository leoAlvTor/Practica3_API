# Libraries for API definition
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Class for Mysql database connection.
from pydantic import BaseModel

import AustroDB_utility


# FastAPI instantiation.
app = FastAPI()
au_conecction = AustroDB_utility.DBConnector()

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

@app.get('/austro/private/cuenta')
async def institucion(cedula: str):
    austro = au_conecction.execute_query(au_conecction.sql_dict.get('obtener_institucion'), (cedula,))
    match len(austro):
        case 0:
            return {'status': '0'}
        case _:
            return {'status': '1'}


@app.post('/austro/private/debito')
async def debito(cedula , origen , monto ):
    saldo_actual=au_conecction.execute_query(au_conecction.sql_dict.get('saldo_actual'),(cedula,origen))
    if len(saldo_actual) >0:
        if saldo_actual[0][0] > float(monto):
            debito=au_conecction.execute_query(au_conecction.sql_dict.get('debito'),(monto,cedula,origen))
            print('Paso debido')
            au_conecction.execute_query('commit', None)
            return {'status': 'Debito Realizado'}
        return {'status': 'Error en la transaccion'}

@app.post('/austro/private/deposito')
async def deposito(cedula , destino , monto):
    deposito=au_conecction.execute_query(au_conecction.sql_dict.get('deposito'),(monto,cedula,destino))
    au_conecction.execute_query('commit', None)
    return {'status': 'Deposito Realizado'}

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
