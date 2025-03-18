import products
from store import Store

class TestStore:
    def setup(self):
        product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                        products.Product("Google Pixel 7", price=500, quantity=250),
                        products.ImmaterialProduct("Windows License", price=125),
                        products.ImmaterialProduct("XYZ Service Contract", price=400),
                        products.LimitedImmaterialProduct("Shipping", price=10, maximum=1),
                        products.LimitedProduct("Rare coffee", price=100, maximum=1, quantity=100),
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
        store.add_product(product2)
        assert store.get_all_products()[0] is product1
        assert store.get_all_products()[0].get_quantity() == 200
        assert len(store.get_all_products()) == 1
        product3 = products.Product("MacBook Air M2", price=1500, quantity=100)
        store.add_product(product3)
        assert store.get_all_products()[0].get_quantity() == 200
        assert store.get_all_products()[1].get_quantity() == 100
        assert len(store.get_all_products()) == 2

    def test_add_immaterial_product(self):
        store = self.setup()
        product1 = products.ImmaterialProduct("New Immaterial", price=300)
        store.add_product(product1)
        assert store.get_all_products()[-1] is product1
        no_of_products = len(store.get_all_products())
        product2 = products.ImmaterialProduct("New Immaterial", price=300)
        store.add_product(product2)
        assert store.get_all_products()[-1] is product1
        assert len(store.get_all_products()) == no_of_products
        product3 = products.ImmaterialProduct("New Immaterial", price=1500)
        store.add_product(product3)
        assert store.get_all_products()[-1] is product3
        assert store.get_all_products()[-1].name_and_price() == ("New Immaterial", 1500)
        assert len(store.get_all_products()) == no_of_products + 1

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
                (False, 'there are only 100 pieces of MacBook Air M2. Cannot sell 101'))

    def test_validate_shopping_list_wrong_format(self):
        store = self.setup()
        products_all = store.get_all_products()
        shopping_list = [products_all[0], 100, products_all[1], 200]
        assert (store.validate_shopping_list(shopping_list) ==
                (False, 'Shopping list format is wrong. List items are not all tuples'))

    def test_validate_shopping_list_none_existing_product(self):
        store = self.setup()
        products_all = store.get_all_products()
        product3 = products.Product("Something new", price=1500, quantity=100)
        shopping_list = [(product3, 101), (products_all[1], 200)]
        assert (store.validate_shopping_list(shopping_list) ==
                (False, 'Product Something new is not in the store'))

    def test_remove_product(self):
        store = self.setup()
        products_all = store.get_all_products()
        store.remove_product(products_all[0])
        products_all_new = store.get_all_products()
        assert products_all[1:] == products_all_new


