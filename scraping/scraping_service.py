from driver.kakao.kakao_driver_builder import KakaoDriverBuilder


class ScrapingService(object):
    def __init__(self):
        self.driver = KakaoDriverBuilder().configure()

    def get_all_items(self):
        first_category_size = self.driver.get_first_category_size()
        for category_idx in range(first_category_size):
            self.driver.scrap_category(category_idx)


if __name__ == '__main__':
    service = ScrapingService()
    service.get_all_items()