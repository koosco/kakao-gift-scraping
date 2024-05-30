import import_django

from item_service.models import *

from driver.basic.basic_driver import BasicDriver
from driver.kakao.const.xpaths import *
from driver.kakao.const.black_list import *
from driver.kakao.const.class_name import *
from driver.driver_const import *

from time import sleep
from selenium.webdriver.common.by import By

PAGE_DOWN_CNT = 3


class KakaoDriver(object):
    def __init__(self, driver: BasicDriver, item_builder):
        self._driver = driver
        self._item_builder = item_builder

        self._category_name = None
        self._sub_category_name = None

    def scrap_all(self):
        """
        driver를 이용해 카카오 선물하기 페이지에서 scraping을 수행
        * category를 전부 순회하며 item을 탐색한다
        :return: None
        """
        category_size = self.get_first_category_size()  # first category 길이
        for category_idx in range(1, category_size + 1):
            sub_category_size = self.get_second_category_size(category_idx)  # second category 길이
            for sub_category_idx in range(sub_category_size):
                sleep(TIME_SHORT_TIME)
                self.main_logic(category_idx, sub_category_idx)
                self._sub_category_name = None
            self._category_name = None

    def scrap_category(self, category_idx: int):
        """
        하나의 카테고리에 대해 scraping 수행
        :param category_idx: scrap할 페이지 idx
        :return: 카테고리에 포함된 항목들
        """
        category_idx += 1
        sub_category_size = self.get_second_category_size(category_idx)  # second category 길이
        for sub_category_idx in range(sub_category_size):
            sleep(TIME_SHORT_TIME)
            self.main_logic(category_idx, sub_category_idx)

    def scrap_sub_category(self, category_idx: int, sub_category_idx: int):
        category_idx += 1
        sleep(TIME_SHORT_TIME)
        self.main_logic(category_idx, sub_category_idx)

    def main_logic(self, category_idx, sub_category_idx):
        if not self.__is_in_black(category_idx, sub_category_idx):
            # black list에 포함되지 않는 경우에만 다음 페이지를 조회
            items = self.__find_items_in_page()  # item 목록을 찾는다
            # Item.objects.bulk_create(items)
        else:
            self._click(XPATH_CATEGORY_CANCEL_BUTTON)  # cateogory를 선택하지 못했다면 카테고리 선택 창을 닫는다

    def get_first_category_size(self):
        """
        첫 번째 카테고리 크기를 계산
        :return: 첫 번째 카테고리 크기
        """
        self._click(XPATH_CATEGORY_BUTTON, TIME_SHORT_TIME)
        res = len(self._driver._xpath(XPATH_CATEGORY_LIST)
                  .find_elements(By.CLASS_NAME, CLASS_CATEGORY_LIST))
        self._click(XPATH_CATEGORY_CANCEL_BUTTON, TIME_SHORT_TIME)
        return res

    def get_second_category_size(self, category_idx: int):
        """
        두 번째 카테고리 크기를 계산
        :param category_idx: 카테고리 인덱스
        :return: 두 번째 카테고리 크기
        """
        self._click(XPATH_CATEGORY_BUTTON, TIME_SHORT_TIME)
        self._click(XPATH_CATEGORY_ELEMENT.format(i=category_idx), TIME_SHORT_TIME)
        sub_category_list = self._driver._xpath(XPATH_SUB_LIST.format(i=category_idx - 1))
        text_menus = sub_category_list.find_elements(By.CLASS_NAME, CLASS_CATEGORY_LIST)
        self._click(XPATH_CATEGORY_CANCEL_BUTTON, TIME_SHORT_TIME)
        return len(text_menus)

    def __is_in_black(self, category_idx: int, sub_category_idx: int) -> bool:
        self._click(XPATH_CATEGORY_BUTTON)  # category 버튼 클릭

        # first category 확인
        category_name = self._driver._xpath(XPATH_CATEGORY_ELEMENT.format(i=category_idx)).text
        if category_name in BLACK_LIST:
            return True
        self._category_name = category_name  # black list에 포함되지 않는다면 category_name을 설정
        self._click(XPATH_CATEGORY_ELEMENT.format(i=category_idx))  # black list에 포함되지 않는다면 category를 선택함

        # second category 확인
        sub_category_name = self._driver._xpath(XPATH_SUB_CATEGORY_ELEMENT
                                                .format(i=category_idx - 1, j=sub_category_idx + 1)).text
        if sub_category_name in BLACK_LIST:
            return True
        self._sub_category_name = sub_category_name  # black list에 포함되지 않는다면 sub_category_name 설정
        self._click(XPATH_SUB_CATEGORY_ELEMENT.format(i=category_idx - 1,
                                                      j=sub_category_idx + 1))  # black list에 포함되지 않는다면 sub category 선택
        sleep(TIME_SHORT_TIME)
        return False

    def __fill_category_builder(self):
        (self._item_builder
         .category(self._category_name)
         .sub_category(self._sub_category_name))

    def __go_page_end(self):
        for _ in range(PAGE_DOWN_CNT):
            self.__send_end()
            sleep(TIME_MEDIUM_TIME)
        sleep(TIME_MEDIUM_TIME)

    def __send_end(self):
        self._driver._end()

    def __send_page_down(self):
        self._driver._page_down()

    def __find_items_in_page(self):
        stop_flag = False
        items = []
        self._click(XPATH_ITEM_BUTTON)  # 페이지에 들어가면 item에 대한 항목으로 페이지 기준을 변경
        self.__fill_category_builder()  # builder에 category, sub category 이름을 추가
        self.__go_page_end()
        item_lists = self._driver._class_name(CLASS_ITEM_LIST)  # 각각의 아이템 목록들 (추천 항목 제외)
        self._driver._home()
        for item_list in item_lists:
            elements = item_list.find_elements(By.CLASS_NAME, CLASS_ITEM)  # 아이템 목록에서 아이템들을 찾음
            self.__fill_category_builder()  # 카테고리 항목을 채우고
            for elem in elements:
                item = self.__find_item(elem)
                if item:
                    items.append(item)  # 아이템을 dto로 만듬
                else:
                    stop_flag = True
                    break
            if stop_flag:
                break
        return items

    def __find_item(self, element):
        while 'mud' in element.find_element(By.CLASS_NAME, CLASS_ITEM_NAME).text:
            self._driver.go_to_element(element)
            sleep(TIME_VERY_SHORT_TIME)
        try:
            self._driver.go_to_element(element)
            sleep(TIME_SHORT_TIME)
            item_name = element.find_element(By.CLASS_NAME, CLASS_ITEM_NAME).text
            print('item name')
            print(item_name)
            item_image_url = element.find_element(By.CLASS_NAME, CLASS_ITEM_IMAGE_URL).get_attribute('src')
            print('item image url')
            print(item_image_url)
            if 'mud' in item_image_url:
                print('save point')
            brand_name = element.find_element(By.CLASS_NAME, CLASS_ITEM_BRAND).text
            price = element.find_element(By.CLASS_NAME, CLASS_ITEM_PRICE).text

            return (self._item_builder
                    .item_image_url(item_image_url)
                    .brand_name(brand_name)
                    .item_name(item_name)
                    .price(price)
                    .build())
        except Exception as e:
            print()
            print('====error found====')
            print(e)
            return None
        # try:
        #     self._driver.go_to_element(element)
        #     sleep(TIME_SHORT_TIME)
        #     item_name = element.find_element(By.CLASS_NAME, CLASS_ITEM_NAME).text
        #     print('item name')
        #     print(item_name)
        #     item_image_url = element.find_element(By.CLASS_NAME, CLASS_ITEM_IMAGE_URL).get_attribute('src')
        #     print('item image url')
        #     print(item_image_url)
        #     if 'mud' in item_image_url:
        #         print('save point')
        #     brand_name = element.find_element(By.CLASS_NAME, CLASS_ITEM_BRAND).text
        #     price = element.find_element(By.CLASS_NAME, CLASS_ITEM_PRICE).text
        #
        #     return (self._item_builder
        #             .item_image_url(item_image_url)
        #             .brand_name(brand_name)
        #             .item_name(item_name)
        #             .price(price)
        #             .build())
        # except Exception as e:
        #     print()
        #     print('====error found====')
        #     print(e)
        #     return None

    def _click(self, path: str, time=TIME_VERY_SHORT_TIME):
        sleep(time)
        self._driver._click(path)
        sleep(time)
