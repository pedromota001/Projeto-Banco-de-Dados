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


