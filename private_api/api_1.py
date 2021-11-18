# Libraries for API definition
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Class for Mysql database connection.
import mysql_utility

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


@app.post('/private/send_mail')
async def send_mail(cedula: str, motivo: str, monto: float):
    query_return = db_connection.execute_query(db_connection.sql_dict.get('login'),
                                               (cedula,))
    match len(query_return):
        case 0:
            raise HTTPException(status_code=500, detail='No existe el usuario con la cedula ingresada')
        case _:
            return ''
