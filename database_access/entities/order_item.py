class Order:
    def __init__(self, order_id, item_id, amount):
        self.order_id = order_id
        self.item_id = item_id
        self.amount = amount

    
    @property
    def get_order_id(self):
        return self.order_id
    
    @property
    def get_item_id(self):
        return self.item_id
    
    @property
    def get_item_amount(self):
        return self.amount