import os
import mysql.connector

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

def init_db():
    pass

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