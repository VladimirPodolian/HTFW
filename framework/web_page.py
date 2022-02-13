import logging

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from framework.web_driver import WebDriver


class WebPage:

    def __init__(self, locator_type, locator, name):
        self.locator_type = locator_type
        self.locator = locator
        self.name = name

        self.driver = WebDriver.driver
        self.wait = WebDriverWait(self.driver, 10)

    def wait_page_loaded(self, silent=False):
        if not silent:
            logging.info(f'Wait presence of {self.name}')
        self.wait.until(EC.visibility_of_element_located((self.locator_type, self.locator)))
        return self

    def open_page(self, url='', silent=False):
        url = getattr(self, 'url', '') if not url else url
        if not silent:
            logging.info(f'Navigating to url {url}')
        self.driver.get(url)
        self.wait_page_loaded()
        return self
