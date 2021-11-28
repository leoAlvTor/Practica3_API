# Libreria para conectarse a la base de datos.
import mysql.connector


class DBConnector:

    # Diccionario que contiene consultas SQL relacionadas con la base de datos.
    sql_dict = {
        'obtener_institucion': 'select count(*) from Cliente where cedula = %s',
        'saldo_actual': 'select saldo from Cuenta where cliente_id = %s and cuenta_id = %s',
        'debito': 'update Cuenta  set saldo = saldo - %s  where cliente_id = %s and cuenta_id = %s',
        'deposito': ' update Cuenta set saldo = saldo + %s  where cliente_id = %s and cuenta_id = %s',
        'mis_cuentas': 'select cuenta_id from Cuenta where cliente_id = %s',
        'realizar_transferencia': 'select realizar_transferencia(%s, %s, %s, %s, %s, %s)',
        'buscar_usuario': 'select cedula from CLIENTE'
    }

    # Diccionario que contiene códigos de error / mensaje relacionados con devoluciones de SQL.
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
            database='Jep'
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
            print('query: ', sql_query, 'parameters: ', parameters)
            cursor.execute(sql_query, parameters)
            return cursor.fetchall()
        else:
            cursor.execute(sql_query)
            return cursor.fetchall()
