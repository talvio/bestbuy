import products

class Store:
    def __init__(self, list_of_products = []):
        """
        Initialize the store
        """
        self.list_of_products = list_of_products

    def add_product(self, new_product):
        """
        Add a new product to the store.
        If the product is already listed in the store, product quantity is changed but
        no duplicate product is added.
        If the price is different and the name is the same, the new product is added.
        :param new_product: instance of products.Product
        :return: None
        """
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

    def get_product_type_quantity(self):
        """
        Return how many different items are active in the store inventory.
        """
        return sum(1 for product in self.list_of_products if product.is_active())

    def validate_shopping_list(self, shopping_list):
        for item in shopping_list:
            if not isinstance(item, tuple):
                return False, "Shopping list format is wrong."
            if len(item) != 2:
                return False, "Shopping list format is wrong."
        unified_shopping_list = {}
        for product, quantity in shopping_list:
            if not isinstance(product, products.Product) or not isinstance(quantity, int):
                return False, "Shopping list format is wrong."
            if product in unified_shopping_list:
                unified_shopping_list[product] += quantity
            else:
                unified_shopping_list[product] = quantity
        for product, quantity in unified_shopping_list.items():
            if product not in self.list_of_products:
                return False, f"Product {product.name} is not in the store."
            if quantity > product.get_quantity():
                return False, (f"there are {product.get_quantity()} items of {product.name} available. "
                               f"The store cannot provide the requested amount: {quantity}")
        return True, "No errors"

    def order(self, shopping_list):
        validation_result, message = self.validate_shopping_list(shopping_list)
        if validation_result is not True:
            return None, message
        return sum(product.buy(quantity) for product, quantity in shopping_list), "Order completed successfully."


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
