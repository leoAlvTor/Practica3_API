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
async def debito(cedula: str, origen: str, monto: int):
    saldo_actual=au_conecction.execute_query(au_conecction.sql_dict.get('saldo_actual'),(cedula,origen))
    if len(saldo_actual) >0:
        if saldo_actual[0][0] > monto:
            debito=au_conecction.execute_query(au_conecction.sql_dict.get('debito'),(monto,cedula,origen))
            print('Paso debido')
            au_conecction.execute_query('commit', None)
            return {'status': 'Debito Realizado'}
        return {'status': 'Error en la transaccion'}

@app.post('/austro/private/deposito')
async def deposito(cedula: str, destino: str, monto: int):
    deposito=au_conecction.execute_query(au_conecction.sql_dict.get('deposito'),(monto,cedula,destino))
    au_conecction.execute_query('commit', None)
    return {'status': 'Deposito Realizado'}