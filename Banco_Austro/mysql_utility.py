import mysql.connector


class DBConnector:

    sql_dict = {
        'login': 'select count(*) from CLIENTE where cedula = %s and password = %s',
        'saldo_actual': 'select saldo_actual from CUENTA_FINANCIERA where cliente_cedula = %s and numero_cuenta = %s',
        'realizer_transferencia': 'select realizar_transferencia(%s, %s, %s, %s, %s, %s)'
    }

    messages_dict = {
        0: 'Se realizo la transferencia correctamente',
        -1: 'No tiene saldo suficiente para hacer la transferencia',
        -2: 'La institucion no existe o es incorrecta',
        -3: 'La cuenta financiera no existe en base al numero de cuenta o a la institucion'
    }

    def __init__(self):
        self.db = mysql.connector.connect(
            host='localhost',
            user='monty',
            password='montypassword',
            database='practica2'
        )

    def execute_query(self, sql_query: str, parameters: tuple):
        cursor = self.db.cursor()
        if parameters is not None:
            cursor.execute(sql_query, parameters)
            return cursor.fetchall()
        else:
            cursor.execute(sql_query)
            return cursor
