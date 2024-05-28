from basic.basic_driver_configurer import BasicDriverConfigurer


class KakaoDriverConfigurer(BasicDriverConfigurer):
    def __init__(self):
        super().__init__()
        self.url = 'https://gift.kakao.com/home'
