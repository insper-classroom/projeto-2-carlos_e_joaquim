import os
import mysql.connector
from flask import url_for


def montar_links(contexto, imovel_id=None, tipo=None, cidade=None):
    if contexto == "colecao":
        links = {
            "self": {"href": url_for("listar_imoveis")},
            "create": {"href": url_for("adicionar_imovel")},
        }
        if tipo:
            links["filtrar_por_tipo"] = {"href": f"{url_for('listar_imoveis')}?tipo={tipo}"}
        if cidade:
            links["filtrar_por_cidade"] = {"href": f"{url_for('listar_imoveis')}?cidade={cidade}"}
        return links

    if contexto == "item":
        return {
            "self": {"href": url_for("listar_imoveis_pelo_id", id=imovel_id)},
            "update": {"href": url_for("atualizar_imovel", id=imovel_id)},
            "delete": {"href": url_for("deletar_imovel", id=imovel_id)},
            "collection": {"href": url_for("listar_imoveis")},
        }

    if contexto == "criacao":
        return {
            "self": {"href": url_for("listar_imoveis_pelo_id", id=imovel_id)},
            "collection": {"href": url_for("listar_imoveis")},
        }

    if contexto == "atualizacao":
        return {
            "self": {"href": url_for("listar_imoveis_pelo_id", id=imovel_id)},
            "delete": {"href": url_for("deletar_imovel", id=imovel_id)},
            "collection": {"href": url_for("listar_imoveis")},
        }

    if contexto == "pos_exclusao":
        return {
            "collection": {"href": url_for("listar_imoveis")},
            "create": {"href": url_for("adicionar_imovel")},
        }

    raise ValueError(f"Contexto de links invalido: {contexto}")


def serializar_imovel_com_links(imovel):
    imovel_id = imovel["id"]
    item = dict(imovel)
    item["_links"] = montar_links("item", imovel_id=imovel_id)
    return item


def resposta_colecao_com_links(imoveis, tipo=None, cidade=None):
    return {
        "dados": [serializar_imovel_com_links(imovel) for imovel in imoveis],
        "_links": montar_links("colecao", tipo=tipo, cidade=cidade),
    }

def load_db():
    conn=mysql.connector.connect(
        host=os.getenv('host'),
        port=os.getenv('port'),
        user=os.getenv('user'),
        password=os.getenv('password'),
        database=os.getenv('database'),
        ssl_ca=os.getenv('ssl_ca')
    )
    return conn

def load_data():
    conn=load_db()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM imoveis")
    imoveis=cursor.fetchall()
    cursor.close()
    conn.close()
    return imoveis

def load_data_by_id(id):
    conn=load_db()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM imoveis WHERE id = %s", (id,))
    imovel=cursor.fetchone()
    cursor.close()
    conn.close()
    return imovel

def add_data(imovel):
    conn=load_db()
    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (imovel["logradouro"], imovel["tipo_logradouro"], imovel["bairro"], imovel["cidade"], imovel["cep"], imovel["tipo"], imovel["valor"], imovel["data_aquisicao"])
    )
    conn.commit()
    novo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return novo_id

def update_data(id, imovel):
    conn=load_db()
    cursor=conn.cursor()
    cursor.execute(
        "UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s",
        (imovel["logradouro"], imovel["tipo_logradouro"], imovel["bairro"], imovel["cidade"], imovel["cep"], imovel["tipo"], imovel["valor"], imovel["data_aquisicao"], id)
    )
    conn.commit()
    updated = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return updated

def delete_data(id):
    conn=load_db()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM imoveis WHERE id = %s", (id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return deleted

def load_data_by_type(tipo):
    conn=load_db()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM imoveis WHERE tipo = %s", (tipo,))
    imoveis=cursor.fetchall()
    cursor.close()
    conn.close()
    return imoveis

def load_data_by_city(cidade):
    conn=load_db()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM imoveis WHERE cidade = %s", (cidade,))
    imoveis=cursor.fetchall()
    cursor.close()
    conn.close()
    return imoveis