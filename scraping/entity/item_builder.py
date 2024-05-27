from scraping.entity.item import Item
from scraping.PriceProcessor import PriceProcessor

from copy import deepcopy


class ItemBuilder:
    def __init__(self):
        self.__item = Item()

    def item_image_url(self, image_url):
        self.__item.item_image_url = image_url
        return self

    def brand_name(self, brand_name):
        self.__item.brand_name = brand_name
        return self

    def item_name(self, item_name):
        self.__item.item_name = item_name
        return self

    def price(self, str_price):
        price = PriceProcessor.proceed(str_price)
        self.__item.price = price
        return self

    def category(self, category):
        self.__item.category = category
        return self

    def sub_category(self, sub_category):
        self.__item.sub_category = sub_category
        return self

    def option_name(self, option_name):
        self.__item.option_name = option_name
        return self

    def build(self):
        ret = deepcopy(self.__item)
        category_name = self.__item.category
        sub_category = self.__item.sub_category
        self.__item = Item()
        self.__item.category = category_name
        self.__item.sub_category = sub_category
        return ret
