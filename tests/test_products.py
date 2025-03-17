import pytest
from products import Product

class TestProduct:
    #@pytest.fixture(autouse=True)

    def test_init(self):
        with pytest.raises(TypeError, match="is invalid"): Product(1, 1, 1)
        with pytest.raises(ValueError, match="is invalid"): Product("Name", -1, 1)

    def test_show(self):
        product = Product("Name", 1, 2)
        assert product.show() == "Name, Price: $1, Quantity: 2"

    def test_name_and_price(self):
        product = Product("Name", 1, 2)
        assert product.name_and_price(100) == ("Name", 100)

    def test_buy(self):
        product = Product("Name", 1, 200)
        assert product.buy(100) == 100
        with pytest.raises(ValueError, match="Quantity is greater"):  product.buy(101)
        assert product.is_active() is True
        assert product.buy(100) == 100
        assert product.is_active() is False