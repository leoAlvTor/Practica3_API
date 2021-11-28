# Librerias
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

# libreria para generar la conexion con la BD
from pydantic import BaseModel
#importamos la clase AustroBD_utility donde se encuentran las sentencias a usar
import AustroDB_utility


# instanciamiento de FastApi.
app = FastAPI()
au_conecction = AustroDB_utility.DBConnector()

# Definicion cors.
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Clase para los parámetros del modelo de solicitud.
class Transferencia(BaseModel):
    cedula: str
    institucion_destino: str
    origen: str
    destino: str
    monto: float
    motivo: str

#Metodo GET y PATH
@app.get('/austro/private/cuenta')
async def institucion(cedula: str):
    """
    funcion para saber a que institucion pertenece un usuario
    :param cedula: ID Usuario (str)
    :return: status devuelve 0 si la cedula ingresada no existe de lo contrario status devuelve 1
    """
    austro = au_conecction.execute_query(au_conecction.sql_dict.get('obtener_institucion'), (cedula,))
    match len(austro):
        case 0:
            return {'status': '0'}
        case _:
            return {'status': '1'}

#Metodo POST y PATH
@app.post('/austro/private/debito')
async def debito(cedula , origen , monto ):
    """
    Funcion que realiza el debito de dinero al usuario
    :param cedula: ID usuario (str)
    :param origen: ingresamos el parametro origen (str)
    :param monto: ingresamos el parametro monto (str)
    :return: status devuelve que el deposito ha sido realizado si el saldo actual es mayor al monto de lo contrario el status devuelve error en la transaccion
    """
    saldo_actual=au_conecction.execute_query(au_conecction.sql_dict.get('saldo_actual'),(cedula,origen))
    if len(saldo_actual) >0:
        if saldo_actual[0][0] > float(monto):
            debito=au_conecction.execute_query(au_conecction.sql_dict.get('debito'),(monto,cedula,origen))
            print('Paso debido')
            au_conecction.execute_query('commit', None)
            return {'status': 'Debito Realizado'}
        return {'status': 'Error en la transaccion'}

#Metodo POST y PATH
@app.post('/austro/private/deposito')
async def deposito( destino , monto):
    """
    Funcion que realiza el deposito de dinero al usuario
    :param cedula: ingresamos el parametro cedula (str)
    :param destino: ingresamos el parametro destino (str)
    :param monto: ingresamos el parametro monto (str)
    :return: Realizada la query el status devuelve el siguiente mensaje -> deposito realizado
    """
    deposito=au_conecction.execute_query(au_conecction.sql_dict.get('deposito'),(monto,destino))
    au_conecction.execute_query('commit', None)
    return {'status': 'Deposito Realizado'}

#Metodo GET y PATH
@app.get('/austro/private/mis_cuentas')
async def get_cuentas(cedula: str):
    """
    Función para obtener todas las cuentas bancarias por usuario.
    :param cedula: ID del usuario (str)
    :return: status con datos relacionados con el número de cuenta, de lo contrario, devuelve un error.
    """
    query_return = au_conecction.execute_query(au_conecction.sql_dict.get('mis_cuentas'), (cedula,))
    match len(query_return):
        case 0:
            return {'status': 'No hay cuentas asociadas a la cedula ingresada.'}
        case _:
            return {'status': 'successful', 'data': [x[0] for x in query_return]}
