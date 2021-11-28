# Librerias para la definición de API
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Clase para la conexión a la base de datos Mysql.
import PichinchaDB_utility

# Creación de instancias de FastAPI.
app = FastAPI()
pi_connection=PichinchaDB_utility.DBConnector()


# Definición de CORS.
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Metodo GET y PATH
@app.get('/pichincha/private/cuenta')
async def institucion(cedula: str):
    pichibcha = pi_connection.execute_query(pi_connection.sql_dict.get('obtener_institucion'), (cedula,))
    match len(pichibcha):
        case 0:
            return {'status': '0'}
        case _:
            return {'status': '1'}

#Metodo POST y PATH
@app.post('/pichincha/private/debito')
async def debito(cedula , origen , monto):
    """
           Funcion que realiza el debito de dinero al usuario
           :param cedula: ingresamos el parametro cedula (str)
           :param origen: ingresamos el parametro origen (str)
           :param monto: ingresamos el parametro monto (str)
           :return: status devuelve que el deposito ha sido realizado si el saldo actual es mayor al monto de lo contrario el status devuelve error en la transaccion
           """
    saldo_actual=pi_connection.execute_query(pi_connection.sql_dict.get('saldo_actual'),(cedula, origen))
    if len(saldo_actual) > 0:
        if saldo_actual[0][0] > float(monto):
            debito=pi_connection.execute_query(pi_connection.sql_dict.get('debito'),(monto,cedula,origen))
            pi_connection.execute_query('commit', None)
            return {'status': 'Debito Realizado'}
        return {'status': 'Error en la transaccion'}

#Metodo POST y URL
@app.post('/pichincha/private/deposito')
async def deposito(cedula, destino, monto):
    """
           Funcion que realiza el deposito de dinero al usuario
           :param cedula: ingresamos el parametro cedula (str)
           :param destino: ingresamos el parametro destino (str)
           :param monto: ingresamos el parametro monto (str)
           :return: Realizada la query el status devuelve el siguiente mensaje -> deposito realizado
           """
    deposito=pi_connection.execute_query(pi_connection.sql_dict.get('deposito'),(monto,cedula,destino))
    pi_connection.execute_query('commit', None)
    return {'status': 'Deposito Realizado'}

@app.get('/pichincha/private/mis_cuentas')
async def get_cuentas(cedula: str):

    print(cedula)
    """
           Función para obtener todas las cuentas bancarias por usuario.
           :param cedula: ID del usuario
           :return: status con datos relacionados con el número de cuenta, de lo contrario, devuelve un error.
    """
    query_return = pi_connection.execute_query(pi_connection.sql_dict.get('mis_cuentas'), (cedula,))
    match len(query_return):
        case 0:
            return {'status': 'No hay cuentas asociadas a la cedula ingresada.'}
        case _:
            return {'status': 'successful', 'data': [x[0] for x in query_return]}
