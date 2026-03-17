from flask import Flask
from utils import load_data, load_templates, load_db, init_db
app = Flask(__name__)

init_db()

@app.route("/")
def listar():
    imoveis = load_data()




    

if __name__ == "__main__":
    app.run(debug=True)