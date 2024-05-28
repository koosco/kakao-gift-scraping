from driver.kakao.kakao_driver_builder import KakaoDriverBuilder


class ScrapingService(object):
    def __init__(self):
        self.driver = KakaoDriverBuilder().configure()

    def find_all(self):
        self.driver.