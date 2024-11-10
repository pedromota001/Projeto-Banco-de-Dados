from datetime import datetime

import mysql.connector
from mysql.connector import Error

import BuscasNoBanco
import CriacaoDeRoles
import CriacaoDeViews
import RemocaoNoBanco
import insercaoNoBanco
from BuscasNoBanco import buscar_arquivos_usuario, buscar_usuario_email, buscar_arquivoPor_nome, \
    buscar_arquivos_proprios_compartilhados
from RemocaoNoBanco import remove_arquivo_por_id
from insercaoNoBanco import insert_compartilhamentos, insert_operacoes
from procedures import verificar_atividades, conta_usuario, chavear_arquivo, remover_acessos


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
            duracao INT,
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
            email VARCHAR(20) UNIQUE NOT NULL,
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
            nome VARCHAR(20) UNIQUE NOT NULL,
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
            id_usuario INT,
            PRIMARY KEY(id_operacoes),
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
        ); 
    """)
    print("Tabela 'operacoes' criada com sucesso.")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compartilhamentos(
            id_compartilhado INT AUTO_INCREMENT,
            id_usuario_dono INT,
            id_usuario_compartilhado INT,
            id_arquivo INT,
            data_compartilhado DATE,
            PRIMARY KEY(id_compartilhado),
            FOREIGN KEY(id_usuario_dono) REFERENCES usuarios(id_usuario),
            FOREIGN KEY(id_usuario_compartilhado) REFERENCES usuarios(id_usuario),
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

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS suportes(
                id_suporte INT AUTO_INCREMENT,
                dia DATE,
                hora TIME,
                descricao VARCHAR(30),
                id_adm INT,
                PRIMARY KEY(id_suporte),
                FOREIGN KEY(id_adm) REFERENCES administradores(id_adm)
            ); 
        """)
    print("Tabela 'suportes' criada com sucesso.")

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS atividades_recentes(
                id_atv_rec INT AUTO_INCREMENT,
                ultima_versao DATE,
                acesso VARCHAR(2),
                id_arquivo INT,
                PRIMARY KEY(id_atv_rec),
                FOREIGN KEY(id_arquivo) REFERENCES arquivos(id_arquivo)
            ); 
        """)
    print("Tabela 'atividades_recentes' criada com sucesso.")


def defineUserLogado(conexao, id_usuario):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        set @usuario_id_logado = %s
        """, (id_usuario,))
        conexao.commit()
    except Error as erro:
        print(f"Erro ao definir usuario logado: {erro}")
        return None
    finally:
        cursor.close()

def exibeMenu():
        print("""
            OPCOES DE LOGIN
            1 - Usuario
            2 - Administrador 
            3 - Se cadastrar como usuario, caso nao tenha conta
            4 - Atualizar senha
            5 - Atualizar email
            0 - Encerrar
                    """)
        resp = int(input("Digite sua resposta: "))
        return resp


def exibeMenuUsuario(conexao):
    login = str(input("Digite seu login: "))
    senha = str(input("Digite sua senha: "))
    usuario = BuscasNoBanco.buscar_usuario(conexao, login, senha)
    if usuario:
        defineUserLogado(conexao, usuario)
        ##view_arquivo_usuario(conexao)
        op = -1
        print("Bem vindo!!!!")
        while op != 0:
            # implementar outras opcoes
            print("""
            Opcoes:
            1 - Inserir arquivo no driver
            2 - Listar apenas MEUS arquivos
            3 - Deletar arquivo do drive
            4 - Listar TODOS os arquivos(Meus e compartilhados)
            5 - Compartilhar arquivo com outro usuario(atraves do email)
            6 - Fazer comentario em arquivo
            7 - Fazer operacoes em arquivos
            0 - Sair
            """)
            op = int(input("Digite sua opcao: "))
            if op == 1:
                insercaoNoBanco.insert_arquivos(conexao, usuario)
                conexao.commit()
            elif op == 2:
                arquivos = buscar_arquivos_usuario(conexao, usuario)
                if arquivos:
                    for arquivo in arquivos:
                        print(f"\nDono:{arquivo[0]}\nNome do arquivo: {arquivo[1]}")
                else:
                    print("Voce nao tem arquivos no drive")
            elif op == 3:
                print("Seus arquivos: ")
                arquivos = buscar_arquivos_usuario(conexao, usuario)
                for arquivo in arquivos:
                    print(f"\nDono:{arquivo[0]}\nNome do arquivo: {arquivo[1]}")
                nomeRemover = str(input("Digite o nome do arquivo que voce deseja remover: "))
                RemocaoNoBanco.removeArquivo(conexao, nomeRemover)
                print("Remocao concluida!!!")
                conexao.commit()
            elif op == 4:
                arquivos = buscar_arquivos_proprios_compartilhados(conexao, usuario)
                if arquivos:
                    print("Arquivos compartilhados e seus: \n")
                    for arquivo in arquivos:
                        print(f"Arquivo: {arquivo[0]}\n")
                else:
                    print("Voce nao possui nenhum arquivo no drive! ")
            elif op == 5:
                insert_compartilhamentos(conexao,usuario)
            elif op == 6:
                pass
            elif op == 7:
                print("Seus arquivos: ")
                arquivos = buscar_arquivos_usuario(conexao, usuario)
                for arquivo in arquivos:
                    print(f"\nDono:{arquivo[0]}\nNome do arquivo: {arquivo[1]}")
                arquivo = str(input("Digite o nome do arquivo que voce deseja operar: "))
                id_arquivo_achado = buscar_arquivoPor_nome(conexao, arquivo)
                if id_arquivo_achado:
                    print("""\n
                    1 - Carregar
                    2 - Remover 
                    3 - Atualizar nome do arquivo
                    \n
                    """)
                    tipo_operacao = int(input("Especifique o tipo de operacao que voce deseja fazer: "))
                    if tipo_operacao == 1:
                        operacao = "carregar"
                        pass
                    elif tipo_operacao == 2:
                        operacao = "remover"
                        date_op = datetime.now().date()
                        hora_op = datetime.now().time()
                        insert_operacoes(conexao, date_op, hora_op, operacao, usuario)
                        remove_arquivo_por_id(conexao, id_arquivo_achado)
                    else:
                        operacao = "atualizar"
                        ##implementar







        #implementar outras opcoes
    else:
        print("Usuario nao cadastrado no banco")

def setAdmRole(conexao):
    pass
##implementar


def exibe_menu_adm(conexao):
    login = str(input("Digite seu login: "))
    senha = str(input("Digite sua senha: "))
    adm = BuscasNoBanco.buscar_adm(conexao, login, senha)
    if adm:
        op = -1
        print("Bem vindo!!!")
        while(op != 0):
            print("""
            1 - Inserir planos
            2 - Inserir instituição 
            3 - Inserir usuario no banco de dados
            4 - Inserir arquivo associado a um usuario
            0 - Sair
            """)
            op = int(input("Digite sua opção: "))
            if op == 1:
                insercaoNoBanco.insert_planos(conexao)
            elif op == 2:

                insercaoNoBanco.insert_instituicao(conexao)
            elif op == 3:
                insercaoNoBanco.inserir_usuario(conexao)
            elif op == 4:
                pass
    else:
        print("Esse adm não existe no banco de dados")


def atualizar(cursor, novoValor, chave, tabela, coluna):
    query = f"""
    UPDATE {tabela} 
    SET {coluna} = %s
    WHERE email = %s
    """
    cursor.execute(query, (novoValor, chave))



def main():
    conexao = criar_conexao()
    if conexao:
        try:
            cursor = conexao.cursor()
            criar_banco_de_dados(cursor)
            criar_tabelas(cursor)
            CriacaoDeViews.view_administradores(conexao)
            ##CriacaoDeRoles.cria_role_PapelAdm(conexao)

            ##verificar_atividades(conexao)
            cursor.callproc("verificar_atividades")
            conexao.commit()
            for result in cursor.stored_results():
                print(result.fetchall())

            ##conta_usuario(conexao)
            total_usuarios = 0
            total_usuarios = cursor.callproc("ContaUsuarios", [2,total_usuarios])
            print(f"Total de usuarios: {total_usuarios[1]}")

            ##chavear_arquivo(conexao)
            #cursor.callproc("chavear_arquivo", [1])
            #conexao.commit()

            ##remover_acessos(conexao)
            #cursor.callproc("remover_acessos", [2])
            #conexao.commit()

            resp = -1
            while (resp != 0):
                resp = exibeMenu()
                if resp == 1:
                    exibeMenuUsuario(conexao)
                elif resp == 2:
                    exibe_menu_adm(conexao)
                elif resp == 4:
                    #ajeitar verificacoes a mais
                    email = str(input("Digite seu email: "))
                    senha = str(input("Digite a sua senha: "))
                    senhaConfirma = str(input("Repita a nova senha: "))
                    if senha == senhaConfirma:
                        atualizar(cursor, senhaConfirma, email, tabela="usuarios", coluna="senha")
                        conexao.commit()
                        print("Senha atualizada!")
                    else:
                        print("Nao foi possivel atualizar, as senhas nao coincidem")
                elif resp == 5:
                    print("teste")
            print("Encerrando aplicacao...")
        except Error as erro:
            print(f"Erro ao criar banco de dados ou tabelas: {erro}")
        finally:
            cursor.close()
            conexao.close()
            print("Conexão encerrada.")

if __name__ == "__main__":
    main()
