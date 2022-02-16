import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from framework.utils import log, cut_log_data
from framework.web_driver import WebDriver


class WebElement:
    def __init__(self, locator=None, name=None, locator_type=None):
        self.locator = locator
        self.name = locator if not name else name
        if not locator_type:
            self.locator_type = By.XPATH if '//' in locator else By.CSS_SELECTOR
        else:
            self.locator_type = locator_type

        self.driver = WebDriver.driver
        self.wait = WebDriverWait(self.driver, 10)

    @property
    def element(self):
        return self.driver.find_element(by=self.locator_type, value=self.locator)

    @property
    def all_elements(self):
        return self.driver.find_elements(by=self.locator_type, value=self.locator)

    # Element waits

    def wait_element_hidden(self, silent=False):
        if not silent:
            log(f'Wait until hidden of "{self.name}"')
        self.wait.until_not(EC.visibility_of_element_located((self.locator_type, self.locator)),
                            message=f'Element "{self.name}" still visible. Locator: {self.locator}')
        return self

    def wait_element(self, silent=False):
        if not silent:
            log(f'Wait until presence of "{self.name}"')
        self.wait.until(EC.visibility_of_element_located((self.locator_type, self.locator)),
                        message=f'Not waited for element "{self.name}". Locator: {self.locator}')
        return self

    def wait_clickable(self, silent=False):
        if not silent:
            log(f'Wait until clickable of "{self.name}"')
        self.wait.until(EC.element_to_be_clickable((self.locator_type, self.locator)),
                        message=f'Element "{self.name}" still not clickable. Locator: {self.locator}')
        return self

    # Element interaction

    def click(self):
        log(f'Click into "{self.name}"')
        self.wait_element(silent=True).wait_clickable(silent=True).element.click()
        return self

    def type_text(self, text, wait=True, silent=False):
        if wait:
            self.wait_element(silent=True)
        if not silent:
            log(f'Type text {cut_log_data(text)} into "{self.name}"')
        self.element.send_keys(text)
        return self

    def type_slowly(self, text, sleep_gap=0.05, wait=True, silent=False):
        if wait:
            self.wait_element(silent=True)
        if not silent:
            log(f'Type text "{cut_log_data(text)}" into "{self.name}"')
        for letter in str(text):
            self.element.send_keys(letter)
            time.sleep(sleep_gap)
        return self

    def clear_text(self, wait=True, silent=False):
        if wait:
            self.wait_element(silent=True)
        if not silent:
            log(f'Clear text in "{self.name}"')
        self.element.clear()
        return self

    # Element state

    def is_displayed(self, silent=False):
        if not silent:
            log(f'Check visibility of "{self.name}"')
        return self.element.is_displayed()

    def is_available(self, silent=False):
        if not silent:
            log(f'Check accessibility of "{self.name}"')
        return True if len(self.all_elements) > 0 else False

    def get_text(self, wait=True, silent=False):
        if wait:
            self.wait_element(silent=True)
        if not silent:
            log(f'Get text from "{self.name}"')
        return self.element.text

    def get_attribute(self, attribute, wait=True, silent=False):
        if wait:
            self.wait_element(silent=True)
        if not silent:
            log(f'Get attribute from "{self.name}"')
        return self.element.get_attribute(attribute)

    def get_elements_texts(self, wait=True, silent=False):
        if wait:
            self.wait_element(silent=True)
        if not silent:
            log(f'Get all texts from "{self.name}"')
        return (element_item.text for element_item in self.all_elements)

    def get_elements_count(self, wait=True, silent=False):
        if wait:
            self.wait_element(silent=True)
        if not silent:
            log(f'Get elements count of "{self.name}"')
        return len(self.all_elements)

    # Element location

    def scroll_to_viewport(self, block='center', wait=True):
        """
        Scroll to element.

        :param block: one of "start", "center", "end", "nearest"
        :param wait: wait element before interaction
        :return: self object
        """
        if wait:
            self.wait_element(silent=True)
        self.driver.execute_script('arguments[0].scrollIntoView({{block: "{0}"}});'.format(block), self.element)
        return self
