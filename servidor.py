from flask import Flask, request
from utils import load_data, add_data, init_db, load_data_by_id, update_data
app = Flask(__name__)

CAMPOS_OBRIGATORIOS = [
    "logradouro",
    "tipo_logradouro",
    "bairro",
    "cidade",
    "cep",
    "tipo",
    "valor",
    "data_aquisicao",
]

def validar_campos(payload):
    """Valida se todos os campos obrigatórios estão presentes."""
    faltando = [campo for campo in CAMPOS_OBRIGATORIOS if campo not in payload]
    if faltando:
        return False, {"erro": f"Campos obrigatorios: {', '.join(CAMPOS_OBRIGATORIOS)}"}, 400
    return True, None, None

init_db()

@app.route("/listar-imoveis")
def listar_imoveis():
    imoveis = load_data()
    return imoveis, 200

@app.route("/listar-imoveis/<int:id>")
def listar_imoveis_pelo_id(id):
    imovel = load_data_by_id(id)
    if imovel is None:
        return {"erro": "Imovel nao encontrado"}, 404
    return imovel, 200

@app.route("/adicionar-imovel", methods=["POST"])
def adicionar_imovel():
    payload = request.get_json(silent=True) or {}
    valido, erro, status = validar_campos(payload)
    if not valido:
        return erro, status

    novo_id = add_data(payload)

    return {"id": novo_id}, 201

@app.route("/listar-imoveis/<int:id>", methods=["PUT"])
def atualizar_imovel(id):
    payload = request.get_json(silent=True) or {}
    valido, erro, status = validar_campos(payload)
    if not valido:
        return erro, status

    atualizado = update_data(id, payload)
    
    if not atualizado:
        return {"erro": "imovel nao encontrado"}, 404

    return {"mensagem": "Imovel atualizado com sucesso"}, 200

if __name__ == "__main__":
    app.run(debug=True)