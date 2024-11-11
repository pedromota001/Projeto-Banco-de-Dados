import mysql.connector
from mysql.connector import Error


def safe_security(conexao):
    try:
        cursor = conexao.cursor()
        query = """
        CREATE TRIGGER safe_security
        BEFORE INSERT ON arquivos
        FOR EACH ROW
        BEGIN
            IF NEW.tipo = '.exe' THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Nao foi possivel inserir, nao permitido arquivos.exe';
            END IF;
        END;
        """
        cursor.execute(query)
        conexao.commit()
        print("Trigger safe_security criada!")

    except Error as erro:
        print(f"Erro ao criar trigger: {erro}")
        return None
    finally:
        cursor.close()

def atualiza_acesso(conexao):
    try:
        cursor = conexao.cursor()
        query = """
        CREATE TRIGGER atualiza_acesso
        AFTER INSERT ON compartilhamentos
        FOR EACH ROW
        BEGIN 
            UPDATE compartilhamentos
            SET id_usuario_compartilhado = NEW.id_usuario_compartilhado
            WHERE id_arquivo = NEW.id_arquivo;
        END;
        """
        cursor.execute(query)
        cursor.commit()
        print("Trigger atualiza_acesso criada com sucesso!")
    except Error as erro:
        print(f"Erro ao criar trigger atualiza_acesso {erro}")
        return None
    finally:
        cursor.close()

def registrar_operacao(conexao):
    try:
        cursor = conexao.cursor()

        query = """
        CREATE TRIGGER registrar_operacao
        AFTER INSERT ON arquivos
        FOR EACH ROW
        BEGIN
            UPDATE atividades_recentes
            SET ultima_versao = NOW()
            WHERE id_arquivo = NEW.id;
        END;
        """
        cursor.execute(query)

        conexao.commit()
        print("Trigger 'registrar_operacao' criada com sucesso!")

    except mysql.connector.Error as err:
        print(f"Erro ao criar a trigger: {err}")
    finally:
        cursor.close()
