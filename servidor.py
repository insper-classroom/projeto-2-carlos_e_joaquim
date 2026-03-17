from flask import Flask
from utils import load_data, load_db, init_db, load_data_by_id
app = Flask(__name__)

init_db()

@app.route("/listar-imoveis")
def listar_imoveis():
    imoveis = load_data()
    return imoveis

@app.route("/listar-imoveis/<int:id>")
def listar_imoveis_pelo_id(id):
    imovel = load_data_by_id(id)
    return imovel



if __name__ == "__main__":
    app.run(debug=True)