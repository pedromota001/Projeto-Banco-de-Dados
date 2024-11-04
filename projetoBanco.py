from datetime import datetime

import mysql.connector
from mysql.connector import Error

import BuscasNoBanco
from BuscasNoBanco import buscar_arquivos_usuario


def criar_conexao():
    try:
        conexao = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="root",
            password="pedro123"
        )
        if conexao.is_connected():
            print("Conexão com o banco de dados bem-sucedida.")
            return conexao
    except Error as erro:
        print(f"Erro ao conectar ao banco de dados: {erro}")
        return None

def criar_banco_de_dados(cursor):
    cursor.execute("CREATE DATABASE IF NOT EXISTS webDriver_db")
    print("Banco de dados 'webDriver_db' criado com sucesso.")
    cursor.execute("USE webDriver_db")

def criar_tabelas(cursor):
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
    print("Tabela 'planos' criada com sucesso.")

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
    print("Tabela 'instituicoes' criada com sucesso.")

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
    print("Tabela 'usuarios' criada com sucesso.")
##alterar permissao de boolean para varchar talvez.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS arquivos(
            id_arquivo INT AUTO_INCREMENT,
            permissao BOOLEAN DEFAULT FALSE,
            nome VARCHAR(20) NOT NULL,
            tipo VARCHAR(20) NOT NULL,
            url VARCHAR(15) UNIQUE NOT NULL, 
            tam FLOAT NOT NULL,
            data_ult_modificacao DATE,
            id_usuario INT,
            PRIMARY KEY(id_arquivo), 
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
        );
    """)
    print("Tabela 'arquivos' criada com sucesso")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comentarios(
            id_comentario INT AUTO_INCREMENT, 
            conteudo VARCHAR(20), 
            data_comentario DATE,
            hora_comentario TIME, 
            id_usuario INT,
            id_arquivo INT,
            PRIMARY KEY(id_comentario),
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario),
            FOREIGN KEY(id_arquivo) REFERENCES arquivos(id_arquivo)
        );
    """)
    print("Tabela 'comentarios' criada com sucesso")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_versionamento(
            id_historico INT AUTO_INCREMENT,
            data_historico DATE,
            hora_historico TIME,
            operacao_historico VARCHAR(15),
            id_usuario_alterou INT,
            conteudo_mudado VARCHAR(50),
            id_arquivo INT,
            PRIMARY KEY (id_historico),
            FOREIGN KEY(id_arquivo) REFERENCES arquivos(id_arquivo)
        ); 
    """)
    print("Tabela 'historico_versionamento' criada com sucesso.")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operacoes(
            id_operacoes INT AUTO_INCREMENT,
            data_op DATE,
            hora_op TIME,
            tipo_operacao VARCHAR(15),
            id_arquivo INT,
            id_usuario INT,
            PRIMARY KEY(id_operacoes),
            FOREIGN KEY(id_arquivo) REFERENCES arquivos(id_arquivo),
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
        ); 
    """)
    print("Tabela 'operacoes' criada com sucesso.")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compartilhamentos(
            id_compartilhado INT AUTO_INCREMENT,
            id_usuario INT,
            id_arquivo INT,
            data_compartilhado DATE,
            PRIMARY KEY(id_compartilhado),
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario),
            FOREIGN KEY(id_arquivo) REFERENCES arquivos(id_arquivo)
        );
    """)
    print("Tabela 'compartilhamentos' criada com sucesso.")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS administradores(
            id_adm INT AUTO_INCREMENT,
            email VARCHAR(20),
            senha VARCHAR(15),
            login VARCHAR(20),
            PRIMARY KEY(id_adm),
            data_ingresso DATE
        );
    """)
    print("Tabela 'administradores' criada com sucesso.")

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS adm_usuarios(
                id_adm INT,
                id_usuario INT,
                FOREIGN KEY(id_adm) REFERENCES administradores(id_adm),
                FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
            ); 
        """)
    print("Tabela 'adm_usuarios' criada com sucesso.")


def insert_Arquivos(cursor, id_usuario):
    nome = input("Digite o nome do arquivo: ")
    tipo = input("Digite o tipo desse arquivo: ")
    url = input("Digite o url do arquivo: ")
    tam = input("Digite o tamanho desse arquivo: ")
    permissao = input("Digite o tipo de permissao desse arquivo: ")
    data_ult_modificacao = datetime.now()
    cursor.execute("""
    INSERT INTO arquivos(permissao, nome, tipo, url, tam, data_ult_modificacao, id_usuario)VALUES(%s,%s,%s,%s,%s,%s, %s);
    """, (permissao, nome, tipo, url, tam, data_ult_modificacao, id_usuario))
    print("Insercao efetuada com sucesso! ")


def exibeMenu():
        print("""
            OPCOES DE LOGIN
            1 - Usuario
            2 - Administrador 
            3 - Se cadastrar como usuario, caso nao tenha conta
            0 - Encerrar
                    """)
        resp = int(input("Digite sua resposta: "))
        return resp


def exibeMenuUsuario(conexao):
    login = str(input("Digite seu login: "))
    senha = str(input("Digite sua senha: "))
    usuario = BuscasNoBanco.buscar_usuario(conexao, login, senha)
    if usuario:
        op = -1
        print("Bem vindo!!!!")
        while op != 0:
            # implementar outras opcoes
            print("""
            Opcoes:
            1 - Inserir arquivo no driver
            2 - Listar meus arquivos
            0 - Sair
            """)
            op = int(input("Digite sua opcao: "))
            if op == 1:
                insert_Arquivos(conexao.cursor(), usuario)
                conexao.commit()
            elif op == 2:
                arquivos = buscar_arquivos_usuario(conexao, usuario)
                if arquivos:
                    for arquivo in arquivos:
                        print(arquivo[0])
                else:
                    print("Voce nao tem arquivos no drive")

        #implementar outras opcoes
    else:
        print("Usuario nao cadastrado no banco")

def main():
    conexao = criar_conexao()
    if conexao:
        try:
            cursor = conexao.cursor()
            criar_banco_de_dados(cursor)
            criar_tabelas(cursor)
            resp = -1
            while (resp != 0):
                resp = exibeMenu()
                if resp == 1:
                    exibeMenuUsuario(conexao)
            print("Encerrando aplicacao...")
        except Error as erro:
            print(f"Erro ao criar banco de dados ou tabelas: {erro}")
        finally:
            cursor.close()
            conexao.close()
            print("Conexão encerrada.")

if __name__ == "__main__":
    main()
