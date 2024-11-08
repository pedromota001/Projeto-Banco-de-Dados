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



def remove_arquivo_por_id(conexao, id_arquivo):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        DELETE FROM arquivos 
        WHERE id_arquivo = %s
        """, (id_arquivo,))
        conexao.commit()
        print("Remocao efetuada!")
    except Error as erro:
        print("Erro ao remover arquivo: {erro}")
        return None
    finally:
        cursor.close()