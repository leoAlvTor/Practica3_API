# Libraries for API definition
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Class for Mysql database connection.
import JepDB_utility

# FastAPI instantiation.
app = FastAPI()
je_connection=JepDB_utility.DBConnector()

# CORS definition.
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/jep/private/cuenta')
async def institucion(cedula: str):
    print(cedula)
    jep = je_connection.execute_query(je_connection.sql_dict.get('obtener_institucion'),(cedula,))
    print(jep)
    match len(jep):
        case 0:
            return {'status': '0'}
        case _:
            return {'status': '1'}


@app.post('/jep/private/debito')
async def debito(cedula: str, origen: str, monto: int):
    saldo_actual=je_connection.execute_query(je_connection.sql_dict.get('saldo_actual'),(cedula, origen))
    if len(saldo_actual) > 0:
        if saldo_actual[0][0] > monto:
            debito=je_connection.execute_query(je_connection.sql_dict.get('debito'),(monto,cedula,origen))
            je_connection.execute_query('commit', None)
            return {'status': 'Debito Realizado'}
        return {'status': 'Error en la transaccion'}

@app.post('/jep/private/deposito')
async def deposito(cedula: str, destino: str, monto: int):
    deposito=je_connection.execute_query(je_connection.sql_dict.get('deposito'),(monto,cedula,destino))
    je_connection.execute_query('commit', None)
    return {'status': 'Deposito Realizado'}