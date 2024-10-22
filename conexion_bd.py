import mysql.connector
import socket



def pedir_ip():
    return "localhost"

def conexion():
    connection = mysql.connector.connect(
            host=pedir_ip(),
            user='root',  # Reemplaza con tu usuario de MySQL
            password='sandrauno',  # Reemplaza con tu contraseña de MySQL
            database='cafe'  # Base de datos 'cafe'
        )
    return connection

r = pedir_ip()