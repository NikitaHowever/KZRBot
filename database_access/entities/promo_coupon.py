
class PromoCoupon:
    def __init__(self, id, name, coupon_value, coupon_discount_percent):
        self.id = id
        self.name = name
        self.coupon_value = coupon_value
        self.coupon_discount_percent = coupon_discount_percent
    

    @property
    def get_id(self):
        return self.id
    
    @property
    def get_name(self):
        return self.name

    @property
    def get_coupon_value(self):
        return self.coupon_value
    
    @property
    def get_coupon_discount_percent(self):
        return self.coupon_discount_percent