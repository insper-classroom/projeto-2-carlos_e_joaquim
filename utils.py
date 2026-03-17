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
    imovel=cursor.fetchall()
    cursor.close()
    conn.close()
    return imovel