import pytest
from unittest.mock import patch, MagicMock 
from servidor import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
@patch("api.conectar_banco")
def test_listar_imoveis_com_dados(mock_conectar_banco, client):
    """GET /listar-imoveis - lista com dados."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        ('John Falls', 'Rua', 'Port Carol', 'Knappview', '14150', 'casa', 961722.89, '2022-01-05'),
        ('Jane Doe', 'Avenida', 'Centro', 'São Paulo', '01310-100', 'apartamento', 500000.00, '2022-01-06'),
    ]

    mock_conectar_banco.return_value = mock_conn

    response = client.get("/listar-imoveis")

    assert response.status_code == 200
    assert response.get_json() == [
        {"logradouro": "John Falls", "tipo_logradouro": "Rua", "bairro": "Port Carol", "cidade": "Knappview", "cep": "14150", "tipo": "casa", "valor": 961722.89, "data_aquisicao": "2022-01-05"},
        {"logradouro": "Jane Doe", "tipo_logradouro": "Avenida", "bairro": "Centro", "cidade": "São Paulo", "cep": "01310-100", "tipo": "apartamento", "valor": 500000.00, "data_aquisicao": "2022-01-06"},
    ]

    mock_cursor.execute.assert_called_once_with(
        "SELECT logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis"
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()



@patch("api.conectar_banco")
def test_listar_imoveis_vazio(mock_conectar_banco, client):
    """GET /listar-imoveis - lista vazia."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    mock_conectar_banco.return_value = mock_conn

    response = client.get("/listar-imoveis")

    assert response.status_code == 200
    assert response.get_json() == []

    mock_cursor.execute.assert_called_once_with(
        "SELECT logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis"
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("api.conectar_banco")
def test_listar_imoveis_pelo_id(mock_conectar_banco, client):
    """GET /listar-imoveis - listar imóvel pelo id."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        ('John Falls', 'Rua', 'Port Carol', 'Knappview', '14150', 'casa', 961722.89, '2022-01-05'),
    ]

    mock_conectar_banco.return_value = mock_conn

    response = client.get("/listar-imoveis?id=1")

    assert response.status_code == 200
    assert response.get_json() == [
        {"logradouro": "John Falls", "tipo_logradouro": "Rua", "bairro": "Port Carol", "cidade": "Knappview", "cep": "14150", "tipo": "casa", "valor": 961722.89, "data_aquisicao": "2022-01-05"},
    ]

    mock_cursor.execute.assert_called_once_with(
        "SELECT logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis WHERE id = %s",
        (1,)
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

def test_listar_imoveis_pelo_id_inexistente(mock_conectar_banco, client):
    """GET /listar-imoveis - listar imóvel pelo id inexistente."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    mock_conectar_banco.return_value = mock_conn

    response = client.get("/listar-imoveis?id=999")

    assert response.status_code == 200
    assert response.get_json() == []

    mock_cursor.execute.assert_called_once_with(
        "SELECT logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis WHERE id = %s",
        (999,)
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("api.conectar_banco")
def test_listar_contatos_com_dados(mock_conectar_banco, client):
    """GET /contacts - lista com dados."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        ("John Falls", "Rua", "Port Carol", "Knappview", "14150", "casa", 961722.89, "2022-01-05"),
        ("Jane Doe", "Avenida", "Centro", "São Paulo", "01310-100", "apartamento", 500000.00, "2022-01-06"),
    ]

    mock_conectar_banco.return_value = mock_conn

    response = client.get("/contacts")

    assert response.status_code == 200
    assert response.get_json() == [
        {"logradouro": "John Falls", "tipo_logradouro": "Rua", "bairro": "Port Carol", "cidade": "Knappview", "cep": "14150", "tipo": "casa", "valor": 961722.89, "data_aquisicao": "2022-01-05"},
        {"logradouro": "Jane Doe", "tipo_logradouro": "Avenida", "bairro": "Centro", "cidade": "São Paulo", "cep": "01310-100", "tipo": "apartamento", "valor": 500000.00, "data_aquisicao": "2022-01-06"},
    ]

    mock_cursor.execute.assert_called_once_with(
        "SELECT logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis"
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("api.conectar_banco")
def test_adicionar_imoveis(mock_conectar_banco, client):
    """POST /adicionar-imovel - cria imóvel com sucesso."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Simula ID gerado pelo banco
    mock_cursor.lastrowid = 10

    mock_conectar_banco.return_value = mock_conn

    payload =  {"logradouro": "John Falls", "tipo_logradouro": "Rua", "bairro": "Port Carol", "cidade": "Knappview", "cep": "14150", "tipo": "casa", "valor": 961722.89, "data_aquisicao": "2022-01-05"}
    response = client.post("/adicionar-imovel", json=payload)

    assert response.status_code == 201
    assert response.get_json() == {"id": 10}

    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        ("John Falls", "Rua", "Port Carol", "Knappview", "14150", "casa", 961722.89, "2022-01-05"),
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("api.conectar_banco")
def test_adicionar_imovel_erro_validacao(mock_conectar_banco, client):
    """POST /adicionar-imovel - falta campo obrigatório -> 400. Não deve acessar o banco."""
    response = client.post("/adicionar-imovel", json={"logradouro": "John Falls"})

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Campos obrigatórios: logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao"}

    mock_conectar_banco.assert_not_called()
