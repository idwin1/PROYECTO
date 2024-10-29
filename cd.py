import mysql.connector
from mysql.connector import Error

def test_mysql_connection(ip_publica, usuario, contraseña, base_datos):
    try:
        # Configuración de la conexión
        config = {
            'user': usuario,
            'password': contraseña,
            'host': ip_publica,
            'database': base_datos,
            'raise_on_warnings': True
        }

        # Establecer la conexión
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            print("Conexión exitosa a la base de datos.")
            # Realiza una consulta simple para verificar la conexión
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            database_name = cursor.fetchone()
            print(f"Conectado a la base de datos: {database_name[0]}")
            cursor.close()

    except Error as err:
        print(f"Error: {err}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Conexión cerrada.")

# Reemplaza estos valores con tus datos
ip_publica = '189.194.185.106'
usuario = 'root'
contraseña = 'sandrauno'
base_datos = 'cafe'

# Llama a la función de prueba
test_mysql_connection(ip_publica, usuario, contraseña, base_datos)
