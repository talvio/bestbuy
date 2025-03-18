import pytest
from products import Product

class TestProduct:

    def test_init_wrong_types_name_integer(self):
        with pytest.raises(TypeError, match="is invalid"): Product(1, 1, 1)

    def test_init_wrong_types_quantity_string(self):
        with pytest.raises(TypeError, match="is invalid"): Product(1, 1, "1")

    def test_init_wrong_values_negative_price(self):
        with pytest.raises(ValueError, match="is invalid"): Product("Name", -1, 1)

    def test_init_wrong_values_empty_name(self):
        with pytest.raises(ValueError, match="is invalid"): Product("", 1, 1)

    def test_init_wrong_values_negative_quantity(self):
        with pytest.raises(ValueError, match="is invalid"): Product("Name", 1, -11)

    def test_init_nominal(self):
        product = Product("Name test testing", price=100, quantity=10000)
        assert product.show() == "Name test testing, Price: $100, Quantity: 10000"

    def test_show(self):
        product = Product("Name", 1, 2)
        assert product.show() == "Name, Price: $1, Quantity: 2"

    def test_name_and_price(self):
        product = Product("Name", 1, 2)
        assert product.name_and_price(100) == ("Name", 100)

    def test_buy_too_many(self):
        product = Product("Name", 1, 200)
        assert product.buy(100) == 100
        assert product.get_quantity() == 100
        with pytest.raises(ValueError, match="Quantity is greater"):  product.buy(101)

    def test_buy_all(self):
        product = Product("Name", 1, 200)
        assert product.is_active() is True
        assert product.get_quantity() == 200
        assert product.buy(200) == 200
        assert product.is_active() is False
        assert product.get_quantity() == 0