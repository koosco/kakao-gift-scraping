class Item:
    def __init__(self):
        self.item_image_url: str = None
        self.brand_name: str = None
        self.item_name: str = None
        self.price: int = None
        self.category: str = None
        self.sub_category: str = None
        self.option_name: str = None

    def __repr__(self):
        ret = ''
        ret += 'item_image_url: ' + self.item_image_url + '\n'
        ret += 'brand_name: ' + self.brand_name + '\n'
        ret += 'item_name: ' + self.item_name + '\n'
        ret += 'price: ' + str(self.price) + '\n'
        ret += 'category: ' + self.category + '\n'
        ret += 'sub_category: ' + self.sub_category + '\n'
        # ret += 'option_name: ' + self.option_name + '\n'
        return ret