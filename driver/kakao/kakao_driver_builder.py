from basic.basic_driver_builder import BasicDriverBuilder
from driver.kakao.kakao_driver import KakaoDriver
from scraping.entity.item_builder import ItemBuilder
from driver.kakao.kakao_driver_configurer import KakaoDriverConfigurer


class KakaoDriverBuilder(BasicDriverBuilder):
    def __init__(self):
        super().__init__()
        self.configurer = KakaoDriverConfigurer()
        self.item_builder = ItemBuilder()

    def url(self, url: str):
        self.configurer.url = url
        return self

    def configure(self):
        driver = super().configure()
        kakao_driver = KakaoDriver(driver, self.item_builder)
        kakao_driver.open_url(self.configurer.url)

