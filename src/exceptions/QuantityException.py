class QuantityException(Exception):
    def __init__(self, *args, op):
        super().__init__(args)

    def __str__(self):
        return self