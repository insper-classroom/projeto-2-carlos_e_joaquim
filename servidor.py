from flask import Flask
from utils import load_data, load_templates, load_db, init_db
app = Flask(__name__)

init_db()

@app.route("/listar-imoveis")
def listar_imoveis():
    imoveis = load_data()
    return {"imoveis": [
        {
            "logradouro": imovel[0],
            "tipo_logradouro": imovel[1],
            "bairro": imovel[2],
            "cidade": imovel[3],
            "cep": imovel[4],
            "tipo": imovel[5],
            "valor": imovel[6],
            "data_aquisicao": str(imovel[7])
        }
        for imovel in imoveis
    ]}
if __name__ == "__main__":
    app.run(debug=True)