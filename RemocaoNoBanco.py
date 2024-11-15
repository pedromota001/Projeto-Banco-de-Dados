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
        print(f"Erro ao remover usuário: {erro}")
        return None
    finally:
        cursor.close()



def remocao_historico_versionamento(conexao, id_arquivo):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        DELETE FROM historico_versionamento WHERE id_arquivo = %s;
        """, (id_arquivo,))
        conexao.commit()
    except Error as erro:
        print(f"Erro ao remover de histórico de versionamento: {erro}")
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
        print("Remoção efetuada!")
    except Error as erro:
        print(f"Erro ao remover arquivo: {erro}")
        return None
    finally:
        cursor.close()

def remove_arquivo_atividades_recentes(conexao, id_arquivo):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        DELETE FROM atividades_recentes 
        WHERE id_arquivo = %s 
        """, (id_arquivo,))
        conexao.commit()
        print("Arquivo removido da tabela de atividades recentes por ser muito antigo!\n")

    except Error as erro:
        print(f"Erro ao remover arquivo de atividades recentes: {erro}")
        return None
    finally:
        cursor.close()