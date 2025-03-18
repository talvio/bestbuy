import promotions

class ImmaterialProduct:
    """
    Class representing a product.
    """

    def __init__(self, name, price):
        """
        Initialize the product.
        :param name: name of the product
        :param price: price of the product
        """
        if not isinstance(name, str) or not isinstance(price, int):
            raise TypeError("One of the arguments to Product is invalid")
        if not len(name) > 0 or price < 0:
            raise ValueError("One of the arguments to Product is invalid")
        self.name = name
        self._price = price
        self._active = True
        self._promotion = None

    def is_active(self):
        """
        Test if the product is active.
        """
        return self._active

    def activate(self):
        """
        Activate the product.
        """
        self._active = True

    def deactivate(self):
        """
        Deactivate the product.
        """
        self._active = False

    def show(self):
        """
        Return the product name, price and quantity in a string.
        """
        return f"{self.name}, Price: ${self._price}, Quantity: Unlimited, Promotion: {self._promotion}"

    def get_price(self):
        """ Get the price of one product"""
        return self._price

    def name_and_price(self, quantity=1):
        """
        Return the product name and price based on given quantity.
        """
        if self._promotion is not None:
            return self.name, self._promotion.apply_promotion(self, quantity)
        return self.name, self._price * quantity

    def buy(self, quantity=1):
        """
        Return the price based on given quantity.
        :param quantity: How many products are being purchased.
        :return: The total price of the purchase.
        """
        precheck, message = self.precheck_purchase(quantity)
        if precheck is False:
            return False, message
        if self._promotion is not None:
            return self._promotion.apply_promotion(self, quantity), "Purchase was successful"
        return quantity * self._price, "Purchase was successful"

    def precheck_purchase(self, quantity=1):
        if not isinstance(quantity, int) or quantity <= 0:
            return False, "impossible quantity given"
        return True, "purchase ok" if self.is_active() else (False, "product not active")

    def set_promotion(self, promotion):
        if not isinstance(promotion, promotions.Promotion):
            raise TypeError("promotion must be of type promotions.Promotion")
        self._promotion = promotion

class Product(ImmaterialProduct):
    def __init__(self, name, price, quantity):
        """
        Initialize the product.
        :param name: name of the product
        :param price: price of the product
        :param quantity: quantity of the product
        """
        super().__init__(name, price)
        if not isinstance(quantity, int):
            raise TypeError("One of the arguments to Product is invalid")
        if quantity < 0:
            raise ValueError("One of the arguments to Product is invalid")
        self._quantity = quantity
        self._active = True if quantity > 0 else False

    def get_quantity(self):
        """
        Return the quantity of the product.
        """
        return self._quantity

    def set_quantity(self, quantity):
        """
        Set the quantity of the product.
        """
        self._quantity = quantity

    def show(self):
        """
        Return the product name, price and quantity in a string.
        """
        return (f"{self.name}, Price: ${self._price}, "
               f"Quantity: {self._quantity}, Promotion: {self._promotion}")

    def buy(self, quantity=1):
        """
        Reduce the product in the storage through a purchase.
        :param quantity: How many products are being purchased.
        :return: The total price of the purchase.
        """
        purchase_result, message = super().buy(quantity)
        if purchase_result is False:
            return False, message
        self._quantity -= quantity
        if self._quantity == 0:
            self.deactivate()
        return purchase_result, message

    def precheck_purchase(self, quantity=1):
        precheck, message = super().precheck_purchase(quantity)
        if precheck is False:
            return False, message
        if quantity > self._quantity:
            return (False, f"there are only {self._quantity} pieces of {self.name}. " 
                           f"Cannot sell {quantity}")
        return precheck, message


class LimitedImmaterialProduct(ImmaterialProduct):
    """
    Limited immaterial product can be sold only one at a time
    """
    def __init__(self, name, price, maximum=1):
        super().__init__(name, price)
        self.__maximum = maximum

    def show(self):
        """
        Return the product name, price and quantity in a string.
        """
        return (f"{self.name}, Price: ${self._price} "
                f" Limited to {self.__maximum} per order!, "
                f"Promotion: {self._promotion}")

    def precheck_purchase(self, quantity=1):
        precheck, message = super().precheck_purchase(quantity)
        if precheck is False:
            return False, message
        if quantity > self.__maximum:
            return (False, f"{self.name} is a limited product. " 
                           f"Only {self.__maximum} allowed in one purchase")
        return precheck, message


class LimitedProduct(Product, LimitedImmaterialProduct):
    """
    Limited product can be sold only one at a time
    """
    def __init__(self, name, price, quantity, maximum=1):
        super().__init__(name, price, quantity)
        self.__maximum = maximum

    def show(self):
        """
        Return the product name, price and quantity in a string.
        """
        return (f"{self.name}, Price: ${self._price}, "
                f"Limited to {self.__maximum} per order!, " 
                f"Promotion: {self._promotion}")

    def precheck_purchase(self, quantity=1):
        precheck, message = super().precheck_purchase(quantity)
        if precheck is False:
            return False, message
        if quantity > self.__maximum:
            return (False, f"{self.name} is a limited product. " 
                           f"Only {self.__maximum} allowed in one purchase")
        return precheck, message


def main():
    """
    Test the Product class
    :return:
    """
    product_list = [Product("MacBook Air M2", price=1450, quantity=100),
                    Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    Product("Google Pixel 7", price=500, quantity=250),
                    ImmaterialProduct("Windows License", price=125),
                    ImmaterialProduct("XYZ Service Contract", price=400),
                    LimitedImmaterialProduct("Shipping", price=10, maximum=1),
                    LimitedProduct("Rare coffee", price=100, maximum=1, quantity=100),
                    ]

    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    service = ImmaterialProduct("Service", price=1000)
    service.buy(2)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active())

    print(bose.show())
    print(mac.show())


if __name__ == "__main__":
    main()
