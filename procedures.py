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
            SET total_usuarios = 0;
        
            SELECT COUNT(DISTINCT a.id_usuario) + IFNULL(COUNT(DISTINCT c.id_usuario_compartilhado), 0)
            INTO total_usuarios
            FROM arquivos a
            LEFT JOIN compartilhamentos c ON c.id_arquivo = a.id_arquivo
            WHERE a.id_arquivo = arquivo_id;
        
            IF total_usuarios IS NULL THEN
                SET total_usuarios = 0;
            END IF;
        END;
        """)
        conexao.commit()
    except Error as erro:
        print(f"Erro ao criar procedure de contagem de usuarios: {erro}")
        return None
    finally:
        cursor.close()

def chavear_arquivo(conexao):
    cursor = conexao.cursor()

    try:
        cursor.execute("""
    CREATE PROCEDURE chavear_arquivo(IN p_id_arquivo INT)
    BEGIN
        IF EXISTS (
            SELECT 1
            FROM arquivos
            WHERE id_arquivo = p_id_arquivo
        ) THEN
            IF EXISTS (
                SELECT 1
                FROM atividades_recentes
                WHERE id_arquivo = p_id_arquivo AND acesso = 'p'
            ) THEN
                UPDATE atividades_recentes
                SET acesso = 'np'
                WHERE id_arquivo = p_id_arquivo;
            ELSEIF EXISTS (
                SELECT 1
                FROM atividades_recentes
                WHERE id_arquivo = p_id_arquivo AND acesso = 'np'
            ) THEN
                UPDATE atividades_recentes
                SET acesso = 'p'
                WHERE id_arquivo = p_id_arquivo;
            ELSE
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'O arquivo não existe na tabela de atividades recentes ou não está marcado como prioritário ou não prioritário.';
            END IF;
        ELSE
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'O arquivo não existe na tabela arquivos.';
        END IF;
    END;
""")

        conexao.commit()
        print("Procedimento 'chavear_usuario' criado com sucesso.")

    except Error as erro:
        print(f"Erro ao criar procedimento: {erro}")
    finally:
        cursor.close()

def remover_acessos(conexao):
    try:
        cursor = conexao.cursor()
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

                    UPDATE compartilhamentos
                    SET id_usuario_compartilhado = NULL
                    WHERE id_arquivo = r_id_arquivo
                    AND id_usuario_compartilhado != v_id_usuario_dono;
                END IF;
            END;                  
        """)
        conexao.commit()
        print("Procedimento 'remover_acessos' criado com sucesso.")
    except Exception as error:
        print(f"Erro ao remover acessos: {error}")
    finally:
        cursor.close()    