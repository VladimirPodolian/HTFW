import time

from framework.utils import log


class WebDriver:
    driver = None

    def __init__(self, driver):
        self.driver = driver
        WebDriver.driver = self.driver

    @property
    def current_url(self):
        log('Getting current url')
        return self.driver.current_url

    @property
    def window_handles(self):
        return self.driver.window_handles

    def switch_to_tab(self, tab_id=1, wait=True, timeout=10):
        expected_windows_count = tab_id + 1
        log(f'Switch to tab {expected_windows_count}')

        def is_tab_opened():
            return len(self.window_handles) == expected_windows_count

        if wait:
            start_time = time.time()
            while timeout > (time.time() - start_time) and not is_tab_opened():
                time.sleep(0.05)

        if not is_tab_opened():
            raise Exception(f'Tab {expected_windows_count} not opened')

        self.driver.switch_to.window(self.window_handles[tab_id])
