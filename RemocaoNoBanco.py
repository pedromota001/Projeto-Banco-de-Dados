import mysql.connector
from mysql.connector import Error

def removeArquivo(conexao, valor_remover):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
            DELETE FROM arquivos
            WHERE nome = %s
            """, (valor_remover,))
    except Error as erro:
        print(f"Erro ao remover usuario: {erro}")
        return None
    finally:
        cursor.close()



