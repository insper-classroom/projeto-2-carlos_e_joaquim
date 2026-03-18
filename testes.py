import pytest
from unittest.mock import patch, MagicMock
from servidor import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def assert_links_item(imovel, imovel_id):
    assert imovel["_links"]["self"]["href"] == f"/imoveis/{imovel_id}"
    assert imovel["_links"]["update"]["href"] == f"/imoveis/{imovel_id}"
    assert imovel["_links"]["delete"]["href"] == f"/imoveis/{imovel_id}"
    assert imovel["_links"]["collection"]["href"] == "/imoveis"

def assert_links_collection(payload):
    assert payload["_links"]["self"]["href"] == "/imoveis"
    assert payload["_links"]["create"]["href"] == "/imoveis"

@patch("utils.load_db")
def test_listar_imoveis_com_dados(mock_load_db, client):
    """GET /imoveis - lista com dados e links HATEOAS."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [{"id": 1, "logradouro": "John Falls", "tipo_logradouro": "Rua", "bairro": "Port Carol", "cidade": "Knappview", "cep": "14150", "tipo": "casa", "valor": 961722.89, "data_aquisicao": "2022-01-05"}, {"id": 2, "logradouro": "Jane Doe", "tipo_logradouro": "Avenida", "bairro": "Centro", "cidade": "Sao Paulo", "cep": "01310-100", "tipo": "apartamento", "valor": 500000.00, "data_aquisicao": "2022-01-06"}]

    mock_load_db.return_value = mock_conn

    response = client.get("/imoveis")
    body = response.get_json()

    assert response.status_code == 200
    assert "dados" in body
    assert [imovel["id"] for imovel in body["dados"]] == [1, 2]
    assert body["dados"][0]["id"] == 1
    assert body["dados"][1]["id"] == 2
    assert_links_item(body["dados"][0], 1)
    assert_links_item(body["dados"][1], 2)
    assert_links_collection(body)

    mock_cursor.execute.assert_called_once_with("SELECT * FROM imoveis")
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("utils.load_db")
def test_listar_imoveis_vazio(mock_load_db, client):
    """GET /imoveis - lista vazia com links de navegacao."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    mock_load_db.return_value = mock_conn

    response = client.get("/imoveis")
    body = response.get_json()

    assert response.status_code == 200
    assert body["dados"] == []
    assert_links_collection(body)

    mock_cursor.execute.assert_called_once_with("SELECT * FROM imoveis")
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("utils.load_db")
def test_listar_imoveis_pelo_id(mock_load_db, client):
    """GET /imoveis/<id> - retorna item com links HATEOAS."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {"id": 1, "logradouro": "John Falls", "tipo_logradouro": "Rua", "bairro": "Port Carol", "cidade": "Knappview", "cep": "14150", "tipo": "casa", "valor": 961722.89, "data_aquisicao": "2022-01-05"}

    mock_load_db.return_value = mock_conn

    response = client.get("/imoveis/1")
    body = response.get_json()

    assert response.status_code == 200
    assert body["id"] == 1
    assert body["logradouro"] == "John Falls"
    assert_links_item(body, 1)

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis WHERE id = %s",
        (1,),
    )
    mock_cursor.fetchone.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("utils.load_db")
def test_listar_imovel_id_not_found(mock_load_db, client):
    """GET /imoveis/<id> - imovel nao existe."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None
    mock_load_db.return_value = mock_conn

    response = client.get("/imoveis/999")

    assert response.status_code == 404
    assert response.get_json() == {"erro": "Imovel nao encontrado"}

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis WHERE id = %s",
        (999,),
    )
    mock_cursor.fetchone.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("utils.load_db")
def test_adicionar_imoveis(mock_load_db, client):
    """POST /imoveis - cria imovel com sucesso e links."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.lastrowid = 10
    mock_load_db.return_value = mock_conn

    payload = {"logradouro": "John Falls", "tipo_logradouro": "Rua", "bairro": "Port Carol", "cidade": "Knappview", "cep": "14150", "tipo": "casa", "valor": 961722.89, "data_aquisicao": "2022-01-05"}

    response = client.post("/imoveis", json=payload)
    body = response.get_json()

    assert response.status_code == 201
    assert body["id"] == 10
    assert body["_links"]["self"]["href"] == "/imoveis/10"
    assert body["_links"]["collection"]["href"] == "/imoveis"

    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        ("John Falls", "Rua", "Port Carol", "Knappview", "14150", "casa", 961722.89, "2022-01-05"),
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("utils.load_db")
def test_adicionar_imovel_erro_validacao(mock_load_db, client):
    """POST /imoveis - falta campo obrigatorio -> 400."""
    response = client.post("/imoveis", json={"logradouro": "John Falls"})

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Campos obrigatorios: logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao"}

    mock_load_db.assert_not_called()

@patch("utils.load_db")
def test_adicionar_imovel_erro_validacao_campos_nulos_ou_vazios(mock_load_db, client):
    """POST /imoveis - campo obrigatorio nulo/vazio -> 400."""
    payload = {"logradouro": "", "tipo_logradouro": "Rua", "bairro": "Centro", "cidade": None, "cep": "01310-100", "tipo": "apartamento", "valor": 500000.00, "data_aquisicao": "2022-01-06"}

    response = client.post("/imoveis", json=payload)

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Campos obrigatorios: logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao"}

    mock_load_db.assert_not_called()

@patch("utils.load_db")
def test_atualizar_imovel_ok(mock_load_db, client):
    """PUT /imoveis/<id> - atualiza com sucesso e retorna links."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 1
    mock_load_db.return_value = mock_conn

    payload = {"logradouro": "John Falls", "tipo_logradouro": "Rua", "bairro": "Port Carol", "cidade": "Knappview", "cep": "14150", "tipo": "casa", "valor": 961722.89, "data_aquisicao": "2022-01-05"}

    response = client.put("/imoveis/1", json=payload)
    body = response.get_json()

    assert response.status_code == 200
    assert body["mensagem"] == "Imovel atualizado com sucesso"
    assert body["_links"]["self"]["href"] == "/imoveis/1"
    assert body["_links"]["delete"]["href"] == "/imoveis/1"
    assert body["_links"]["collection"]["href"] == "/imoveis"

    mock_cursor.execute.assert_called_once_with(
        "UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s",
        ("John Falls", "Rua", "Port Carol", "Knappview", "14150", "casa", 961722.89, "2022-01-05", 1),
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("utils.load_db")
def test_atualizar_imovel_not_found(mock_load_db, client):
    """PUT /imoveis/<id> - imovel nao encontrado (rowcount=0)."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 0
    mock_load_db.return_value = mock_conn

    payload = {"logradouro": "John Falls", "tipo_logradouro": "Rua", "bairro": "Port Carol", "cidade": "Knappview", "cep": "14150", "tipo": "casa", "valor": 961722.89, "data_aquisicao": "2022-01-05"}

    response = client.put("/imoveis/999", json=payload)

    assert response.status_code == 404
    assert response.get_json() == {"erro": "Imovel nao encontrado"}

    mock_cursor.execute.assert_called_once_with(
        "UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s",
        ("John Falls", "Rua", "Port Carol", "Knappview", "14150", "casa", 961722.89, "2022-01-05", 999),
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("utils.load_db")
def test_atualizar_imovel_erro_validacao(mock_load_db, client):
    """PUT /imoveis/<id> - falta campo obrigatorio -> 400."""
    response = client.put("/imoveis/1", json={"logradouro": "John Falls"})

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Campos obrigatorios: logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao"}

    mock_load_db.assert_not_called()

@patch("utils.load_db")
def test_atualizar_imovel_erro_validacao_campos_nulos_ou_vazios(mock_load_db, client):
    """PUT /imoveis/<id> - campo obrigatorio nulo/vazio -> 400."""
    payload = {"logradouro": "John Falls", "tipo_logradouro": "Rua", "bairro": "   ", "cidade": "Knappview", "cep": "14150", "tipo": "casa", "valor": None, "data_aquisicao": "2022-01-05"}

    response = client.put("/imoveis/1", json=payload)

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Campos obrigatorios: logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao"}

    mock_load_db.assert_not_called()

@patch("utils.load_db")
def test_deletar_imovel_ok(mock_load_db, client):
    """DELETE /imoveis/<id> - deleta com sucesso e retorna links."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 1
    mock_load_db.return_value = mock_conn

    response = client.delete("/imoveis/1")
    body = response.get_json()

    assert response.status_code == 200
    assert body["mensagem"] == "Imovel exclu\u00eddo com sucesso"
    assert body["_links"]["collection"]["href"] == "/imoveis"
    assert body["_links"]["create"]["href"] == "/imoveis"

    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM imoveis WHERE id = %s",
        (1,),
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("utils.load_db")
def test_deletar_imovel_not_found(mock_load_db, client):
    """DELETE /imoveis/<id> - imovel nao encontrado."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 0
    mock_load_db.return_value = mock_conn

    response = client.delete("/imoveis/999")

    assert response.status_code == 404
    assert response.get_json() == {"erro": "Imovel nao encontrado"}

    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM imoveis WHERE id = %s",
        (999,),
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("utils.load_db")
def test_listar_imoveis_pelo_tipo(mock_load_db, client):
    """GET /imoveis?tipo=casa - filtra por tipo com links."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [{"id": 1, "logradouro": "John Falls", "tipo_logradouro": "Rua", "bairro": "Port Carol", "cidade": "Knappview", "cep": "14150", "tipo": "casa", "valor": 961722.89, "data_aquisicao": "2022-01-05"}]

    mock_load_db.return_value = mock_conn

    response = client.get("/imoveis?tipo=casa")
    body = response.get_json()

    assert response.status_code == 200
    assert len(body["dados"]) == 1
    assert body["dados"][0]["id"] == 1
    assert_links_item(body["dados"][0], 1)
    assert body["_links"]["filtrar_por_tipo"]["href"] == "/imoveis?tipo=casa"

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis WHERE tipo = %s",
        ("casa",),
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("utils.load_db")
def test_listar_imovel_tipo_not_found(mock_load_db, client):
    """GET /imoveis?tipo=<tipo> - tipo nao existe."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = []
    mock_load_db.return_value = mock_conn

    response = client.get("/imoveis?tipo=mansao")
    body = response.get_json()

    assert response.status_code == 200
    assert body["dados"] == []
    assert body["_links"]["filtrar_por_tipo"]["href"] == "/imoveis?tipo=mansao"

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis WHERE tipo = %s",
        ("mansao",),
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("utils.load_db")
def test_listar_imoveis_pela_cidade(mock_load_db, client):
    """GET /imoveis?cidade=Knappview - filtra por cidade com links."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [{"id": 1, "logradouro": "John Falls", "tipo_logradouro": "Rua", "bairro": "Port Carol", "cidade": "Knappview", "cep": "14150", "tipo": "casa", "valor": 961722.89, "data_aquisicao": "2022-01-05"}]

    mock_load_db.return_value = mock_conn

    response = client.get("/imoveis?cidade=Knappview")
    body = response.get_json()

    assert response.status_code == 200
    assert len(body["dados"]) == 1
    assert body["dados"][0]["id"] == 1
    assert_links_item(body["dados"][0], 1)
    assert body["_links"]["filtrar_por_cidade"]["href"] == "/imoveis?cidade=Knappview"

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis WHERE cidade = %s",
        ("Knappview",),
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("utils.load_db")
def test_listar_imovel_cidade_not_found(mock_load_db, client):
    """GET /imoveis?cidade=<cidade> - cidade nao existe."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = []
    mock_load_db.return_value = mock_conn

    response = client.get("/imoveis?cidade=goiania")
    body = response.get_json()

    assert response.status_code == 200
    assert body["dados"] == []
    assert body["_links"]["filtrar_por_cidade"]["href"] == "/imoveis?cidade=goiania"

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis WHERE cidade = %s",
        ("goiania",),
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()