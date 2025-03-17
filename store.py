import products

class Store:
    def __init__(self, list_of_products = []):
        self.list_of_products = list_of_products

    def add_product(self, new_product):
        for old_product in self.list_of_products:
            if old_product.name == new_product.name and old_product.price == new_product.price:
                old_product.quantity += new_product.quantity
                return
        self.list_of_products.append(new_product)

    def remove_product(self, product):
        if product in self.list_of_products:
            self.list_of_products.remove(product)

    def get_total_quantity(self):
        return sum(product.quantity for product in self.list_of_products)

    def get_all_products(self):
        return [product for product in self.list_of_products if product.is_active()]

    def validate_shopping_list(self, shopping_list):

        for item in shopping_list:
            if not isinstance(item, tuple):
                return False
            if len(item) != 2:
                return False
            product, quantity = item
            if not isinstance(product, products.Product) or not isinstance(quantity, int):
                return False
            if product not in self.list_of_products:
                return False
            if quantity > product.get_quantity():
                return False
        return True

    def order(self, shopping_list):
        if self.validate_shopping_list(shopping_list) is False:
            raise ValueError("Invalid shopping list.")
        return sum(product.buy(quantity) for product, quantity in shopping_list)


def main():
    product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    products.Product("Google Pixel 7", price=500, quantity=250),
                    ]

    best_buy = Store(product_list)
    all_products = best_buy.get_all_products()
    print(best_buy.get_total_quantity())
    print(best_buy.order([(all_products[0], 1), (all_products[1], 2)]))

if __name__ == '__main__':
    main()
