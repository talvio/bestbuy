"""
Various product classes for the Store class to use.
"""

import promotions


class ImmaterialProduct:
    """
    Class representing a product. Since the product is immaterial, there
    is a limitless supply.
    This is the base class for all product classes.
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

    def __gt__(self, other):
        """ Overload > operator. """
        return self.get_price() > other.get_price()

    def __lt__(self, other):
        """ Overload < operator. """
        return self.get_price() < other.get_price()

    def __str__(self):
        """
        Return the product name, price and quantity in a string.
        """
        return f"{self.name}, Price: ${self._price}, "\
               f"Quantity: Unlimited, Promotion: {self._promotion}"

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
        """
        Check if it is possible to purchase the product in the quantity defined.
        :param quantity: How many products are being purchased.
        :return: Tuple (True/False, message) Message explain why the product cannot be purchased.
        """
        if not isinstance(quantity, int) or quantity <= 0:
            return False, "impossible quantity given"
        return True, "purchase ok" if self.is_active() else (False, "product not active")

    def set_promotion(self, promotion):
        """
        Attach a promotion to the product.
        :param promotion: Promotion object.
        :return: None
        """
        if not isinstance(promotion, promotions.Promotion):
            raise TypeError("promotion must be of type promotions.Promotion")
        self._promotion = promotion

class Product(ImmaterialProduct):
    """
    Class representing a product.
    The major difference from ImmaterialProduct:
    There is a defined number of the product available.
    """
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
        self._active = quantity > 0

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
        self._active = quantity > 0

    def __str__(self):
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
        self.set_quantity(self.get_quantity() - quantity)
        return purchase_result, message

    def precheck_purchase(self, quantity=1):
        """
        Check if it is possible to purchase the product in the quantity defined.
        :param quantity: How many products are being purchased.
        :return: Tuple (True/False, message) Message explain why the product cannot be purchased.
        """
        precheck, message = super().precheck_purchase(quantity)
        if precheck is False:
            return False, message
        if quantity > self._quantity:
            return (False, f"there are only {self._quantity} pieces of {self.name}. "
                           f"Cannot sell {quantity}")
        return precheck, message


class LimitedImmaterialProduct(ImmaterialProduct):
    """
    Limited immaterial product can be sold only a defined amount in one order.
    """
    def __init__(self, name, price, maximum=1):
        """
        Initialize the product.
        :param name: Name of the product.
        :param price: Price of the product.
        :param maximum: How many of the product can be included in one order.
        """
        super().__init__(name, price)
        self.__maximum = maximum

    def __str__(self):
        """
        Return the product name, price and quantity in a string.
        """
        return (f"{self.name}, Price: ${self._price} "
                f" Limited to {self.__maximum} per order!, "
                f"Promotion: {self._promotion}")

    def precheck_purchase(self, quantity=1):
        """
        Check if it is possible to purchase the product in the quantity defined.
        :param quantity: How many products are being purchased.
        :return: Tuple (True/False, message) Message explain why the product cannot be purchased.
        """
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

    def __str__(self):
        """
        Return the product name, price and quantity in a string.
        """
        return (f"{self.name}, Price: ${self._price}, "
                f"Quantity: {self._quantity}, "
                f"Limited to {self.__maximum} per order!, "
                f"Promotion: {self._promotion}")

    def precheck_purchase(self, quantity=1):
        """
        Check if it is possible to purchase the product in the quantity defined.
        :param quantity: How many products are being purchased.
        :return: Tuple (True/False, message) Message explain why the product cannot be purchased.
        """
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
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    service = ImmaterialProduct("Service", price=1000)
    service.buy(2)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active())

    print(bose)
    print(mac)


if __name__ == "__main__":
    main()
