from abc import ABC, abstractmethod

class Promotion(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity):
        pass

    def __str__(self):
        return self.name

class SecondHalfPrice(Promotion):
    @staticmethod
    def apply_promotion(product, quantity):
        return product.get_price() * (quantity - (quantity // 2) / 2)


class ThirdOneFree(Promotion):
    @staticmethod
    def apply_promotion(product, quantity):
        return product.get_price() * (quantity - (quantity // 3))

class PercentDiscount(Promotion):
    def __init__(self, name, percent):
        super().__init__(name)
        self._discount_percent = percent

    def apply_promotion(self, product, quantity):
        return product.get_price() * quantity * (1 - self._discount_percent / 100)