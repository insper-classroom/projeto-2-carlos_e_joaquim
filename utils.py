import os
import mysql.connector

def load_templates(arquivo_html):
    with open(f'static/templates/{arquivo_html}','r') as file:
        template = file.read()
    return template

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
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM imoveis")
    imoveis=cursor.fetchall()
    conn.close()
    return imoveis