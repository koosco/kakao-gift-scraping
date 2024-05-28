from basic.basic_driver import BasicDriver
from kakao.const.xpaths import *
from kakao.const.black_list import *
from kakao.const.class_name import *
from driver.driver_const import *

from time import sleep
from selenium.webdriver.common.by import By

PAGE_DOWN_CNT = 3


class KakaoDriver(object):
    def __init__(self, driver: BasicDriver, item_builder):
        super().__init__(driver)
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
                sleep(SHORT_TIME)
                if not self.__is_in_black(category_idx, sub_category_idx):
                    # black list에 포함되지 않는 경우에만 다음 페이지를 조회
                    self.__find_items_in_page()  # item 목록을 찾는다
                else:
                    self._click(CATEGORY_CANCEL_BUTTON)  # cateogory를 선택하지 못했다면 카테고리 선택 창을 닫는다
                self._sub_category_name = None
            self._category_name = None

    def scrap_category(self, category_idx: int):
        """
        하나의 카테고리에 대해 scraping 수행
        :param category_idx: scrap할 페이지 idx
        :return: 카테고리에 포함된 항목들
        """
        sub_category_size = self.get_second_category_size(category_idx)  # second category 길이
        for sub_category_idx in range(sub_category_size):
            sleep(SHORT_TIME)
            if not self.__is_in_black(category_idx, sub_category_idx):
                # black list에 포함되지 않는 경우에만 다음 페이지를 조회
                return self.__find_items_in_page()  # item 목록을 찾는다
            else:
                self._click(CATEGORY_CANCEL_BUTTON)  # cateogory를 선택하지 못했다면 카테고리 선택 창을 닫는다

    def scrap_sub_category(self, category_idx: int, sub_category_idx: int):
        sleep(SHORT_TIME)
        if not self.__is_in_black(category_idx, sub_category_idx):
            # black list에 포함되지 않는 경우에만 다음 페이지를 조회
            return self.__find_items_in_page()  # item 목록을 찾는다
        else:
            self._click(CATEGORY_CANCEL_BUTTON)  # cateogory를 선택하지 못했다면 카테고리 선택 창을 닫는다

    def get_first_category_size(self):
        """
        첫 번째 카테고리 크기를 계산
        :return: 첫 번째 카테고리 크기
        """
        self._click(CATEGORY_BUTTON)
        res = len(self._driver._xpath(CATEGORY_LIST)
                  .find_elements(By.CLASS_NAME, CATEGORY_LIST))
        self._click(CATEGORY_CANCEL_BUTTON)
        return res

    def get_second_category_size(self, category_idx: int):
        """
        두 번째 카테고리 크기를 계산
        :param category_idx: 카테고리 인덱스
        :return: 두 번째 카테고리 크기
        """
        self._click(CATEGORY_BUTTON)
        self._click(CATEGORY_ELEMENT.format(i=category_idx))
        sub_category_list = self._driver._xpath(SUB_LIST.format(i=category_idx - 1))
        text_menus = sub_category_list.find_elements(By.CLASS_NAME, CATEGORY_LIST)
        self._click(CATEGORY_CANCEL_BUTTON)
        return len(text_menus)

    def __is_in_black(self, category_idx: int, sub_category_idx: int) -> bool:
        self._click(CATEGORY_BUTTON)  # category 버튼 클릭

        # first category 확인
        category_name = self._driver._xpath(CATEGORY_ELEMENT.format(i=category_idx)).text
        if category_name in BLACK_LIST:
            return True
        self._category_name = category_name  # black list에 포함되지 않는다면 category_name을 설정
        self._click(CATEGORY_ELEMENT.format(i=category_idx))  # black list에 포함되지 않는다면 category를 선택함

        # second category 확인
        sub_category_name = self._driver._xpath(SUB_CATEGORY_ELEMENT
                                                .format(i=category_idx - 1, j=sub_category_idx + 1)).text
        if sub_category_name in BLACK_LIST:
            return True
        self._sub_category_name = sub_category_name  # black list에 포함되지 않는다면 sub_category_name 설정
        self._click(SUB_CATEGORY_ELEMENT.format(i=category_idx - 1, j=sub_category_idx + 1))  # black list에 포함되지 않는다면 sub category 선택
        sleep(SHORT_TIME)
        return False

    def __fill_category_builder(self):
        (self._item_builder
         .category(self._category_name)
         .sub_category(self._sub_category_name))

    def __page_down(self):
        last_height = self._driver._get_height()
        for _ in range(PAGE_DOWN_CNT):
            self._driver._page_end()
            new_height = self._driver._get_height()
            sleep(LONG_TIME)
            if new_height == last_height:
                break
            last_height = new_height

    def __find_items_in_page(self):
        items = []
        self._click(ITEM_BUTTON)  # 페이지에 들어가면 item에 대한 항목으로 페이지 기준을 변경
        self.__fill_category_builder()  # builder에 category, sub category 이름을 추가
        self.__page_down()
        item_lists = self._driver.find_elements(By.CLASS_NAME, ITEM_LIST)  # 각각의 아이템 목록들 (추천 항목 제외)
        for item_list in item_lists:
            elements = item_list.find_elements(By.CLASS_NAME, ITEM)  # 아이템 목록에서 아이템들을 찾음
            self.__fill_category_builder()  # 카테고리 항목을 채우고
            for elem in elements:
                items.append(self.__find_item(elem))  # 아이템을 dto로 만듬
        return items

    def __find_item(self, element):
        item_image_url = element.find_element(By.CLASS_NAME, ITEM_IMAGE_URL).get_attribute('src')
        brand_name = element.find_element(By.CLASS_NAME, ITEM_BRAND).text
        item_name = element.find_element(By.CLASS_NAME, ITEM_NAME).text
        price = element.find_element(By.CLASS_NAME, ITEM_PRICE).text

        return (self._item_builder
                .item_image_url(item_image_url)
                .brand_name(brand_name)
                .item_name(item_name)
                .price(price)
                .build())

    def _click(self, path: str, time=SHORT_TIME):
        sleep(time)
        self._driver._click(path)
        sleep(time)
