from datetime import datetime

import mysql.connector
from mysql.connector import Error

import random
import BuscasNoBanco
import CriacaoDeRoles
import CriacaoDeViews
import RemocaoNoBanco
import insercaoNoBanco
from BuscasNoBanco import buscar_arquivos_usuario, buscar_usuario_email, buscar_arquivoPor_nome, \
    buscar_arquivos_proprios_compartilhados, buscar_comentarios_arquivo, busca_atv_recentes
from RemocaoNoBanco import remove_arquivo_por_id, remocao_historico_versionamento
from Triggers import safe_security, registrar_operacao
from insercaoNoBanco import insert_compartilhamentos, insert_operacoes, insert_comentarios, \
    insert_historico_versionamento, insert_atv_recentes, insert_suportes, insert_adm_usuarios
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


def exibeMenu():
        print("""
            OPÇÕES DE LOGIN
            1 - Usuário
            2 - Administrador 
            3 - Se cadastrar como usuário, caso não tenha conta
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
        op = -1
        print("Bem vindo!!!!")
        while op != 0:
            # implementar outras opcoes
            print("""
            Opcoes:
            1 - Inserir arquivo no driver
            2 - Listar apenas MEUS arquivos
            3 - Deletar arquivo do drive
            4 - Listar TODOS os arquivos (Meus e compartilhados)
            5 - Compartilhar arquivo com outro usuário (através do email)
            6 - Fazer comentário em arquivo
            7 - Fazer operações em arquivos
            8 - Listar comentário de arquivo
            9 - Pedir suporte a adm
            0 - Sair
            """)
            op = int(input("Digite sua opção: "))
            if op == 1:
                insercaoNoBanco.insert_arquivos(conexao, usuario)
                operacao = "criação"
                date_op = datetime.now().date()
                hora_op = datetime.now().time()
                insert_operacoes(conexao,date_op, hora_op, operacao, usuario)
                conexao.commit()
            elif op == 2:
                arquivos = buscar_arquivos_usuario(conexao, usuario)
                if arquivos:
                    for arquivo in arquivos:
                        print(f"\nDono:{arquivo[0]}\nNome do arquivo: {arquivo[1]}")
                else:
                    print("Voce não tem arquivos no drive")
            elif op == 3:
                print("Seus arquivos: ")
                arquivos = buscar_arquivos_usuario(conexao, usuario)
                for arquivo in arquivos:
                    print(f"\nDono:{arquivo[0]}\nNome do arquivo: {arquivo[1]}")
                nomeRemover = str(input("Digite o nome do arquivo que voce deseja remover: "))
                id_arquivo = buscar_arquivoPor_nome(conexao, nomeRemover)
                if id_arquivo:
                    operacao = "remover"
                    date_op = datetime.now().date()
                    hora_op = datetime.now().time()
                    insert_operacoes(conexao, date_op, hora_op, operacao, usuario)
                    remocao_historico_versionamento(conexao, id_arquivo)
                    remove_arquivo_por_id(conexao, id_arquivo)
                else:
                    print("Arquivo não existe no banco!\n")
            elif op == 4:
                arquivos = buscar_arquivos_proprios_compartilhados(conexao, usuario)
                if arquivos:
                    print("Arquivos compartilhados e seus: \n")
                    for arquivo in arquivos:
                        print(f"Arquivo: {arquivo[0]}\n")
                else:
                    print("Você não possui nenhum arquivo no drive! ")
            elif op == 5:
                insert_compartilhamentos(conexao,usuario)
            elif op == 6:
                arquivos = buscar_arquivos_proprios_compartilhados(conexao, usuario)
                if arquivos:
                    print("Arquivos que você pode comentar: ")
                    for arquivo in arquivos:
                        print(f"Arquivo: {arquivo[0]}\n")
                    arquivo_comentario = str(input("Digite o arquivo que voce deseja comentar: "))
                    insert_comentarios(conexao, arquivo_comentario, usuario)
                else:
                    print("Voce nao pode comentar em nenhum arquivo! \n")
            elif op == 7:
                print("Seus arquivos: ")
                arquivos = buscar_arquivos_usuario(conexao, usuario)
                for arquivo in arquivos:
                    print(f"\nDono:{arquivo[0]}\nNome do arquivo: {arquivo[1]}")
                arquivo = str(input("Digite o nome do arquivo que voce deseja operar: "))
                id_arquivo_achado = buscar_arquivoPor_nome(conexao, arquivo)
                if id_arquivo_achado:
                    print("""\n
                    1 - Carregar/ ?
                    2 - Atualizar arquivo
                    0 - Sair
                    \n
                    """)
                    tipo_operacao = int(input("Especifique o tipo de operação que você deseja fazer: "))
                    if tipo_operacao == 1:
                        operacao = "carregar"
                        insert_historico_versionamento(conexao, id_arquivo_achado, usuario, operacao)
                        atividade_existe = busca_atv_recentes(conexao, id_arquivo_achado)
                        if atividade_existe:
                            continue
                        else:
                            insert_atv_recentes(conexao, id_arquivo_achado)
                        conexao.commit()
                        pass
                    elif tipo_operacao == 2:
                        operacao = "Atualização"
                        print("""
                        1 - Atualizar nome
                        2 - Atualizar permissão 
                        3 - Atualizar url
                        """)
                        op = int(input("Digite sua opção: \n"))
                        if op == 1:
                            novo_nome = str(input("Digite o novo nome: "))
                            atualizar_arquivo(conexao.cursor(), novo_nome, id_arquivo_achado, coluna="nome")
                            insert_historico_versionamento(conexao,id_arquivo_achado, usuario, operacao)
                            atividade_existe = busca_atv_recentes(conexao, id_arquivo_achado)
                            if atividade_existe:
                                continue
                            else:
                                insert_atv_recentes(conexao, id_arquivo_achado)
                            conexao.commit()
                        elif op == 2:
                            nova_permissao = int(input("Digite a nova permissão (Permissão total(1) ou somente de visualização(0) do arquivo: "))
                            atualizar_arquivo(conexao.cursor(), nova_permissao, id_arquivo_achado, coluna="permissão")
                            insert_historico_versionamento(conexao, id_arquivo_achado, usuario, operacao)
                            atividade_existe = busca_atv_recentes(conexao, id_arquivo_achado)
                            if atividade_existe:
                                continue
                            else:
                                insert_atv_recentes(conexao, id_arquivo_achado)
                            conexao.commit()
                        else:
                            novo_url = str(input("Digite o novo url: "))
                            atualizar_arquivo(conexao.cursor(), novo_url, id_arquivo_achado, coluna="url")
                            insert_historico_versionamento(conexao, id_arquivo_achado, usuario, operacao)
                            atividade_existe = busca_atv_recentes(conexao, id_arquivo_achado)
                            if atividade_existe:
                                continue
                            else:
                                insert_atv_recentes(conexao, id_arquivo_achado)
                            conexao.commit()
                    else:
                        return
            elif op == 8:
                arquivos = buscar_arquivos_proprios_compartilhados(conexao, usuario)
                if arquivos:
                    print("Arquivos que voce pode visualizar comentários: ")
                    for arquivo in arquivos:
                        print(f"Arquivo: {arquivo[0]}\n")
                    arquivo_comentario = str(input("Digite o nome do arquivo que você deseja visualizar os comentários: "))
                    id_arquivo = buscar_arquivoPor_nome(conexao, arquivo_comentario)
                    if id_arquivo:
                        comentarios = buscar_comentarios_arquivo(conexao, id_arquivo)
                        for comentario in comentarios:
                            print(f"\nComentário: {comentario[0]}"
                                  f"\nData do comentário: {comentario[1]}\n")
                    else:
                        print("Arquivo não existe no banco!")
            elif op == 9:
                cursor = conexao.cursor()
                id_adm = random.randint(1,3)
                insert_suportes(conexao, id_adm)
                insert_adm_usuarios(conexao, id_adm, usuario)
                print("Encaminhando voce ao suporte com um administrador...")
                


    else:
        print("Usuário não cadastrado no banco")

def exibe_menu_adm(conexao):
    cursor = conexao.cursor()
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
            3 - Inserir usuário no banco de dados
            4 - Inserir arquivo associado a um usuário
            5 - Atualizar toda a tabela de atividades recentes com a data atual
            6 - Contar quantos usuarios possuem um mesmo arquivo
            7 - NP
            8 - Remover acesso de usuarios sobre um arquivo(Menos o dono)
            9 - Verificar se arquivo foi modificado há muito tempo
            0 - Sair
            """)
            op = int(input("Digite sua opção: "))
            if op == 1:
                insercaoNoBanco.insert_planos(conexao)
            elif op == 2:
                insercaoNoBanco.insert_instituicoes(conexao)
            elif op == 3:
                insercaoNoBanco.insert_usuarios(conexao)
            elif op == 4:
                pass
            elif op == 5:
                cursor.callproc("verificar_atividades")
                conexao.commit()
                for result in cursor.stored_results():
                    print(result.fetchall()[0][0])
            elif op == 6:
                cursor.execute("""
                SELECT DISTINCT nome_arquivo, email
                FROM view_administradores;
                """)
                resultados = cursor.fetchall()
                for busca in resultados:
                    print(f"Dono: {busca[1]}\n"
                          f"Arquivo: {busca[0]}\n")
                nome_arquivo = str(input("Digite o nome do arquivo que voce deseja: "))
                id_arquivo_achado = buscar_arquivoPor_nome(conexao, nome_arquivo)
                if id_arquivo_achado:
                    total_usuarios = 0
                    total_usuarios = cursor.callproc("ContaUsuarios", [id_arquivo_achado,total_usuarios])
                    print(f"Total de usuários: {total_usuarios[1]}")
                else:
                    print("Arquivo nao existe no banco, caro amigo administrador! \n")
            elif op == 7:
                cursor.execute("""
                SELECT DISTINCT nome_arquivo, email
                FROM view_administradores;
                """)
                resultados = cursor.fetchall()
                for busca in resultados:
                    print(f"Dono: {busca[1]}\n"
                          f"Arquivo: {busca[0]}\n")
                nome_arquivo = str(input("Digite o nome do arquivo que voce deseja: "))
                id_arquivo_achado = buscar_arquivoPor_nome(conexao, nome_arquivo)
                if id_arquivo_achado:
                    cursor.callproc("chavear_arquivo", [id_arquivo_achado])
                    conexao.commit()
                    print("Sucesso ao realizar operacao de chavear arquivos! \n")
                else:
                    print("Arquivo nao esta no banco, caro amigo administrador!\n")
            elif op == 8:
                cursor.execute("""
                SELECT DISTINCT nome_arquivo, email
                FROM view_administradores;
                """)
                resultados = cursor.fetchall()
                for busca in resultados:
                    print(f"Dono: {busca[1]}\n"
                          f"Arquivo: {busca[0]}\n")
                nome_arquivo = str(input("Digite o nome do arquivo que voce deseja: "))
                id_arquivo_achado = buscar_arquivoPor_nome(conexao, nome_arquivo)
                if id_arquivo_achado:
                    cursor.callproc("remover_acessos", [id_arquivo_achado])
                    conexao.commit()
                    print("Sucesso ao remover acessos!\n")
                else:
                    print("Arquivo nao esta no banco, caro amigo administrador! \n")
            else:
                cursor.execute("""
                SELECT a.nome_arquivo FROM view_administradores;
                """)
                arquivos = cursor.fetchall()
                print("Arquivos no banco: \n")
                for arquivo in arquivos:
                    print(f"Arquivo: {arquivo}\n")
                nome_arquivo = str(input("Digite o nome do arquivo que voce deseja ver a data"))
                data_ult_modif_arquivo = buscar_arquivoPor_nome(conexao, nome_arquivo)
                if data_ult_modif_arquivo:
                    cursor.execute("""
                    SELECT verificar_arquivo_antigo(%s);
                    """, data_ult_modif_arquivo)
                    resultado = conexao.fetchone()[0]
                    resultado_final = resultado(bool)
                    if resultado_final == True:
                        pass
                        #implementar
                    else:
                        print("Arquivo teve modificao feita em menos de 100 dias! ")



    else:
        print("Esse adm não existe no banco de dados")


def atualizar_usuario(cursor, novoValor, chave, coluna):
    query = f"""
    UPDATE usuarios 
    SET {coluna} = %s
    WHERE id_usuario = %s
    """
    cursor.execute(query, (novoValor, chave))

def atualizar_arquivo(cursor, novo_valor, chave, coluna):
    query = f"""
    UPDATE arquivos 
    SET {coluna} = %s
    WHERE id_arquivo = %s
    """
    cursor.execute(query, (novo_valor, chave))

def main():
    conexao = criar_conexao()
    if conexao:
        try:
            cursor = conexao.cursor()
            criar_banco_de_dados(cursor)
            criar_tabelas(cursor)
            ##safe_security(conexao)
            ##registrar_operacao(conexao)
            ##CriacaoDeViews.view_administradores(conexao)

            ##CriacaoDeRoles.cria_role_PapelAdm(conexao)

            ##verificar_atividades(conexao)
            ##conta_usuario(conexao)
            ##chavear_arquivo(conexao)
            remover_acessos(conexao)


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
                        usuario = buscar_usuario_email(conexao, email)
                        if usuario:
                            atualizar_usuario(cursor, senhaConfirma, usuario, tabela="usuarios", coluna="senha")
                            conexao.commit()
                            print("Senha atualizada!")
                        else:
                            print("Usuário não existe no banco, erro ao alterar senha \n")
                    else:
                        print("Não foi possível atualizar, as senhas não coincidem")
                elif resp == 5:
                    print("teste")
            print("Encerrando aplicação...")
        except Error as erro:
            print(f"Erro ao criar banco de dados ou tabelas: {erro}")
        finally:
            cursor.close()
            conexao.close()
            print("Conexão encerrada.")

if __name__ == "__main__":
    main()
