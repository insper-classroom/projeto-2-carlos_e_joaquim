import pytest
from unittest.mock import patch, MagicMock 
from servidor import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
@patch("utils.load_db")
def test_listar_imoveis_com_dados(mock_load_db, client):
    """GET /listar-imoveis - lista com dados."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {'id': 1, 'logradouro': 'John Falls', 'tipo_logradouro': 'Rua', 'bairro': 'Port Carol', 'cidade': 'Knappview', 'cep': '14150', 'tipo': 'casa', 'valor': 961722.89, 'data_aquisicao': '2022-01-05'},
        {'id': 2, 'logradouro': 'Jane Doe', 'tipo_logradouro': 'Avenida', 'bairro': 'Centro', 'cidade': 'São Paulo', 'cep': '01310-100', 'tipo': 'apartamento', 'valor': 500000.00, 'data_aquisicao': '2022-01-06'},
    ]

    mock_load_db.return_value = mock_conn

    response = client.get("/imoveis")

    assert response.status_code == 200
    assert response.get_json() == [
        {"id": 1, "logradouro": "John Falls", "tipo_logradouro": "Rua", "bairro": "Port Carol", "cidade": "Knappview", "cep": "14150", "tipo": "casa", "valor": 961722.89, "data_aquisicao": "2022-01-05"},
        {"id": 2, "logradouro": "Jane Doe", "tipo_logradouro": "Avenida", "bairro": "Centro", "cidade": "São Paulo", "cep": "01310-100", "tipo": "apartamento", "valor": 500000.00, "data_aquisicao": "2022-01-06"},
    ]

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis"
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()



@patch("utils.load_db")
def test_listar_imoveis_vazio(mock_load_db, client):
    """GET /listar-imoveis - lista vazia."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    mock_load_db.return_value = mock_conn

    response = client.get("/imoveis")

    assert response.status_code == 200
    assert response.get_json() == []

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis"
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("utils.load_db")
def test_listar_imoveis_pelo_id(mock_load_db, client):
    """GET /listar-imoveis/<id> - listar imóvel pelo id."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {
        'id': 1, 'logradouro': 'John Falls', 'tipo_logradouro': 'Rua', 'bairro': 'Port Carol', 'cidade': 'Knappview', 'cep': '14150', 'tipo': 'casa', 'valor': 961722.89, 'data_aquisicao': '2022-01-05'
    }

    mock_load_db.return_value = mock_conn

    response = client.get("/imoveis/1")

    assert response.status_code == 200
    assert response.get_json()['id'] == 1
    assert response.get_json()['logradouro'] == 'John Falls'

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis WHERE id = %s",
        (1,)
    )
    mock_cursor.fetchone.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("utils.load_db")
def test_listar_imovel_id_not_found(mock_load_db, client):
    """GET /listar-imoveis/<id> - imóvel não existe."""
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
    """POST /adicionar-imovel - cria imóvel com sucesso."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Simula ID gerado pelo banco
    mock_cursor.lastrowid = 10

    mock_load_db.return_value = mock_conn

    payload =  {"logradouro": "John Falls", "tipo_logradouro": "Rua", "bairro": "Port Carol", "cidade": "Knappview", "cep": "14150", "tipo": "casa", "valor": 961722.89, "data_aquisicao": "2022-01-05"}
    response = client.post("/imoveis", json=payload)

    assert response.status_code == 201
    assert response.get_json() == {"id": 10}

    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        ("John Falls", "Rua", "Port Carol", "Knappview", "14150", "casa", 961722.89, "2022-01-05"),
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("utils.load_db")
def test_adicionar_imovel_erro_validacao(mock_load_db, client):
    """POST /adicionar-imovel - falta campo obrigatório -> 400. Não deve acessar o banco."""
    response = client.post("/imoveis", json={"logradouro": "John Falls"})

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Campos obrigatorios: logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao"}

    mock_load_db.assert_not_called()

@patch("utils.load_db")
def test_atualizar_imovel_ok(mock_load_db, client):
    """PUT /listar-imoveis/<id> - atualiza com sucesso."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Simula que 1 linha foi atualizada
    mock_cursor.rowcount = 1
    mock_load_db.return_value = mock_conn

    payload = {"logradouro": "John Falls", "tipo_logradouro": "Rua", "bairro": "Port Carol", "cidade": "Knappview", "cep": "14150", "tipo": "casa", "valor": 961722.89, "data_aquisicao": "2022-01-05"}
    response = client.put("/imoveis/1", json=payload)

    assert response.status_code == 200
    assert response.get_json() == {"mensagem": "Imovel atualizado com sucesso"}

    mock_cursor.execute.assert_called_once_with(
        "UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s",
        ("John Falls", "Rua", "Port Carol", "Knappview", "14150", "casa", 961722.89, "2022-01-05", 1),
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("utils.load_db")
def test_atualizar_imovel_not_found(mock_load_db, client):
    """PUT /listar-imoveis/<id> - imóvel não encontrado (rowcount=0)."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 0
    mock_load_db.return_value = mock_conn

    payload = {"logradouro": "John Falls", "tipo_logradouro": "Rua", "bairro": "Port Carol", "cidade": "Knappview", "cep": "14150", "tipo": "casa", "valor": 961722.89, "data_aquisicao": "2022-01-05"}
    response = client.put("/imoveis/999", json=payload)

    assert response.status_code == 404
    assert response.get_json() == {"erro": "imovel nao encontrado"}

    mock_cursor.execute.assert_called_once_with(
        "UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s",
        ("John Falls", "Rua", "Port Carol", "Knappview", "14150", "casa", 961722.89, "2022-01-05", 999),
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("utils.load_db")
def test_atualizar_imovel_erro_validacao(mock_load_db, client):
    """PUT /listar-imoveis/<id> - falta campo obrigatório -> 400. Não deve acessar o banco."""
    response = client.put("/imoveis/1", json={"logradouro": "John Falls"})

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Campos obrigatorios: logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao"}

    mock_load_db.assert_not_called()
