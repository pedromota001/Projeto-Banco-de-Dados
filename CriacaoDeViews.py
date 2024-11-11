import mysql.connector
from mysql.connector import Error

def view_arquivo_usuario(conexao, id_usuario):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        CREATE OR REPLACE VIEW arquivos_usuario AS
        SELECT
        a.nome, a.tipo, a.tam, a.data_ult_modificacao
        FROM arquivos a
        INNER JOIN compartilhamentos c ON c.id_arquivo = a.id_arquivo
        WHERE id_usuario_dono = @id_usuario_logado OR id_usuario_compartilhado = @id_usuario_logado
        """)
        conexao.commit()
        print(" A view: 'view_arquivo_usuario' foi criada com sucesso!")
    except Error as erro:
        print(f"Não foi possível criar view: {erro}")
        return None
    finally:
        cursor.close()

def view_administradores(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE OR REPLACE VIEW view_administradores As 
            SELECT
                u.email, u.login, u.data_ingresso,
                i.nome AS nome_instituicao, i.endereco, i.causa_social,
                p.nome AS nome_plano, p.duracao, p.espaco_por_usuario,
                a.nome AS nome_arquivo, a.tipo, a.url, a.tam, a.data_ult_modificacao,
                c.conteudo AS comentario, c.data_comentario, c.hora_comentario,
                o.tipo_operacao, o.data_op, o.hora_op,
                h.operacao_historico, h.data_historico, h.hora_historico
            FROM 
                usuarios u
            JOIN 
                instituicoes i ON u.id_instituicao = i.id_instituicao
            JOIN 
                planos p ON i.id_plano = p.id
            LEFT JOIN 
                arquivos a ON a.id_usuario = u.id_usuario
            LEFT JOIN 
                comentarios c ON c.id_usuario = u.id_usuario
            LEFT JOIN 
                operacoes o ON o.id_usuario = u.id_usuario
            LEFT JOIN 
                historico_versionamento h ON h.id_arquivo = a.id_arquivo;
        """)
        conexao.commit()
        print(" A view: 'view_administradores' foi criada com sucesso!")
    except Error as erro:
        print(f"Não foi possível criar a view: {erro}")
    finally:
        cursor.close()

def view_historico_usuario(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("""
        CREATE OR REPLACE VIEW historico_usuario AS
        SELECT
        o.data_op,
        o.hora_op,
        o.tipo_operecao
        FROM operacoes o
        INNER JOIN usuarios u ON o.id_usuario = u.id_usuario
        WHERE o.id_usuario = @id_usuario_logado;                                                                                                                                      
        """)
        cursor.execute("GRANT SELECT ON historico_operacoes_usuario TO usuario_logado;")
        conexao.commit()
        print(" A view: 'view_historico_usuario' foi criada com sucesso!")
    except Error as erro:
        print(f"Não foi possivel criar view: {erro}")
        return None
    finally:
        cursor.close()