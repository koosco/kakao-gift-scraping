import import_django

from item_service.models import *

from scraping.PriceProcessor import PriceProcessor

from copy import deepcopy


class ItemBuilder:
    def __init__(self):
        self.__item = Item()

    def item_image_url(self, image_url: str):
        self.__item.item_image_url = image_url
        return self

    def brand_name(self, brand_name: str):
        self.__item.brand_name = brand_name
        return self

    def item_name(self, item_name: str):
        self.__item.item_name = item_name
        return self

    def price(self, str_price: str):
        price = PriceProcessor.proceed(str_price)
        self.__item.item_price = price
        return self

    def category(self, category: str):
        self.__item.category = category
        return self

    def sub_category(self, sub_category: str):
        self.__item.sub_category = sub_category
        return self

    def option_name(self, option_name: str):
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
