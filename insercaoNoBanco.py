from datetime import datetime
import mysql.connector
from mysql.connector import Error

from BuscasNoBanco import buscar_arquivos_usuario, buscar_usuario_email, buscar_arquivoPor_nome


def insert_arquivos(conexao, id_usuario):
    try:
        cursor = conexao.cursor()
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
    except Error as erro:
        print(f"Erro ao inserir arquivo: {erro}")
        return None
    finally:
        cursor.close()   
        
def insert_planos(conexao):
    try:
        cursor = conexao.cursor()
        nome = input("Digite o nome do plano: ")
        duracao = int(input("Digite a duração do plano (em meses): "))
        data_aquisicao = input("Digite a data de aquisição (AAAA-MM-DD): ")
        espaco_por_usuario = float(input("Digite o espaço por usuário (em GB): "))
        cursor.execute("""
        INSERT INTO planos(nome, duracao, data_aquisicao, espaco_por_usuario) 
        VALUES (%s, %s, %s, %s);
        """, (nome, duracao, data_aquisicao, espaco_por_usuario))
        conexao.commit()
        print("Plano inserido com sucesso!")
    except Error as erro:
        print(f"Erro ao inserir plano: {erro}")
    finally:
        cursor.close()
        
def insert_instituicoes(conexao):
    try:
        cursor = conexao.cursor()
        nome = input("Digite o nome da instituição: ")
        endereco = input("Digite o endereço da instituição: ")
        causa_social = input("Digite a causa social da instituição: ")
        id_plano = int(input("Digite o ID do plano ao qual a instituição está atrelada: "))

        cursor.execute("""
        INSERT INTO instituicoes(nome, endereco, causa_social, id_plano) 
        VALUES (%s, %s, %s, %s);
        """, (nome, endereco, causa_social, id_plano))

        print("Instituição inserida com sucesso!")
    except Error as erro:
        print(f"Erro ao inserir instituição: {erro}")
    finally:
        cursor.close()

def insert_usuarios(conexao):
    try:
        cursor = conexao.cursor()
        email = input("Digite o email do usuário: ")
        senha = input("Digite a senha do usuário: ")
        login = input("Digite o login do usuário: ")
        data_ingresso = input("Digite a data de ingresso (AAAA-MM-DD): ")
        id_instituicao = int(input("Digite o ID da instituição à qual o usuário está atrelado: "))

        cursor.execute("""
        INSERT INTO usuarios(email, senha, login, data_ingresso, id_instituicao) 
        VALUES (%s, %s, %s, %s, %s);
        """, (email, senha, login, data_ingresso, id_instituicao))

        print("Usuário inserido com sucesso!")
    except Error as erro:
        print(f"Erro ao inserir usuário: {erro}")
    finally:
        cursor.close()

def insert_comentarios(conexao):
    try:
        cursor = conexao.cursor()
        conteudo = input("Digite o conteúdo do comentário: ")
        data_comentario = input("Digite a data do comentário (AAAA-MM-DD): ")
        hora_comentario = input("Digite a hora do comentário (HH:MM:SS): ")
        id_usuario = int(input("Digite o ID do usuário que está comentando: "))
        id_arquivo = int(input("Digite o ID do arquivo ao qual o comentário está atrelado: "))

        cursor.execute("""
        INSERT INTO comentarios(conteudo, data_comentario, hora_comentario, id_usuario, id_arquivo) 
        VALUES (%s, %s, %s, %s, %s);
        """, (conteudo, data_comentario, hora_comentario, id_usuario, id_arquivo))

        print("Comentário inserido com sucesso!")
    except Error as erro:
        print(f"Erro ao inserir comentário: {erro}")
    finally:
        cursor.close()

def insert_historico_versionamento(conexao):
    try:
        cursor = conexao.cursor()
        data_historico = input("Digite a data do histórico (AAAA-MM-DD): ")
        hora_historico = input("Digite a hora do histórico (HH:MM:SS): ")
        operacao_historico = input("Digite a operação realizada (ex: 'edição', 'exclusão'): ")
        id_usuario_alterou = int(input("Digite o ID do usuário que realizou a alteração: "))
        conteudo_mudado = input("Digite o conteúdo que foi alterado: ")
        id_arquivo = int(input("Digite o ID do arquivo ao qual o histórico está atrelado: "))

        cursor.execute("""
        INSERT INTO historico_versionamento(data_historico, hora_historico, operacao_historico, 
                                            id_usuario_alterou, conteudo_mudado, id_arquivo) 
        VALUES (%s, %s, %s, %s, %s, %s);
        """, (data_historico, hora_historico, operacao_historico, id_usuario_alterou, conteudo_mudado, id_arquivo))

        print("Histórico de versionamento inserido com sucesso!")
    except Error as erro:
        print(f"Erro ao inserir histórico de versionamento: {erro}")
    finally:
        cursor.close()

def insert_operacoes(conexao):
    try:
        cursor = conexao.cursor()
        data_op = input("Digite a data da operação (AAAA-MM-DD): ")
        hora_op = input("Digite a hora da operação (HH:MM:SS): ")
        tipo_operacao = input("Digite o tipo de operação realizada (ex: 'upload', 'download', 'exclusão'): ")
        id_usuario = int(input("Digite o ID do usuário que realizou a operação: "))
        id_arquivo = int(input("Digite o ID do arquivo ao qual a operação está relacionada: "))

        cursor.execute("""
        INSERT INTO operacoes(data_op, hora_op, tipo_operacao, id_usuario, id_arquivo) 
        VALUES (%s, %s, %s, %s, %s);
        """, (data_op, hora_op, tipo_operacao, id_usuario, id_arquivo))

        print("Operação inserida com sucesso!")
    except Error as erro:
        print(f"Erro ao inserir operação: {erro}")
    finally:
        cursor.close()

def insert_compartilhamentos(conexao, id_usuario_dono):
    try:
        cursor = conexao.cursor()
        email = str(input("Digita o email do usuario que voce quer compartilhar um arquivo: "))
        id_usuario_compartilhado = buscar_usuario_email(conexao, email)
        if id_usuario_compartilhado:
            arquivos = buscar_arquivos_usuario(conexao, id_usuario_dono)
            for arquivo in arquivos:
                print(f"\nDono:{arquivo[0]}\nNome do arquivo: {arquivo[1]}")
            nomeArquivo = str(input("Digite o nome do arquivo que voce ira compartilhar: "))
            id_arquivo = buscar_arquivoPor_nome(conexao, nomeArquivo)
            if id_arquivo:
                data_compartilhado = datetime.now().date()
                cursor.execute("""
                        INSERT INTO compartilhamentos(id_usuario_dono, id_usuario_compartilhado, id_arquivo, data_compartilhado) 
                        VALUES (%s, %s, %s, %s);
                        """, (id_usuario_dono, id_usuario_compartilhado, id_arquivo, data_compartilhado))
                conexao.commit()
                print("Compartilhamento inserido com sucesso!")
            else:
                print("\nErro! Arquivo nao existe no banco de dados.")
        else:
            print("\nUsuario nao existe no banco, tente outro email! ")
    except Error as erro:
        print(f"Erro ao inserir compartilhamento: {erro}")
    finally:
        cursor.close()

def insert_administradores(conexao):
    try:
        cursor = conexao.cursor()
        email = input("Digite o email do administrador: ")
        senha = input("Digite a senha do administrador: ")
        login = input("Digite o login do administrador: ")
        data_ingresso = input("Digite a data de ingresso (AAAA-MM-DD): ")
        cursor.execute("""
        INSERT INTO administradores(email, senha, login, data_ingresso) 
        VALUES (%s, %s, %s, %s);
        """, (email, senha, login, data_ingresso))
        print("Administrador inserido com sucesso!")
    except Error as erro:
        print(f"Erro ao inserir administrador: {erro}")
    finally:
        cursor.close()

def insert_suportes(conexao):
    try:
        cursor = conexao.cursor()
        dia = input("Digite a data do suporte (AAAA-MM-DD): ")
        hora = input("Digite a hora do suporte (HH:MM:SS): ")
        descricao = input("Digite a descrição do suporte: ")
        id_adm = int(input("Digite o ID do administrador responsável pelo suporte: "))

        cursor.execute("""
        INSERT INTO suportes(dia, hora, descricao, id_adm) 
        VALUES (%s, %s, %s, %s);
        """, (dia, hora, descricao, id_adm))

        print("Suporte inserido com sucesso!")
    except Error as erro:
        print(f"Erro ao inserir suporte: {erro}")
    finally:
        cursor.close()