from kakao.const.xpaths import *
from kakao.const.black_list import *
from kakao.const.class_name import *
from driver.driver_const import *

from time import sleep
from selenium.webdriver.common.by import By

PAGE_DOWN_CNT = 3


class KakaoDriver(object):
    def __init__(self, driver, builder):
        self.driver = driver
        self.builder = builder

        self.category_name = None
        self.sub_category_name = None

    def execute(self):
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
                if not self._is_in_black(category_idx, sub_category_idx):
                    # black list에 포함되지 않는 경우에만 다음 페이지를 조회
                    self.find_items_in_page()  # item 목록을 찾는다
                else:
                    self.click(CATEGORY_CANCEL_BUTTON)  # cateogory를 선택하지 못했다면 카테고리 선택 창을 닫는다
                self.sub_category_name = None
            self.category_name = None

    def get_first_category_size(self):
        """
        첫 번째 카테고리 크기를 계산
        :return: 첫 번째 카테고리 크기
        """
        self.click(CATEGORY_BUTTON)
        res = len(self.driver.xpath(CATEGORY_LIST)
                  .find_elements(By.CLASS_NAME, CATEGORY_LIST))
        self.click(CATEGORY_CANCEL_BUTTON)
        return res

    def get_second_category_size(self, category_idx: int):
        """
        두 번째 카테고리 크기를 계산
        :param category_idx: 카테고리 인덱스
        :return: 두 번째 카테고리 크기
        """
        self.click(CATEGORY_BUTTON)
        self.click(CATEGORY_ELEMENT.format(i=category_idx))
        sub_category_list = self.driver.xpath(SUB_LIST.format(i=category_idx - 1))
        text_menus = sub_category_list.find_elements(By.CLASS_NAME, CATEGORY_LIST)
        self.click(CATEGORY_CANCEL_BUTTON)
        return len(text_menus)

    def _is_in_black(self, category_idx: int, sub_category_idx: int) -> bool:
        self.click(CATEGORY_BUTTON)  # category 버튼 클릭

        # first category 확인
        category_name = self.driver.xpath(CATEGORY_ELEMENT.format(i=category_idx)).text
        if category_name in BLACK_LIST:
            return True
        self.category_name = category_name  # black list에 포함되지 않는다면 category_name을 설정
        self.click(CATEGORY_ELEMENT.format(i=category_idx))  # black list에 포함되지 않는다면 category를 선택함

        # second category 확인
        sub_category_name = self.driver.xpath(SUB_CATEGORY_ELEMENT
                                              .format(i=category_idx - 1, j=sub_category_idx + 1)).text
        if sub_category_name in BLACK_LIST:
            return True
        self.sub_category_name = sub_category_name  # black list에 포함되지 않는다면 sub_category_name 설정
        self.click(SUB_CATEGORY_ELEMENT.format(i=category_idx - 1, j=sub_category_idx + 1))  # black list에 포함되지 않는다면 sub category 선택
        sleep(SHORT_TIME)
        return False

    def fill_category_builder(self):
        (self.builder
         .category(self.category_name)
         .sub_category(self.sub_category_name))

    def page_down(self):
        last_height = self.driver.get_height()
        for _ in range(PAGE_DOWN_CNT):
            self.driver.page_end()
            new_height = self.driver.get_height()
            sleep(LONG_TIME)
            if new_height == last_height:
                break
            last_height = new_height

    def find_items_in_page(self):
        self.click(ITEM_BUTTON)  # 페이지에 들어가면 item에 대한 항목으로 페이지 기준을 변경
        self.fill_category_builder()  # builder에 category, sub category 이름을 추가
        self.page_down()
        item_lists = self.driver.find_elements(By.CLASS_NAME, ITEM_LIST)
        for item_list in item_lists:
            elements = item_list.find_elements(By.CLASS_NAME, ITEM)
            self.fill_category_builder()
            for elem in elements:
                item = self.find_item(elem)

    def find_item(self, element):
        item_image_url = element.find_element(By.CLASS_NAME, ITEM_IMAGE_URL).get_attribute('src')
        brand_name = element.find_element(By.CLASS_NAME, ITEM_BRAND).text
        item_name = element.find_element(By.CLASS_NAME, ITEM_NAME).text
        price = element.find_element(By.CLASS_NAME, ITEM_PRICE).text

        return (self.builder
                .item_image_url(item_image_url)
                .brand_name(brand_name)
                .item_name(item_name)
                .price(price)
                .build())

    def click(self, path: str, time=SHORT_TIME):
        sleep(time)
        self.driver.click(path)
        sleep(time)
