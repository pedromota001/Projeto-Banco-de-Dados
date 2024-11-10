import mysql.connector
from mysql.connector import Error

def function(conexao):
    try:
        cursor = conexao.cursor()
        query = """
        CREATE FUNCTION verificar_arquivo_antigo(data_ult_modificacao DATE)
        RETURNS BOOLEAN
        DETERMINISTIC
        BEGIN
            DECLARE resultado BOOLEAN
            IF DATEDIFF(CURDATE(), data_ult_modificacao) > 100 THEN
                SET resultado = TRUE;
            ELSE
                SET resultado = FALSE;
            END IF;
            
            RETURN resultado;
        END;
        """
        cursor.execute(query)
        conexao.commit()
        print("Função 'verificar_arquivo_antigo' criada com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao criar a função: {err}")
    finally:
        cursor.close()
