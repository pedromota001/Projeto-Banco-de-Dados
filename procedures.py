import mysql.connector
from mysql.connector import Error

import mysql.connector


def verificar_atividades(conexao):
    try:
        cursor = conexao.cursor()
        query = """
        CREATE PROCEDURE verificar_atividades()
        BEGIN
            UPDATE atividades_recentes SET ultima_versao = CURDATE();
            SELECT CONCAT(ROW_COUNT(), ' linhas foram atualizadas com a data atual.') AS mensagem_sucesso;
        END;
        """
        cursor.execute(query)
        conexao.commit()
        print("Procedure criada com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao criar a procedure: {err}")
    finally:
        cursor.close()

def conta_usuario(conexao):

    try:
        cursor = conexao.cursor()
        cursor.execute("""   
        CREATE PROCEDURE ContaUsuarios(IN arquivo_id INT, OUT total_usuarios INT)
        BEGIN
            SELECT COUNT(DISTINCT id_usuario) + COUNT(DISTINCT id_usuario_compartilhado) INTO total_usuarios
            FROM arquivos a 
            INNER JOIN compartilhamentos c ON c.id_arquivo = a.id_arquivo
            WHERE a.id_arquivo = arquivo_id;
            IF total_usuarios IS NULL THEN
                SET total_usuarios = 0;
            END IF;
        END; 
        """)
    except Error as erro:
        print(f"Erro ao criar procedure de contagem de usuarios: {erro}")
        return None
    finally:
        cursor.close()

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

def remover_acessos(conexao, id_arquivo):
    cursor = conexao.cursor()

    try:
        cursor.execute("""

            CREATE PROCEDURE remover_acessos(IN r_id_arquivo INT)
            BEGIN
                DECLARE v_id_usuario_dono INT;
               IF EXISTS (
                    SELECT 1
                    FROM arquivos
                    WHERE id_arquivo = r_id_arquivo
               ) THEN
                    SELECT id_usuario_dono INTO v_id_usuario_dono
                    FROM compartilhamentos
                    WHERE id_arquivo = r_id_arquivo;   

                    UPDATE arquivos
                    SET permissao = false
                    WHERE id_arquivo = r_id_arquivo
                    AND id_usuario != v_id_usuario_dono;
                END IF;
            END;                  
        """)

        print("Procedimento 'remover_acessos' criado com sucesso.")
        conexao.commit()
    except Exception as error:
        print(f"Erro ao remover acessos: {error}")
    finally:
        cursor.close()    