import pytest
from products import Product
import promotions

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
        assert product.show() == "Name test testing, Price: $100, Quantity: 10000, Promotion: None"

    def test_show(self):
        product = Product("Name", 1, 2)
        assert product.show() == "Name, Price: $1, Quantity: 2, Promotion: None"

    def test_name_and_price(self):
        product = Product("Name", 1, 2)
        assert product.name_and_price(100) == ("Name", 100)

    def test_buy_too_many(self):
        product = Product("Name", 1, 200)
        assert product.buy(100) == (100, 'Purchase was successful')
        assert product.get_quantity() == 100
        assert product.buy(101) == (False, 'there are only 100 pieces of Name. Cannot sell 101')

    def test_buy_all(self):
        product = Product("Name", 1, 200)
        assert product.is_active() is True
        assert product.get_quantity() == 200
        assert product.buy(200) == (200, 'Purchase was successful')
        assert product.is_active() is False
        assert product.get_quantity() == 0

    def test_second_half_price_promotion(self):
        product = Product("Name", 10, 200)
        second_half_price = promotions.SecondHalfPrice("Second Half price!")
        assert product.buy(2) == (20, 'Purchase was successful')
        product.set_promotion(second_half_price)
        assert product.buy(2) == (15, 'Purchase was successful')

    def test_third_one_free_promotion(self):
        product = Product("Name", 10, 200)
        third_one_free = promotions.ThirdOneFree("Third One Free!")
        assert product.buy(3) == (30, 'Purchase was successful')
        product.set_promotion(third_one_free)
        assert product.buy(3) == (20, 'Purchase was successful')

    def test_thirty_percent_promotion(self):
        product = Product("Name", 10, 200)
        thirty_percent = promotions.PercentDiscount("30% off!", percent=30)
        assert product.buy(100) == (1000, 'Purchase was successful')
        product.set_promotion(thirty_percent)
        assert product.buy(100) == (700, 'Purchase was successful')

