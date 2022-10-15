from src.constants import *

from src.exceptions.IdException import IdException
from src.exceptions.NameException import NameException
from src.exceptions.QuantityException import QuantityException

class Product:
    def __init__(self, id:int, quantity:int, name:str):
        self.id = id
        self.quantity = quantity
        self.name = name

    def serialize(self):
        return {
            'id': self.id,
            'quantity': self.quantity,
            'name': self.name,
        }
