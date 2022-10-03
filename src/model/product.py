class Product:
    def __init__(self, id, quantity, name):
        self.id = id
        self.quantity = quantity
        self.name = name

    def serialize(self):
        return {
            'id': self.id,
            'quantity': self.quantity,
            'name': self.name,
        }
