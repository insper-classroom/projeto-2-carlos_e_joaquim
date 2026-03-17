from flask import Flask, request
from utils import load_data, add_data, init_db, load_data_by_id
app = Flask(__name__)

init_db()

@app.route("/listar-imoveis")
def listar_imoveis():
    imoveis = load_data()
    return imoveis, 200

@app.route("/listar-imoveis/<int:id>")
def listar_imoveis_pelo_id(id):
    imovel = load_data_by_id(id)
    if not imovel:
        return {"erro": "Imovel nao encontrado"}, 404
    return imovel, 200

@app.route("/adicionar-imovel", methods=["POST"])
def adicionar_imovel():
    payload = request.get_json(silent=True) or {}
    campos_obrigatorios = [
        "logradouro",
        "tipo_logradouro",
        "bairro",
        "cidade",
        "cep",
        "tipo",
        "valor",
        "data_aquisicao",
    ]

    faltando = [campo for campo in campos_obrigatorios if campo not in payload]
    if faltando:
        return {"erro": f"Campos obrigatorios: {', '.join(campos_obrigatorios)}"}, 400

    novo_id = add_data(payload)

    return {"id": novo_id}, 201
if __name__ == "__main__":
    app.run(debug=True)