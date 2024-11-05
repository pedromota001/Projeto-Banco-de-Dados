import mysql.connector
from mysql.connector import Error


def cria_role_PapelUsuario(conexao, id_usuario):
     try:
        cursor = conexao.cursor()
        cursor.execute("""
        CREATE ROLE PapelUsuario,
        GRANT CONNECT TO PapelUsuario,
        GRANT SELECT ON arquivos_usuario TO PapelUsuario,
        GRANT INSERT ON arquivos_usuario TO PapelUsuario,
        GRANT UPDATE ON arquivos_usuario TO PapelUsuario
        """, 
        conexao.commit()
    except Error as erro:
        print(f"Nao foi possivel criar role: {erro}")
        return None
    finally:
        cursor.close()

def cria_role_PapelEmpresa(conexao):
     try:
        cursor = conexao.cursor()
        cursor.execute("""
        CREATE ROLE PapelEmpresa,
        GRANT CONNECT TO PapelEmpresa,
        GRANT SELECT ON view_empresa TO PapelEmpresa,
        GRANT SELECT ON view_empresa TO PapelEmpresa
        """,
        conexao.commit()
    except Error as erro:
        print(f"Nao foi possivel criar role: {erro}")
        return None
    finally:
        cursor.close()

def cria_role_PapelAdm(conexao):
     try:
        cursor = conexao.cursor()
        cursor.execute("""
        CREATE ROLE PapelAdm,
        GRANT ALL PRIVILEGES ON webdriver_db.* TO 'PapelAdm';
        """,
        conexao.commit()
    except Error as erro:
        print(f"Nao foi possivel criar role: {erro}")
        return None
    finally:
        cursor.close()
