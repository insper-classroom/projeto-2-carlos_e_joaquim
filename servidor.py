from flask import Flask, request
from utils import *
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
    faltando = []
    for campo in CAMPOS_OBRIGATORIOS:
        valor = payload.get(campo)
        if valor is None:
            faltando.append(campo)
            continue
        if isinstance(valor, str) and not valor.strip():
            faltando.append(campo)

    if faltando:
        return False, {"erro": f"Campos obrigatorios: {', '.join(CAMPOS_OBRIGATORIOS)}"}, 400
    return True, None, None

@app.route("/")
def home():
    return "Bem-vindo à API de Imóveis!", 200

@app.route("/imoveis", methods=["GET"])
def listar_imoveis():
    tipo = request.args.get("tipo")
    cidade = request.args.get("cidade")

    if tipo:
        imoveis = load_data_by_type(tipo)
    elif cidade:
        imoveis = load_data_by_city(cidade)
    else:
        imoveis = load_data()

    return resposta_colecao_com_links(imoveis, tipo=tipo, cidade=cidade), 200

@app.route("/imoveis", methods=["POST"])
def adicionar_imovel():
    payload = request.get_json(silent=True) or {}
    valido, erro, status = validar_campos(payload)
    if not valido:
        return erro, status

    novo_id = add_data(payload)

    return {
        "id": novo_id,
        "_links": montar_links("criacao", imovel_id=novo_id),
    }, 201

@app.route("/imoveis/<int:id>", methods=["GET"])
def listar_imoveis_pelo_id(id):
    imovel = load_data_by_id(id)
    if imovel is None:
        return {"erro": "Imovel nao encontrado"}, 404
    return serializar_imovel_com_links(imovel), 200

@app.route("/imoveis/<int:id>", methods=["PUT"])
def atualizar_imovel(id):
    payload = request.get_json(silent=True) or {}
    valido, erro, status = validar_campos(payload)
    if not valido:
        return erro, status

    atualizado = update_data(id, payload)

    if not atualizado:
        return {"erro": "Imovel nao encontrado"}, 404

    return {
        "mensagem": "Imovel atualizado com sucesso",
        "_links": montar_links("atualizacao", imovel_id=id),
    }, 200

@app.route("/imoveis/<int:id>", methods=["DELETE"])
def deletar_imovel(id):
    deletado = delete_data(id)

    if not deletado:
        return {"erro": "Imovel nao encontrado"}, 404

    return {
        "mensagem": "Imovel excluído com sucesso",
        "_links": montar_links("pos_exclusao"),
    }, 200

if __name__ == "__main__":
    app.run(debug=True)