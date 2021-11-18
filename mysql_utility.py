# Library for connecting to the database.
import mysql.connector


class DBConnector:

    # Dict containing SQL queries related to database.
    sql_dict = {
        'login': 'select count(*) from CLIENTE where cedula = %s and password = %s',
        'saldo_actual': 'select saldo_actual from CUENTA_FINANCIERA where cliente_cedula = %s and numero_cuenta = %s',
        'mis_cuentas': 'select numero_cuenta from CUENTA_FINANCIERA where cliente_cedula = %s',
        'realizar_transferencia': 'select realizar_transferencia(%s, %s, %s, %s, %s, %s)',
        'buscar_usuario': 'select cedula from CLIENTE'
    }

    # Dict containing Error/Message codes related to SQL returns.
    messages_dict = {
        0: 'Se realizo la transferencia correctamente',
        -1: 'No tiene saldo suficiente para hacer la transferencia',
        -2: 'La institucion no existe o es incorrecta',
        -3: 'La cuenta financiera no existe en base al numero de cuenta o a la institucion'
    }

    def __init__(self):
        """
        Class constructor.
        Creates a new instance of mysql connector using connection parameters.
        """
        self.db = mysql.connector.connect(
            host='localhost',
            user='monty',
            password='montypassword',
            database='practica2'
        )

    def execute_query(self, sql_query: str, parameters: tuple):
        """
        Method for executing a query with or without parameters.
        :param sql_query: A valid SQL query based on sql_dict.
        :param parameters: A tuple which contains information related to sql_query.
        :return: a list of results containing information.
        """
        cursor = self.db.cursor()
        if parameters is not None:
            cursor.execute(sql_query, parameters)
            return cursor.fetchall()
        else:
            cursor.execute(sql_query)
            return cursor.fetchall()
