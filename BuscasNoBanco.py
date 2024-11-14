import mysql.connector
from mysql.connector import Error

def buscar_usuario(conexao, login, senha):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT * FROM usuarios WHERE login = %s AND senha = %s
        """, (login, senha))
        usuario = cursor.fetchone()
        if usuario:
            return usuario[0] #retorno de id do usuario
        else:
            return None
    except Error as erro:
        print(f"Erro ao buscar usuário: {erro}")
        return None
    finally:
        cursor.close()

def buscar_arquivos_usuario(conexao, id_usuario):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT usuarios.email, arquivos.nome FROM usuarios 
        INNER JOIN arquivos ON usuarios.id_usuario = arquivos.id_usuario
        WHERE usuarios.id_usuario = %s; 
        """, (id_usuario,))
        arquivosEncontrados = cursor.fetchall()
        if arquivosEncontrados:
            return arquivosEncontrados
        else:
            return None
    except Error as erro:
        print(f"Erro ao buscar arquivo: {erro}")
        return None
    finally:
        cursor.close()


def buscar_arquivos_usuario_view(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT * FROM arquivos_usuario
        """)
        resultados = cursor.fetchall()
        if resultados:
            for linha in resultados:
                print(linha)
        else:
            print("Você não possui arquivos no drive! ")
    except Error as erro:
        print(f"Erro ao buscar view: {erro}")
    finally:
        cursor.close()


def buscar_arquivos_proprios_compartilhados(conexao, id_usuario):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT DISTINCT a.nome
        FROM arquivos a
        LEFT JOIN compartilhamentos c ON c.id_arquivo = a.id_arquivo
        WHERE a.id_usuario = %s OR c.id_usuario_compartilhado = %s;
        """, (id_usuario, id_usuario))
        busca = cursor.fetchall()
        if busca:
            return busca
        else:
            return None
    except Error as erro:
        print(f"Erro ao buscar todos os arquivos do usuário: {erro}")
        return None
    finally:
        cursor.close()


def buscar_usuario_email(conexao, email):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT * FROM usuarios 
        WHERE email = %s
        """, (email,))
        usuario = cursor.fetchone()
        if usuario:
            return usuario[0]##retorno id do usuario
        else:
            return None
    except Error as erro:
        print(f"Não foi possível buscar o usuário pelo email: {erro}")
        return None
    finally:
        cursor.close()



def buscar_adm(conexao, login, senha):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT * FROM administradores WHERE login = %s AND senha = %s
        """, (login, senha))
        adm = cursor.fetchone()
        if adm:
            return adm[0]
        else:
            return None
    except Error as erro:
        print(f"Não foi possível buscar o administrador: {erro}")
        return None
    finally:
        cursor.close()




def buscar_arquivoPor_nome(conexao, nome):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT * FROM arquivos
        WHERE nome = %s
        """, (nome,))
        arquivo = cursor.fetchone()
        if arquivo:
            return arquivo[0]
        else:
            return None
    except Error as erro:
        print(f"Não foi possível buscar o arquivo pelo nome: {erro}")
        return None
    finally:
        cursor.close()

def buscar_instituicao_por_nome(conexao, nome_instituicao):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT id_instituicao FROM instituicoes 
        WHERE nome = %s
        """, (nome_instituicao,))
        instituicao = cursor.fetchone()
        return instituicao[0] if instituicao else None
    except Error as erro:
        print(f"Erro ao buscar instituição: {erro}")
        return None
    finally:
        cursor.close()

def buscar_plano_por_nome(conexao, nome_plano):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT id FROM planos 
        WHERE nome = %s
        """, (nome_plano,))
        plano = cursor.fetchone()
        return plano[0] if plano else None
    except Error as erro:
        print(f"Erro ao buscar plano: {erro}")
        return None
    finally:
        cursor.close()

def buscar_adm_por_email(conexao, email):
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT id_adm FROM administradores WHERE email = %s", (email,))
        administrador = cursor.fetchone()
        return administrador[0] if administrador else None
    except Error as erro:
        print(f"Erro ao buscar administrador: {erro}")
        return None
    finally:
        cursor.close()


def buscar_comentarios_arquivo(conexao, id_arquivo):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT c.conteudo, c.data_comentario FROM
        comentarios c WHERE c.id_arquivo = %s 
        """, (id_arquivo,))
        comentarios = cursor.fetchall()
        if comentarios:
            return comentarios
        else:
            print("Sem comentários nesse arquivo! \n")
    except Error as erro:
        print(f"Erro ao buscar comentário: {erro}")
        return None
    finally:
        cursor.close()


def busca_atv_recentes(conexao, id_arquivo):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT * FROM atividades_recentes WHERE id_arquivo = %s
        """, (id_arquivo,))
        atv_recente = cursor.fetchone()
        if atv_recente:
            return atv_recente
        else:
            return None
    except Error as erro:
        print(f"Erro ao buscar atividade recente: {erro}")
        return None
    finally:
        cursor.close()

def busca_adm_por_id(conexao, id_adm):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT * FROM administradores 
        WHERE id_adm = %s
        """, (id_adm,))
        adm = cursor.fetchall()
        if adm:
            return adm
        else:
            return None
    except Error as erro:
        print(f"Erro ao buscar adm pelo id: {erro}")
        return None
    finally:
        cursor.close()