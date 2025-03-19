"""
The Store class to be used in Best Buy application.
"""

import products


class Store:
    """
    Store functionality. Uses also Product class in store inventory.
    """
    def __init__(self, list_of_products = None):
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
            if (old_product.name_and_price() == new_product.name_and_price()
                    and isinstance(old_product, products.Product)
                    and isinstance(new_product, products.Product)):
                old_product.set_quantity(old_product.get_quantity() + new_product.get_quantity())
                return
            if (old_product.name_and_price() == new_product.name_and_price()
                    and isinstance(old_product, products.ImmaterialProduct)
                    and isinstance(new_product, products.ImmaterialProduct)):
                return
        self.list_of_products.append(new_product)

    def remove_product(self, product):
        """
        Remove a product from the store.
        :param product: product to remove
        :return: None
        """
        if product in self.list_of_products:
            self.list_of_products.remove(product)

    def get_total_quantity(self):
        """
        Return the total quantity of the product in the store.
        """
        return sum(product.quantity for product in self.list_of_products)

    def get_all_products(self):
        """
        Return a list of all products in the store.
        """
        return [product for product in self.list_of_products if product.is_active()]

    def get_product_type_quantity(self):
        """
        Return how many different items are active in the store inventory.
        """
        return sum(1 for product in self.list_of_products if product.is_active())

    @staticmethod
    def validate_shopping_list_format(shopping_list):
        """
        Validate the shopping list format. Other checks are also needed
        and they are done elsewhere.
        :param shopping_list: The shopping list. A list of tuples (product, quantity).
        :return: A tuple: (True/False, message string) where message is why the
                 shopping list is invalid or ok if format is fine.
        """
        for item in shopping_list:
            if not isinstance(item, tuple):
                return (False, "Shopping list format is wrong. "
                               "List items are not all tuples")
            if len(item) != 2:
                return (False, "Shopping list format is wrong. "
                               "List items are not all tuples  of length 2")
            product, quantity = item
            if not isinstance(product, products.ImmaterialProduct) or not isinstance(quantity, int):
                print(product)
                return (False, "Shopping list format is wrong. "
                               "Products are not all inherited from ImmaterialProduct")
        return True, "Shopping list format is correct"

    @staticmethod
    def merge_shopping_list_items(shopping_list):
        """
        If the same product is listed more than once, merge them into one.
        :param shopping_list: A list of tuples. Each tuple == (Product instance, quantity)
        """
        # If same product is ordered twice inside the same order, combine them
        unified_shopping_list = {}
        for product, quantity in shopping_list:
            if product in unified_shopping_list:
                unified_shopping_list[product] += quantity
            else:
                unified_shopping_list[product] = quantity
        return list(unified_shopping_list.items())


    def validate_shopping_list(self, shopping_list):
        """
        Validate the shopping list which the method "order" can accept.
        :param shopping_list: A list of tuples. Each tuple == (Product instance, quantity)
        :return: If valid: True, "No errors"
                 If not:   False, "Error message"
        """
        validation_result, message = self.validate_shopping_list_format(shopping_list)
        if validation_result is False:
            return validation_result, message

        # If same product is ordered twice inside the same order, combine them
        unified_shopping_list = self.merge_shopping_list_items(shopping_list)
        for product, quantity in unified_shopping_list:
            if product not in self.list_of_products:
                return False, f"Product {product.name} is not in the store"
            precheck_result, message =  product.precheck_purchase(quantity)
            if precheck_result is False:
                return False, message
        return True, "No errors"

    def order(self, shopping_list):
        """
        Process the shopping list. Reduce quantity of products in the store accordingly.
        :param shopping_list: A list of tuples. Each tuple == (Product instance, quantity)
        :return if successful: (float/int, str) price of purchase, "Order completed successfully."
        :return if not successful: (None, str) None, Error message
        """
        validation_result, message = self.validate_shopping_list(shopping_list)
        if validation_result is not True:
            return None, message
        return (sum(product.buy(quantity)[0] for product, quantity in shopping_list),
                "Order completed successfully.")

    def __contains__(self, item):
        return item in self.list_of_products

    def __add__(self, other):
        new_store = Store([])
        for product in self.list_of_products:
            new_store.add_product(product)
        for product in other.list_of_products:
            new_store.add_product(product)
        return new_store

def main():
    """
    This was code given in the exercise to test the class.
    """
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
