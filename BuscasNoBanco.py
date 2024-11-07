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
        SELECT usuarios.email, arquivos.nome FROM usuarios 
        INNER JOIN arquivos ON usuarios.id_usuario = arquivos.id_usuario
        WHERE usuarios.id_usuario = %s; 
        """, (id_usuario,))
        arquivosEncontrados = cursor.fetchall()
        if arquivosEncontrados:
            return arquivosEncontrados
        else:
            return None
    except Error as erro:
        print(f"Erro ao buscar arquivo: {erro}")
        return None
    finally:
        cursor.close()


def buscar_arquivos_usuario_view(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT * FROM arquivos_usuario
        """)
        resultados = cursor.fetchall()
        if resultados:
            for linha in resultados:
                print(linha)
        else:
            print("Voce nao possui arquivos no drive! ")
    except Error as erro:
        print(f"Erro ao buscar view: {erro}")
    finally:
        cursor.close()



def buscar_usuario_email(conexao, email):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT * FROM usuarios 
        WHERE email = %s
        """, (email,))
        usuario = cursor.fetchone()
        if usuario:
            return usuario[0]##retorno id do usuario
        else:
            return None
    except Error as erro:
        print(f"Nao foi possivel buscar o usuario pelo email: {erro}")
        return None
    finally:
        cursor.close()



def buscar_adm(conexao, login, senha):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT * FROM administradores WHERE login = %s AND senha = %s
        """, (login, senha))
        adm = cursor.fetchone()
        if adm:
            return adm[0]
        else:
            return None
    except Error as erro:
        print(f"Não foi possivel buscar o administrador: {erro}")
        return None
    finally:
        cursor.close()




def buscar_arquivoPor_nome(conexao, nome):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT * FROM arquivos
        WHERE nome = %s
        """, (nome,))
        arquivo = cursor.fetchone()
        if arquivo:
            return arquivo[0]
        else:
            return None
    except Error as erro:
        print(f"Nao foi possivel buscar o arquivo pelo nome: {erro}")
        return None
    finally:
        cursor.close()