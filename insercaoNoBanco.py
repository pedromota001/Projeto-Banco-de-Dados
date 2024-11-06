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
        
def insert_planos(conexao):
    try:
        cursor = conexao.cursor()
        nome = input("Digite o nome do plano: ")
        duracao = float(input("Digite a duração do plano (em meses): "))
        data_aquisicao = input("Digite a data de aquisição (AAAA-MM-DD): ")
        espaco_por_usuario = float(input("Digite o espaço por usuário (em GB): "))
        cursor.execute("""
        INSERT INTO planos(nome, duracao, data_aquisicao, espaco_por_usuario) 
        VALUES (%s, %s, %s, %s);
        """, (nome, duracao, data_aquisicao, espaco_por_usuario))
        print("Plano inserido com sucesso!")
    except Error as erro:
        print(f"Erro ao inserir plano: {erro}")
    finally:
        cursor.close()
        
def insert_instituicoes(conexao):
    try:
        cursor = conexao.cursor()
        nome = input("Digite o nome da instituição: ")
        endereco = input("Digite o endereço da instituição: ")
        causa_social = input("Digite a causa social da instituição: ")
        id_plano = int(input("Digite o ID do plano ao qual a instituição está atrelada: "))

        cursor.execute("""
        INSERT INTO instituicoes(nome, endereco, causa_social, id_plano) 
        VALUES (%s, %s, %s, %s);
        """, (nome, endereco, causa_social, id_plano))

        print("Instituição inserida com sucesso!")
    except Error as erro:
        print(f"Erro ao inserir instituição: {erro}")
    finally:
        cursor.close()
