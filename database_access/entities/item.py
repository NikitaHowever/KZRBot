
class Item:
    def __init__(self, id, name, material, description, has_one_size,
                    paper_size_id, price_for_pack, price_for_displaybox):

                    self.id = id
                    self.name = name
                    self.material = material
                    self.description = description
                    self.has_one_size = has_one_size
                    self.paper_size_id = has_one_size if paper_size_id else None
                    self.price_for_pack = price_for_pack
                    self.price_for_displaybox = price_for_displaybox
    

    @property
    def get_id(self):
        return self.id

    @property
    def get_name(self):
        return self.name

    @property
    def get_material(self):
        return self.get_material
    
    @property
    def get_descriptiom(self):
        return self.description

    @property
    def get_has_one_size(self):
        return self.has_one_size

    @property
    def get_paper_size_id(self):
        return self.paper_size_id
    
    @property
    def get_price_for_pack(self):
        return self.price_for_pack
    
    @property
    def get_price_for_displaybox(self):
        return self.price_for_displaybox
