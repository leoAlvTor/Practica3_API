# Libreria para conectarse a la base de datos.
import mysql.connector


class DBConnector:

    # Diccionario que contiene consultas SQL relacionadas con la base de datos.
    sql_dict = {
        'login': 'select count(*) from cliente where cedula = %s and password = %s',
        'saldo_actual': 'select saldo_actual from CUENTA_FINANCIERA where cliente_cedula = %s and numero_cuenta = %s',
        'mis_cuentas': 'select numero_cuenta from CUENTA_FINANCIERA where cliente_cedula = %s',
        'realizar_transferencia': 'select realizar_transferencia(%s, %sCLIENTE, %s, %s, %s, %s)',
        'buscar_usuario': 'select correo from cliente where cedula = %s'
    }

    # #Diccionario que contiene códigos de error / mensaje relacionados con devoluciones de SQL.
    messages_dict = {
        0: 'Se realizo la transferencia correctamente',
        -1: 'No tiene saldo suficiente para hacer la transferencia',
        -2: 'La institucion no existe o es incorrecta',
        -3: 'La cuenta financiera no existe en base al numero de cuenta o a la institucion'
    }

    def __init__(self):
        """
        Constructor de clases.
        Crea una nueva instancia del conector mysql usando parámetros de conexión.
        """
        self.db = mysql.connector.connect(
            host='localhost',
            user='monty',
            password='montypassword',
            database='central'
        )

    def execute_query(self, sql_query: str, parameters: tuple):
        """
        Método para ejecutar una consulta con o sin parámetros.
        :param sql_query: Una consulta SQL válida basada en sql_dict.
        :param parameters: Una tupla que contiene información relacionada con sql_query.
        :return: una lista de resultados que contiene información.
        """
        cursor = self.db.cursor()
        if parameters is not None:
            cursor.execute(sql_query, parameters)
            return cursor.fetchall()
        else:
            cursor.execute(sql_query)
            return cursor.fetchall()
