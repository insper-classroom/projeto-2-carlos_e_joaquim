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
