from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from basic.basic_driver import BasicDriver


class BasicDriverConfigurer(object):
    def __init__(self):
        self.url = ''
        self.headless = False
        self.no_sandbox = False
        self.pop_up = False

    def headless(self, headless: bool):
        self.headless = headless
        return self

    def no_sandbox(self, no_sandbox: bool):
        self.no_sandbox = no_sandbox
        return self

    def has_pop_up(self, flag: bool):
        self.pop_up = flag
        return self

    def configure(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        if self.no_sandbox:
            chrome_options.add_argument('--no-sandbox')
        chrome_options.add_experimental_option('detach', True)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(options=chrome_options)
        if self.pop_up:
            handles = driver.window_handles
            for handle in handles:
                if handle != handles[0]:
                    driver.switch_to.window(handle)
                    driver.close()
            driver.switch_to.window(handles[0])
        return BasicDriver(driver)
