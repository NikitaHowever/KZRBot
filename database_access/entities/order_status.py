class OrderStatus:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    
    @property
    def get_id(self):
        return self.id

    @property
    def get_name(self):
        return self.name