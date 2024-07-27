import pytest

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


@pytest.mark.parametrize("list_currency, expected", [
    (["AAPL"], [{'stock': 'AAPL', 'price': '224.31000'}])
])
def test_get_stock_prices_aapl(list_currency, expected):
    assert get_stock_prices(list_currency) == expected


@pytest.mark.parametrize("list_currency, expected", [
    (["MSFT"], [{'stock': 'MSFT', 'price': '437.10999'}])
])
def test_get_stock_prices_msft(list_currency, expected):
    assert get_stock_prices(list_currency) == expected


@pytest.mark.parametrize("list_currency, expected", [
    (["NVDA"], [{'stock': 'NVDA', 'price': '117.93000'}])
])
def test_get_stock_prices_nvda(list_currency, expected):
    assert get_stock_prices(list_currency) == expected
