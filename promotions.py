"""
Promotion classes are used in Best Buy to define product price discounts of different types.
"""

from abc import ABC, abstractmethod


class Promotion(ABC):
    """
    Abstract base class for all promotions.
    """
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity):
        """
        Abstract method to apply a promotion to a product.
        Classes which inherit from Promotion must implement this method.
        :param product: instance of one of the product classes.
        :param quantity: How many products are being bought
        :return: The price after applying the promotion.
        """
        pass

    def __str__(self):
        return self.name

class SecondHalfPrice(Promotion):
    """
    Defines a promotion where the second product is half price.
    """
    @staticmethod
    def apply_promotion(product, quantity):
        return product.get_price() * (quantity - (quantity // 2) / 2)


class ThirdOneFree(Promotion):
    """
    Defines a promotion where the third product is a free product.
    """
    @staticmethod
    def apply_promotion(product, quantity):
        return product.get_price() * (quantity - (quantity // 3))

class PercentDiscount(Promotion):
    """
    Defines a promotion where the percent discount is applied.
    Discount percentage is defined at the time the instance is
    created.
    """
    def __init__(self, name, percent):
        """
        Constructor.
        """
        super().__init__(name)
        self._discount_percent = percent

    def apply_promotion(self, product, quantity):
        """
        Calculates the product discount percentage.
        :param product:
        :param quantity:
        :return:
        """
        return product.get_price() * quantity * (1 - self._discount_percent / 100)
