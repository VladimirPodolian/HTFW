from framework.web_element import WebElement


class CookieFooter(WebElement):

    def __init__(self):
        self.cookie_footer_locator = '[id = onetrust-banner-sdk]'
        super().__init__(self.cookie_footer_locator, name='cookie footer')

    # Elements

    @property
    def policy(self):
        return WebElement(f'{self.cookie_footer_locator} [id *= policy-text]', name='cookie policy text')

    @property
    def accept_button(self):
        return WebElement(f'{self.cookie_footer_locator} button[id *= accept]', name='accept cookie footer button')

    @property
    def close_button(self):
        return WebElement(f'{self.cookie_footer_locator} button[class *= close]', name='close cookie footer button')
