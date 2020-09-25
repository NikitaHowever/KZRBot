class Item:
    def __init__(self, id, name, unit_name,nds,price,quantity):
        self.id = id
        self.name = name
        self.unit_name = unit_name
        self.nds = nds
        self.price = price
        self.quantity = quantity

    
    @property
    def get_id(self):
        return self.id
    

    @property
    def get_name(self):
        return self.name

    @property
    def get_unit_name(self):
        return self.unit_name

    @property
    def get_nds(self):
        return self.nds

    @property
    def get_price(self):
        return self.price

    @property
    def get_quantity(self):
        return self.quantity