import pytest
import main
from unittest.mock import patch

def test_setup_store():
    store = main.setup_store()
    all_products = store.get_all_products()
    assert all_products[0].show() == "MacBook Air M2, Price: $1450, Quantity: 100"
    assert all_products[-1].show() == "Rare coffee, Price: $100, Quantity: 100 Limited to 1 per order!"

def test_get_order(monkeypatch, capfd):
    store = main.setup_store()
    inputs_to_get_order = iter(['7', '1', '6', '1', '5', '100', '\n'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs_to_get_order))
    shopping_list = main.get_order(store)
    assert shopping_list[0][0].show() == "Rare coffee, Price: $100, Quantity: 100 Limited to 1 per order!"
    assert shopping_list[1][0].show() == "Shipping, Price: $10  Limited to 1 per order!"
    assert shopping_list[2][0].show() == "XYZ Service Contract, Price: $400, Quantity: Unlimited"
    assert shopping_list[0][1] == 1
    assert shopping_list[1][1] == 1
    assert shopping_list[2][1] == 100

def test_get_order_limited_too_many(monkeypatch, capfd):
    store = main.setup_store()
    inputs_to_get_order = iter(['7', '2', '\n'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs_to_get_order))
    shopping_list = main.get_order(store)
    captured = capfd.readouterr()
    assert "limited product. Only 1 allowed in one purchase." in captured.out

def test_make_an_order(monkeypatch, capfd):
    store = main.setup_store()
    products_all = store.get_all_products()
    order = [(products_all[0], 100), (products_all[1], 200), (products_all[5], 1)]
    monkeypatch.setattr('main.get_order', lambda _: order)
    main.make_an_order(store)
    captured = capfd.readouterr()
    assert "Total payment: $195010" in captured.out

def test_make_an_invalid_order(monkeypatch, capfd):
    store = main.setup_store()
    products_all = store.get_all_products()
    order = [(products_all[0], 100), (products_all[1], 200), (products_all[5], 2)]
    monkeypatch.setattr('main.get_order', lambda _: order)
    main.make_an_order(store)
    captured = capfd.readouterr()
    assert "Shipping is a limited product" in captured.out