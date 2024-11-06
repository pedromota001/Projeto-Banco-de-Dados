import mysql.connector
from mysql.connector import Error

def cria_role_PapelUsuario(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("CREATE ROLE PapelUsuario")
        cursor.execute("GRANT CONNECT ON DATABASE webdriver_db TO PapelUsuario")
        cursor.execute("GRANT SELECT ON arquivos_usuario TO PapelUsuario")
        cursor.execute("GRANT INSERT ON arquivos_usuario TO PapelUsuario")
        cursor.execute("GRANT UPDATE ON arquivos_usuario TO PapelUsuario")
        conexao.commit()
        print("Role 'PapelUsuario' criada com sucesso.")
    except Exception as erro:  
        conexao.rollback()  
        print(f"Não foi possível criar a role: {erro}")    
    finally:
        cursor.close()


def cria_role_PapelEmpresa(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("CREATE ROLE PapelEmpresa")
        cursor.execute("GRANT CONNECT ON DATABASE webdriver_db TO PapelEmpresa")
        cursor.execute("GRANT SELECT ON view_empresa TO PapelEmpresa")
        conexao.commit()
        print("Role 'PapelEmpresa' criada com sucesso.")
    except Exception as erro:
        conexao.rollback()
        print(f"Não foi possível criar a role: {erro}")
    finally:
        cursor.close()


def cria_role_PapelAdm(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("CREATE ROLE PapelAdm")
        cursor.execute("GRANT ALL PRIVILEGES ON webdriver_db TO PapelAdm")
        cursor.execute("GRANT SELECT ON view_administradores TO PapelAdm")
        conexao.commit()
        print("Role 'PapelAdm' criada com sucesso.")    
    except Exception as erro:
        conexao.rollback()
        print(f"Não foi possível criar a role: {erro}")    
    finally:
        cursor.close()
