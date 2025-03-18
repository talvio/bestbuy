import products
from store import Store

class TestStore:
    def setup(self):
        product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                        products.Product("Google Pixel 7", price=500, quantity=250)
                        ]
        store = Store(product_list)
        return store

    def test_init(self):
        store = self.setup()

    def test_add_product(self):
        store = Store([])
        product1 = products.Product("MacBook Air M2", price=1450, quantity=100)
        store.add_product(product1)
        assert store.get_all_products()[0] is product1
        product2 = products.Product("MacBook Air M2", price=1450, quantity=100)
        assert store.get_all_products()[0] is product1
        store.add_product(product2)
        assert store.get_all_products()[0].quantity == 200
        assert len(store.get_all_products()) == 1
        product3 = products.Product("MacBook Air M2", price=1500, quantity=100)
        store.add_product(product3)
        assert store.get_all_products()[0].quantity == 200
        assert store.get_all_products()[1].quantity == 100
        assert len(store.get_all_products()) == 2

    def test_validate_shopping_list(self):
        store = self.setup()
        products_all = store.get_all_products()
        shopping_list = [(products_all[0], 100), (products_all[1], 200)]
        assert store.validate_shopping_list(shopping_list) == (True, 'No errors')

    def test_validate_shopping_list_too_many(self):
        store = self.setup()
        products_all = store.get_all_products()
        shopping_list = [(products_all[0], 101), (products_all[1], 200)]
        assert (store.validate_shopping_list(shopping_list) ==
                (False, ('there are 100 items of MacBook Air M2 available. '
                         'The store cannot provide the requested amount: 101')))

    def test_validate_shopping_list_wrong_format(self):
        store = self.setup()
        products_all = store.get_all_products()
        shopping_list = [products_all[0], 100, products_all[1], 200]
        assert store.validate_shopping_list(shopping_list) == (False, 'Shopping list format is wrong.')

    def test_validate_shopping_list_none_existing_product(self):
        store = self.setup()
        products_all = store.get_all_products()
        product3 = products.Product("Something new", price=1500, quantity=100)
        shopping_list = [(product3, 101), (products_all[1], 200)]
        assert (store.validate_shopping_list(shopping_list) ==
                (False, 'Product Something new is not in the store.'))

    def test_remove_product(self):
        store = self.setup()
        products_all = store.get_all_products()
        store.remove_product(products_all[0])
        products_all_new = store.get_all_products()
        assert products_all[1:] == products_all_new


