from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import NoSuchElementException


class BasicDriver(object):
    def __init__(self, driver):
        self._driver = driver
        self._body = None
        self._page_source = None

    def __del__(self):
        self._driver.quit()
        pass

    def open_url(self, url: str):
        self._driver.get(url)
        self._page_source = self._driver.page_source

    def get_page_source(self):
        return self._page_source

    def save_page_source(self, path: str):
        with open(path, 'w') as file:
            for line in self._page_source:
                file.write(line)
        print('page source saved')

    def _click(self, path: str):
        button = (WebDriverWait(self._driver, 10).
                  until(ec.presence_of_element_located((By.XPATH, path))))
        print(button.text)
        button.click()

    def _xpath(self, path: str):
        try:
            return self._driver.find_element(By.XPATH, path)
        except NoSuchElementException:
            return None

    def _page_end(self):
        self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def _get_height(self):
        return self._driver.execute_script("return document.body.scrollHeight")