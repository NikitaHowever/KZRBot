
class Order:
    def __init__(self, id, customer_name, customer_lastname,customer_phone,customer_email,customer_post_index,boxberry_track_number, 
    order_type_id, paper_size_id, order_status_id, unique_order_id):
        self.id = id
        self.customer_name = customer_name
        self.customer_lastname = customer_lastname
        self.customer_phone = customer_phone
        self.customer_email = customer_email
        self.customer_post_index = customer_post_index
        self.boxberry_track_number = boxberry_track_number
        self.order_type_id = order_type_id
        self.paper_size_id = paper_size_id
        self.order_status_id = order_status_id
        self.unique_order_id = unique_order_id

    
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

    @property
    def get_order_status_id(self):
        return self.order_status_id

    @property
    def get_unique_order_id(self):
        return self.unique_order_id

    @property
    def get_customer_email(self):
        return self.customer_email


    @property
    def get_customer_phone(self):
        return self.customer_phone

    @property
    def get_customer_post_index(self):
        return self.customer_post_index
    

    @property
    def get_boxberry_track_number(self):
        return self.boxberry_track_number