# Libraries for API definition
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Class for Mysql database connection.
import PichinchaDB_utility

# FastAPI instantiation.
app = FastAPI()
pi_connection=PichinchaDB_utility.DBConnector()


# CORS definition.
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/pichincha/private/cuenta')
async def institucion(cedula: str):
    pichibcha = pi_connection.execute_query(pi_connection.sql_dict.get('obtener_institucion'), (cedula))
    match len(pichibcha):
        case 0:
            return {'status': '0'}
        case _:
            return {'status': '1'}

@app.post('pichincha/private/debito')
async def debito(cedula: str, origen: str, monto: int):
    saldo_actual=pi_connection.execute_query(pi_connection.sql_dict.get('saldo_actual'),(cedula, origen))
    if saldo_actual > monto:
        debito=pi_connection.execute_query(pi_connection.sql_dict.get('debito'),(monto,cedula,origen))
        return {'status': 'Debito Realizado'}
    return {'status': 'Error en la transaccion'}


@app.post('pichincha/private/deposito')
async def deposito(cedula: str, destino: str, monto: int):
    deposito=pi_connection.execute_query(pi_connection.sql_dict.get('deposito'),(monto,cedula,destino))
    return {'status': 'Debito Realizado'}