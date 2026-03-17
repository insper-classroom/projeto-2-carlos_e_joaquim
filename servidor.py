from flask import Flask
from utils import load_data, load_db, init_db
app = Flask(__name__)

init_db()

@app.route("/listar-imoveis")
def listar_imoveis():
    imoveis = load_data()
    return imoveis



if __name__ == "__main__":
    app.run(debug=True)