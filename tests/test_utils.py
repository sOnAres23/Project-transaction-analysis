from src.utils import get_currency_rates, get_stock_prices
from unittest.mock import patch


@patch('requests.get')
def test_get_currency_rates_usd(mock_get, get_currency_usd, get_requests_usd):
    mock_get.return_value.json.return_value = get_requests_usd
    list_currency = ["USD"]
    assert get_currency_rates(list_currency) == get_currency_usd


@patch('requests.get')
def test_get_currency_rates_eur(mock_get, get_currency_eur, get_requests_eur):
    mock_get.return_value.json.return_value = get_requests_eur
    list_currency = ["EUR"]
    assert get_currency_rates(list_currency) == get_currency_eur


@patch('requests.get')
def test_get_stock_prices(mock_get, get_stocks_aapl, get_requests_aapl):
    mock_get.return_value.json.return_value = get_requests_aapl
    list_currency = ["AAPL"]
    assert get_stock_prices(list_currency) == get_stocks_aapl
