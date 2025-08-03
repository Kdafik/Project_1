from unittest.mock import patch, mock_open, Mock

from src.external_api import get_currency_rates, get_stock_prices


@patch("src.external_api.requests.get")
@patch("src.external_api.os.getenv", return_value="fake_api_key")
@patch("src.external_api.json.load")
@patch("builtins.open", new_callable=mock_open, read_data='{"user_currencies"}: ["USD", "EUR"]')
def test_get_currency_rates(mock_open_file, mock_json_load, mock_getenv, mock_requests_get):
    mock_json_load.return_value = {"user_currencies": ["USD", "EUR"]}
    mock_getenv.return_value = "fake_api_key"
    mock_requests_get.side_effect = [
        Mock(json=Mock(return_value={"data": {"USDRUB": "89.1234"}})),
        Mock(json=Mock(return_value={"data": {"EURRUB": "97.5678"}}))
    ]

    result = get_currency_rates()

    expected = [
        {"currency": "USD", "rate": 89.12},
        {"currency": "EUR", "rate": 97.57}
    ]

    assert result == expected


@patch("src.external_api.requests.get")
@patch("src.external_api.os.getenv", return_value="fake_api_key")
@patch("src.external_api.json.load")
@patch("builtins.open", new_callable=mock_open, read_data='{"user_stocks"}: ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]')
def test_get_stock_prices(mock_open_file, mock_json_load, mock_getenv, mock_requests_get):
    mock_json_load.return_value = {"user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}
    mock_getenv.return_value = "fake_api_key"
    mock_requests_get.side_effect = [
        Mock(json=Mock(return_value=[{"ticker": "AAPL", "cik": "0000123"}])),
        Mock(json=Mock(return_value=[{"ticker": "AMZN", "cik": "0000124"}])),
        Mock(json=Mock(return_value=[{"ticker": "GOOGL", "cik": "0000125"}])),
        Mock(json=Mock(return_value=[{"ticker": "MSFT", "cik": "0000126"}])),
        Mock(json=Mock(return_value=[{"ticker": "TSLA", "cik": "0000127"}])),
    ]

    result = get_stock_prices()

    expected = [
        {"stock": "AAPL", "price": 123},
        {"stock": "AMZN", "price": 124},
        {"stock": "GOOGL", "price": 125},
        {"stock": "MSFT", "price": 126},
        {"stock": "TSLA", "price": 127},
    ]

    assert result == expected
