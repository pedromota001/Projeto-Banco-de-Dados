import mysql.connector
from mysql.connector import Error

def view_arquivo_usuario(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        CREATE OR REPLACE VIEW arquivos_usuario AS
        SELECT
        a.nome, a.tipo, a.tam, a.data_ult_modificacao
        FROM arquivos a
        INNER JOIN compartilhamentos c ON c.id_arquivo = a.id_arquivo
        WHERE id_usuario_dono = @id_usuario_logado OR id_usuario_compartilhado = @id_usuario_logado
        """)
        conexao.commit()
    except Error as erro:
        print(f"Nao foi possivel criar view: {erro}")
        return None
    finally:
        cursor.close()
