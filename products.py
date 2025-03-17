
class Product:

    def __init__(self, name, price, quantity):
        """
        Initialize the product.
        :param name: name of the product
        :param price: price of the product
        :param quantity: quantity of the product
        """
        if not isinstance(name, str) or not isinstance(price, int) or not isinstance(quantity, int):
            raise TypeError("One of the arguments to Product is invalid")
        if not len(name) > 0 or price < 0 or quantity < 0:
            raise ValueError("One of the arguments to Product is invalid")
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True

    def get_quantity(self):
        """
        Return the quantity of the product.
        """
        return self.quantity

    def set_quantity(self, quantity):
        """
        Set the quantity of the product.
        """
        self.quantity = quantity

    def is_active(self):
        """
        Test if the product is active.
        """
        return self.active

    def activate(self):
        """
        Activate the product.
        """
        self.active = True

    def deactivate(self):
        """
        Deactivate the product.
        """
        self.active = False

    def show(self, quantity=None):
        """
        Return the product name, price and quantity in a string.
        """
        return f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}"

    def name_and_price(self, quantity=1):
        """
        Return the product name and price based on given quantity.
        """
        return self.name, self.price * quantity

    def buy(self, quantity):
        """
        Reduce the product in the storage through a purchase.
        :param quantity: How many products are being purchased.
        :return: The total price of the purchase.
        """
        if quantity > self.quantity:
            raise ValueError("Quantity is greater than product quantity")
        self.quantity -= quantity
        if self.quantity == 0:
            self.deactivate()
        return quantity * self.price


def main():
    """
    Test the Product class
    :return:
    """
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active())

    print(bose.show())
    print(mac.show())


if __name__ == "__main__":
    main()