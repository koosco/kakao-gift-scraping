from basic.basic_driver_builder import BasicDriverBuilder
from kakao.kakao_driver_configurer import KakaoDriverConfigurer


class KakaoDriverBuilder(BasicDriverBuilder):
    def __init__(self):
        super().__init__()
        self.configurer = KakaoDriverConfigurer()

    def configure(self):
        self.url(self.configurer.url)
        return super().configure()
