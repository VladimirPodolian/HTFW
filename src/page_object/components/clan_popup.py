import time

from framework.web_element import WebElement


class ClanPopup(WebElement):

    def __init__(self):
        self.table_row_locator = 'tr[class *= p-leaderboard-team]'
        super().__init__('[class = popup] [class *= p-leaderboard-detail]', name='clan rewards popup')

    # Elements

    @property
    def header(self):
        return WebElement('[class *= p-leaderboard-detail_heading]', name='popup header (clan name)')

    @property
    def header_items(self):
        return WebElement('[class *= info-value]', name='header items')

    @property
    def close_button(self):
        return WebElement('button[class *= popup_button]', name='close popup button')

    @property
    def expand_button(self):
        return WebElement('button[class *= button-more]', name='expand table button')

    # Table elements

    @property
    def table(self):
        return WebElement('table[class *= p-table_table]', name='popup table')

    @property
    def all_rows(self):
        return WebElement(self.table_row_locator, name='table row')

    @property
    def all_rows_except_uncounted(self):
        return WebElement(f'{self.table_row_locator}:not([class *= uncounted])', name='table row except uncounted')

    def tournament_by_id(self, row_id):
        return WebElement(f'{self.table_row_locator}:nth-child({row_id}) [class *= title]',
                          name=f'team tournament by row id: {row_id}')

    def title_by_id(self, row_id):
        return WebElement(f'{self.table_row_locator}:nth-child({row_id}) [class *= participant_name]',
                          name=f'team title by row id: {row_id}')

    def efficient_by_id(self, row_id):
        return WebElement(f'{self.table_row_locator}:nth-child({row_id}) [class *= team_te]',
                          name=f'team efficient by row id: {row_id}')

    def points_by_id(self, row_id):
        return WebElement(f'{self.table_row_locator}:nth-child({row_id}) [class *= team_cups]',
                          name=f'team points by row id: {row_id}')

    # Clan info functions

    def get_clan_name(self):
        return self.header.get_text()

    def get_clan_efficient(self):
        return float(list(self.header_items.get_elements_texts())[1])

    def get_clan_points(self):
        return int(list(self.header_items.get_elements_texts())[0].replace(' ', ''))

    # Team info functions

    def get_team_tournament_by_row_id(self, row_id):
        return self.tournament_by_id(row_id).get_text()

    def get_team_title_by_row_id(self, row_id):
        return self.title_by_id(row_id).get_text()

    def get_team_efficient_by_row_id(self, row_id):
        return float(self.efficient_by_id(row_id).get_text())

    def get_team_points_by_row_id(self, row_id):
        return int(self.points_by_id(row_id).get_text().replace(' ', ''))

    def expand_rewards(self, timeout=10):
        """
        Trying to expand all rewards by 'see moore' button.

        :param timeout: timeout to stop trying to expand rewards
        :return: self object
        """
        start_time = time.time()
        while timeout > (time.time() - start_time) and self.expand_button.is_available():
            self.expand_button.click()
        assert not self.expand_button.is_available(), 'Expand button still presence!'
        return self
