from datetime import datetime
import mysql.connector
from mysql.connector import Error

def insert_arquivos(conexao, id_usuario):
    try:
        cursor = conexao.cursor()
        nome = input("Digite o nome do arquivo: ")
        tipo = input("Digite o tipo desse arquivo: ")
        url = input("Digite o url do arquivo: ")
        tam = input("Digite o tamanho desse arquivo: ")
        permissao = input("Digite o tipo de permissao desse arquivo: ")
        data_ult_modificacao = datetime.now()
        cursor.execute("""
        INSERT INTO arquivos(permissao, nome, tipo, url, tam, data_ult_modificacao, id_usuario)VALUES(%s,%s,%s,%s,%s,%s, %s);
        """, (permissao, nome, tipo, url, tam, data_ult_modificacao, id_usuario))
        print("Insercao efetuada com sucesso! ")
    except Error as erro:
        print(f"Erro ao inserir arquivo: {erro}")
        return None
    finally:
        cursor.close()    