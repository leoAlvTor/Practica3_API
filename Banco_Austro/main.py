from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mysql_utility
from pydantic import BaseModel

app = FastAPI()
db_connection = mysql_utility.DBConnector()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Transferencia(BaseModel):
    cedula: str
    institucion_destino: str
    origen: str
    destino: str
    monto: float
    motivo: str


@app.get("/")
async def main():
    return {"message": "Hello World"}


@app.post('/login')
async def login(cedula: str, password: str):
    query_return = db_connection.execute_query(db_connection.sql_dict.get('login'),
                                               (cedula, password))[0][0]
    match query_return:
        case 1:
            return {'status': 'successful'}
        case 0:
            raise HTTPException(status_code=500, detail='Cedula o Password incorrectos.')


@app.get('/private/saldo_actual')
async def get_saldo(cedula: str, cuenta_id: str):
    query_return = db_connection.execute_query(db_connection.sql_dict.get('saldo_actual'), (cedula, cuenta_id))
    match len(query_return):
        case 0:
            raise HTTPException(status_code=500, detail='El # Cedula/Cuenta no es correcto.')
        case _:
            return query_return[0][0]


@app.post('/private/transferencia')
async def transferir_saldo(datos: Transferencia):
    query_return = db_connection.execute_query(db_connection.sql_dict.get('realizer_transferencia'),
                                               (datos.cedula, datos.institucion_destino, datos.origen, datos.destino,
                                                datos.monto, datos.motivo))
    match len(query_return):
        case 0:
            raise HTTPException(status_code=418, detail='Error while trying to work with database! ??')
        case _:
            return {'status': db_connection.messages_dict.get(query_return[0][0])}
