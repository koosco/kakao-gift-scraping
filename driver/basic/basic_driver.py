from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import NoSuchElementException


class BasicDriver(object):
    def __init__(self, driver):
        self.driver = driver
        self.body = None
        self.page_source = None

    def __del__(self):
        self.driver.quit()
        pass

    def open_url(self, url: str):
        self.driver.get(url)
        self.page_source = self.driver.page_source

    def get_page_source(self):
        return self.page_source

    def save_page_source(self, path: str):
        with open(path, 'w') as file:
            for line in self.page_source:
                file.write(line)
        print('page source saved')

    def click(self, path: str):
        button = (WebDriverWait(self.driver, 10).
                  until(ec.presence_of_element_located((By.XPATH, path))))
        print(button.text)
        button.click()

    def xpath(self, path: str):
        try:
            return self.driver.find_element(By.XPATH, path)
        except NoSuchElementException:
            return None

    def page_end(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def get_height(self):
        return self.driver.execute_script("return document.body.scrollHeight")