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

