from random import randint

from framework.web_element import WebElement
from framework.web_page import WebPage
from selenium.webdriver.common.by import By

from src.page_object.components.clan_popup import ClanPopup
from src.page_object.components.cookie_footer import CookieFooter
from src.data_for_testing.leaderboard_data import leaderboard_page_url, echelons_data, all_echelons_types
from src.page_object.components.social_block import SocialBlock


def get_leader_info(clan_data=None, team_data=None, url=None, page_start=None):
    """
    Get and parse for tests needs available info from original clan/team data.

    :param clan_data: dict object from Rest.get_clans request
    :param team_data: dict object from Rest.get_clan_rewards request
    :param url: required for `page_url` key in root dict
    :param page_start: required for `row_id` key in root dict
    :return: dict object ~ {'page_url': '...', 'row_id': '...', 'leader_info': {'clan': {...}, 'team': {...}}}
    """
    leader_info = {'leader_info': {'clan': {}, 'team': {}}}
    leader_info.update(
        {
            'page_url': url,
            'row_id': clan_data['rank'] - (page_start - 1) if page_start else page_start,
        }
    )

    if clan_data:
        leader_info['leader_info']['clan'].update(get_clan_info(clan_data))

    if team_data:
        leader_info['leader_info']['team'].update(get_team_info(team_data))

    return leader_info


def get_clan_info(clan_data):
    """
    Get and parse for tests needs available info from original clan data.

    :param clan_data: dict object from Rest.get_clans request
    :return: dict object with parsed data
    """
    return {
        'id': clan_data['clan']['id'],
        'rank': clan_data['rank'],
        'name': clan_data['clan']['name'],
        'title': f"[{clan_data['clan']['tag']}] {clan_data['clan']['name']}",
        'efficient': round(clan_data['clan_efficient'] * 100, 1),
        'points': clan_data['rewards_count'],
    }


def get_team_info(team_data):
    """
    Get and parse for tests needs available info from original clan data.

    :param team_data: dict object from Rest.get_clan_rewards request
    :return: dict object with parsed data
    """
    # FIXME remove [:2] after following issue resolved:
    # https://github.com/VladimirPodolyan/HTFW/issues/2
    # https://github.com/VladimirPodolyan/HTFW/issues/3
    team_with_available_data = [item for item in team_data['teams'] if item['team']][:2]
    random_id = randint(0, len(team_with_available_data)-1)
    available_data = team_with_available_data[random_id]
    return {
        'clan_tag': f"[{team_data['clan']['tag']}]",
        'tournament_name': available_data['team']['tournament']['title'],
        'tournament_date': available_data['updated_at'],

        'row_id': random_id + 1,
        'name': available_data['team']['title'],
        'title': f"[{team_data['clan']['tag']}] {available_data['team']['title']}",
        'efficient': round(available_data['team_efficient'] * 100, 1),
        'points': available_data['rewards'],
    }


class LeaderboardPage(WebPage):

    def __init__(self):
        self.url = leaderboard_page_url

        self.cookie_footer = CookieFooter()
        self.carousel = Carousel()
        self.social_block = SocialBlock()
        self.searching_form = SearchingForm()
        self.table = LeaderboardTable()

        super().__init__(By.CSS_SELECTOR, 'main[class *= leaderboard]', name='Leaderboard page')

    # Elements

    @property
    def season_select_arrow(self):
        return WebElement('[class *= season-select_arrow]', name='seasons select arrow')

    @property
    def season_select_menu(self):
        return WebElement('[class *= season-select_menu]', name='seasons select arrow')

    # Functions

    def wait_page_table_loaded(self):
        self.table.spinner.wait_element_hidden()
        return self

    def season_item(self, name):
        raise Exception('https://github.com/VladimirPodolyan/HTFW/issues/1')

    def switch_season(self, season_name):
        self.season_select_arrow.click()
        self.season_select_menu.wait_element()
        self.season_item(season_name).click()
        return self


class Carousel(WebElement):

    def __init__(self):
        self.root_locator = '[class = leaderboard-carousel]'
        super().__init__(self.root_locator, name='leaderboard carousel')

    # Elements

    @property
    def next_echelon(self):
        return WebElement(f'{self.root_locator} [class *= swiper-slide-next]', name=f'next echelon medal')

    @property
    def prev_echelon(self):
        return WebElement(f'{self.root_locator} [class *= swiper-slide-prev]', name=f'previous echelon medal')

    @property
    def unselected_echelons(self):
        return WebElement('[class *= swiper-slide]:not([class *= active])', name='unselected echelons')

    def echelon(self, echelon_type):
        assert echelon_type in all_echelons_types, f'Please select one of {all_echelons_types}'
        return WebElement(f'{self.root_locator} [class *= swiper-slide] [style *= {echelon_type}]',
                          name=f'{echelon_type} echelon')

    def echelon_with_title(self, title):
        return WebElement('//*[@class="leaderboard-carousel" and .//*[contains(@class, "swiper-slide-active")] '
                          f'and contains(., "{title}")]', name=f'echelon with title: {title}')

    # Functions

    def select_echelon(self, echelon_name='', next_echelon=False, prev_echelon=False):
        """
        Select specified echelon and wait until data fetched

        :param echelon_name: select echelon by echelon name
        :param next_echelon: select next (left) echelon
        :param prev_echelon: select next (right) echelon
        :return: sself object
        """
        assert any((echelon_name, next_echelon, prev_echelon)), 'At least one of parameter required'

        if echelon_name:
            self.echelon(echelon_name).click()
            self.echelon_with_title(echelons_data[echelon_name]['title']).wait_element(silent=True)
        elif next_echelon:
            self.next_echelon.click()
        elif prev_echelon:
            self.prev_echelon.click()

        LeaderboardTable().spinner.wait_element_hidden()
        return self

    def available_echelons_range(self):
        return range(self.unselected_echelons.get_elements_count())


class SearchingForm(WebElement):

    def __init__(self):
        self.root_locator = '[class *= search_form]'
        self.empty_search_template = 'По вашему запросу ничего не найдено'
        super().__init__(self.root_locator, name='search form')

    @property
    def search_input(self):
        return WebElement(f'{self.root_locator} input[class *= search_input]', name='search input')

    @property
    def clear_button(self):
        return WebElement(f'{self.root_locator} button[class *= search_clear__show]', name='clear input button')

    def item_by_name(self, clan_name):
        return WebElement(f'//button[contains(@class, "search-list_item") and contains(., "{clan_name}")]',
                          name=f'search item by name: {clan_name}')

    def tag_by_name(self, clan_name):
        return WebElement(f'//button[contains(@class, "search-list_item") and .//*[contains(., "{clan_name}")]]'
                          f'//*[contains(@class, "tag")]', name=f'search tag by name: {clan_name}')

    def any_popup_item(self):
        return WebElement(f'//button[contains(@class, "search-list_item")]', name='popup')

    @property
    def empty_search_result(self):
        return WebElement(f'//*[@class="search_result" and .//*[.="{self.empty_search_template}"]]',
                          name=f'empty search result')

    def search_and_select_item(self, clan_name):
        """
        Search clan by name and select him

        :return: self object
        """
        self.search_input.click().type_slowly(clan_name)
        self.item_by_name(clan_name).click().wait_element_hidden()
        return self


class LeaderboardTable(WebElement):
    def __init__(self, search=False):
        self.clan_popup = ClanPopup()
        self.root_locator = 'table[class *= leaderboard-table]'
        if not search:
            self.root_locator = f'{self.root_locator} tbody[infinite-scroll-disabled]'
        self.table_row_locator = f'{self.root_locator} [class *= table_tr]'
        super().__init__(self.root_locator, name='leaderboard table')

    # Elements

    @property
    def all_rows(self):
        return WebElement(self.table_row_locator, name='all table rows')

    @property
    def spinner(self):
        return WebElement(f'{self.root_locator} [class *= waiting_spinner]', name='leaderboard table spinner')

    @property
    def back_to_table_button(self):
        """ back to table button appear after unsuccessful search result """
        return WebElement(f'[class = leaderboard-button-back]', name='leaderboard table back button')

    def row_by_id(self, row_id):
        return WebElement(f'{self.table_row_locator}:nth-child({row_id})',
                          name=f'row by row id: {row_id}')

    def place_by_id(self, row_id):
        return WebElement(f'{self.table_row_locator}:nth-child({row_id}) td[class *= place]',
                          name=f'place by row id: {row_id}')

    def wrapped_place_by_id(self, row_id):
        return WebElement(f'{self.table_row_locator}:nth-child({row_id}) [class *= "place place"]',
                          name=f'wrapped place by row id: {row_id}')

    def ico_by_id(self, row_id):
        return WebElement(f'{self.table_row_locator}:nth-child({row_id}) td[class *= place]',
                          name=f'place by row id: {row_id}')

    def tag_by_id(self, row_id):
        return WebElement(f'{self.table_row_locator}:nth-child({row_id}) [class *= clan-tag]',
                          name=f'tag by row id: {row_id}')

    def name_by_id(self, row_id):
        return WebElement(f'{self.table_row_locator}:nth-child({row_id}) [class *= participant_name]',
                          name=f'name by row id: {row_id}')

    def efficient_by_id(self, row_id):
        return WebElement(f'{self.table_row_locator}:nth-child({row_id}) [class *= efficient]',
                          name=f'efficient by row id: {row_id}')

    def points_by_id(self, row_id):
        return WebElement(f'{self.table_row_locator}:nth-child({row_id}) [class *= points]',
                          name=f'points by row id: {row_id}')

    def row_by_name(self, clan_name):
        return WebElement(f'//tr[contains(@class, "leaderboard-table") and .//*[contains(., "{clan_name}")]]',
                          name=f'row by clan name: {clan_name}')

    #  Functions

    def get_clan_title_by_row_id(self, row_id):
        """
        Get clan title by row id

        :return: string object with clan title ~ '[TAG] Clan Name'
        """
        return f'{self.tag_by_id(row_id).get_text()} {self.name_by_id(row_id).get_text()}'

    def get_clan_points_by_row_id(self, row_id):
        """
        Get clan point by row id

        :return: int object with clan point  ~ 44500
        """
        return int(self.points_by_id(row_id).get_text().replace(' ', ''))

    def get_clan_rank_by_row_id(self, row_id):
        """
        Get clan rank by row id

        :return: int object with clan rank  ~ 7
        """
        rank_text = self.place_by_id(row_id).get_text()
        if not rank_text:
            rank_text = self.wrapped_place_by_id(row_id).get_attribute('class').split('place__')[1]
        return int(rank_text)

    def get_clan_efficient_by_row_id(self, row_id):
        """
        Get clan efficient by row id

        :return: float object with clan efficient  ~ 89.2
        """
        return float(self.efficient_by_id(row_id).get_text())

    def open_clan(self, clan_name=None, row_id=None):
        """
        Open clan popup by clan name or row id

        :return: ClanPopup object
        """
        clan_row = None

        if clan_name:
            clan_row = self.row_by_name(clan_name=clan_name)
        elif row_id:
            clan_row = self.row_by_id(row_id=row_id)

        clan_row.scroll_to_viewport().click()
        return self.clan_popup.wait_element()

    def scroll_to_table(self):
        """ Scroll to leaderboard table """
        self.scroll_to_viewport(block='start')
        self.spinner.wait_element_hidden()
        return self
