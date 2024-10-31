import mysql.connector

try:
    conexao = mysql.connector.connect(
        host= "127.0.0.1",
        port= "3306",
        user="root",
        password="pedro123"
    )
    if(conexao.is_connected()):
        print("Conexao bem sucedida")
        cursor = conexao.cursor();
        cursor.execute("CREATE DATABASE IF NOT EXISTS webDriver_db")
        print("DataBase criado com sucesso")
        cursor.execute("USE webdriver_db")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS planos(
            id INT AUTO_INCREMENT,
            nome VARCHAR(20) NOT NULL,
            duracao FLOAT,
            data_aquisicao VARCHAR(20),
            espaco_por_usuario FLOAT, 
            PRIMARY KEY(id) 
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS instituicoes(
            id_instituicao INT AUTO_INCREMENT,
            nome VARCHAR(20) NOT NULL,
            endereco VARCHAR(30) NOT NULL,
            causa_social VARCHAR(15),
            id_plano INT,
            PRIMARY KEY(id_instituicao),
            FOREIGN KEY(id_plano) REFERENCES planos(id)
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios(
            id_usuario INT AUTO_INCREMENT,
            email VARCHAR(20) NOT NULL,
            senha VARCHAR(20) NOT NULL, 
            login VARCHAR(15) NOT NULL,
            data_ingresso DATE,
            id_instituicao INT, 
            PRIMARY KEY(id_usuario),
            FOREIGN KEY(id_instituicao) REFERENCES instituicoes(id_instituicao)
        );
        """)
        print("Tabelas criadas com sucesso")
except mysql.connector.Error as erro:
    print(f"conexao mal sucedida: {erro}")
finally:
    if(conexao.is_connected()):
        conexao.close()
