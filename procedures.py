import mysql.conncetor
from datetime import date

def verificar_atividades():
    cursor = conexao.cursor()
    cursor.execute("""
    DELIMITER //
CREATE PROCEDURE verificar_atividades()
BEGIN
    SET @data_atual = CURDATE();
    UPDATE atividades_recentes SET ultima_versao = @data_atual;
    SELECT CONCAT(ROW_COUNT(), ' linhas foram atualizadas com a data atual.') AS mensagem_sucesso;
END //
DELIMITER ;
     """)
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

def chavear_arquivo(conexao, id_arquivo):
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            CREATE PROCEDURE chavear_arquivo(IN p_id_arquivo INT)
            BEGIN
                IF EXISTS (
                    SELECT 1
                    FROM arquivos
                    WHERE id_arquivo = p_id_arquivo
                ) AND EXISTS (
                    SELECT 1
                    FROM atividades_recentes
                    WHERE id_arquivo = p_id_arquivo AND acesso = 'p'
                ) THEN
                    UPDATE atividades_recentes
                    SET acesso = 'np'
                    WHERE id_arquivo = p_id_arquivo;
                ELSE
                    SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'O arquivo não existe ou não está marcado como prioritário.';
                END IF;
            END;
        """)

        print("Procedimento 'chavear_usuario' criado com sucesso.")

    except Error as erro:
        print(f"Erro ao criar procedimento: {erro}")
    finally:
        cursor.close()

