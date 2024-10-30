import mysql.connector

try:
    conexao = mysql.connector.connect(
        host= "127.0.0.1",
        port= "3306",
        user="root",
        password="pedro123"
    )
    if(conexao.is_connected()):
        print("Conexao bem sucedida")
        cursor = conexao.cursor();
        cursor.execute("CREATE DATABASE IF NOT EXISTS webDriver_db")
        print("DataBase criado com sucesso")
        cursor.database = 'webdriver_db'
except mysql.connector.Error as erro:
    print(f"conexao mal sucedida: {erro}")
finally:
    if(conexao.is_connected()):
        conexao.close()
