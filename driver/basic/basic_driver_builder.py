from basic.basic_driver_configurer import BasicDriverConfigurer
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from basic.basic_driver import BasicDriver


class BasicDriverBuilder(object):
    def __init__(self):
        self.configurer = BasicDriverConfigurer()

    def url(self, url: str):
        self.configurer.url = url
        return self

    def headless(self, headless: bool):
        self.configurer.headless = headless
        return self

    def no_sandbox(self, no_sandbox: bool):
        self.configurer.no_sandbox = no_sandbox
        return self

    def has_pop_up(self, flag: bool):
        self.configurer.pop_up = flag
        return self

    def configure(self):
        chrome_options = Options()
        if self.configurer.headless:
            chrome_options.add_argument('--headless')
        if self.configurer.no_sandbox:
            chrome_options.add_argument('--no-sandbox')
        chrome_options.add_experimental_option('detach', True)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(options=chrome_options)
        if self.configurer.pop_up:
            handles = driver.window_handles
            for handle in handles:
                if handle != handles[0]:
                    driver.switch_to.window(handle)
                    driver.close()
            driver.switch_to.window(handles[0])
        return BasicDriver(driver)
