
class OrderItem:
    def __init__(self, id, customer_name, customer_lastname, order_type_id, paper_size_id):
        self.id = id
        self.customer_name = customer_name
        self.customer_lastname = customer_lastname
        self.order_type_id = order_type_id
        self.paper_size_id = paper_size_id

    
    @property
    def get_id(self):
        return self.id

    @property
    def get_customer_name(self):
        return self.customer_name

    @property
    def get_customer_lastname(self):
        return self.customer_lastname
    
    @property
    def get_order_type_id(self):
        return self.order_type_id
    
    @property
    def get_paper_size_id(self):
        return self.paper_size_id