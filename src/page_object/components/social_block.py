from selenium.webdriver.common.by import By
from framework.web_element import WebElement


class SocialBlock(WebElement):

    def __init__(self):
        self.social_locator = '[class = social_content]'
        super().__init__(self.social_locator, name='social content block')

    def social_link(self, link_url):
        return WebElement(locator_type=By.CSS_SELECTOR, locator=f'{self.social_locator} a[href = "{link_url}"]',
                          name=f'social link with url: {link_url}')
