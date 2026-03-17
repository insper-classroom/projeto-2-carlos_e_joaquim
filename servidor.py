from flask import Flask
from utils import load_templates, load_db, init_db
app = Flask(__name__)

init_db()

@app.route("/")
def listar_imoveis():
    pass
    

if __name__ == "__main__":
    app.run(debug=True)