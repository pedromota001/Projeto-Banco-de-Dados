import mysql.connector
from mysql.connector import Error

def buscar_usuario(conexao, login, senha):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT * FROM usuarios WHERE login = %s AND senha = %s
        """, (login, senha))
        usuario = cursor.fetchone()
        if usuario:
            return usuario[0] #retorno de id do usuario
        else:
            return None
    except Error as erro:
        print(f"Erro ao buscar usuario: {erro}")
        return None
    finally:
        cursor.close()

def buscar_arquivos_usuario(conexao, id_usuario):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT arquivos.nome FROM arquivos INNER JOIN usuarios ON arquivos.id_usuario = usuarios.id_usuario WHERE arquivos.id_usuario = %s; 
        """, (id_usuario,))
        arquivo = cursor.fetchall()
        if arquivo:
            return arquivo
        else:
            return None
    except Error as erro:
        print(f"Erro ao buscar arquivo: {erro}")
        return None
    finally:
        cursor.close()