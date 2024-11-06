import mysql.conncetor
from datetime import date

def verificar_atividades():
    cursor = conexao.cursor()
    data_atual = date.today()
    query = "UPDATE atividades_recentes SET ultima_versao = %s"
    cursor.execute(query, (data_atual,))
    if cursor.rowcount > 0:
        conexao.commit()
        print('Tabela Atividades atualizadas com sucesso!')
    else:
        conexao.rollback()
        print('Nenhuma linha foi atualizada com sucesso!')
    cursor.close()
    conexao.close()
verificar_atividades()

def conta_usuario(id_arquivo):
    cursor = conexao.cursor()

    try:
        verifica_arquivo_query = '''
        SELECT COUNT(*) 
        FROM arquivos
        WHERE id_arquivo = %s;
        '''
        cursor.execute(verifica_arquivo_query, (id_arquivo,))
        resultado = cursor.fetchone()
        return result[0] if resul else 0
    except mysql.connector.Error as erro:
        print("Erro ao acessar o banco de dados", erro)
        return None
    finally:
        cursor.close()
        conexao.close()
id_arquivo = 1
print(f"Usuarios  distintos  com acesso ao arquivo {id_arquivo}: {conta_usuario(id_arquivo)}")



