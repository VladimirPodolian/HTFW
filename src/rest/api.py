import httpx
from framework.utils import log

from src.data_for_testing.general_data import BASE_URL
from src.data_for_testing.leaderboard_data import DEFAULT_PAGE_SIZE, RANKED_CLANS_COUNT


class ApiBuilder:
    def __init__(self, base_url=f'{BASE_URL}/ru/api/'):
        self.base_url = base_url

    def __getattr__(self, request_method):
        return lambda *args, **kwargs: self.request(request_method, *args, **kwargs)

    def request(self, method, url, **kwargs):
        return httpx.request(method, f'{self.base_url}{url}', **kwargs)


class Api:
    """ Requests for leaderboard API automation needs """
    def __init__(self):
        self.api = ApiBuilder()

    def get_seasons(self):
        """
        Get available season names for leaderboard page

        :return: dict - available tournament seasons
        """
        log('Get available seasons for leaderboard')
        return self.api.get('tournaments/seasons/')

    def search_clan(self, clan_info):
        """
        Get all leaderboard clans with custom settings

        :param clan_info: clan name or tag to search for
        :return: dict - available clans data
        """
        log(f'Searching clan with given info: "{clan_info}"')
        clan_name = clan_info.replace(' ', '+')
        return self.api.get(f'clans-leaderboard/search/?query={clan_name}')

    def get_clans(self, page=1, size=DEFAULT_PAGE_SIZE, gte=1, lte=RANKED_CLANS_COUNT):
        """
        Get all leaderboard clans with custom settings

        :param page: page number
        :param size: page size
        :param gte: starting index
        :param lte: stopping index
        :return: dict - available clans data
        """
        log(f'Get ranked clans with: page_size={size}, page_start={gte}, page_stop={lte}')
        root_url = 'clans-leaderboard/tournamentCupX/'
        return self.api.get(f'{root_url}?page={page}&page_size={size}&rank__gte={gte}&rank__lte={lte}')

    def get_clan_rewards(self, clan_id):
        """
        Get clan rewards for each team

        :param clan_id: clan id
        :return: dict - rewards data for each team in clan
        """
        log(f'Get clan rewards by clan id: "{clan_id}"')
        return self.api.get(f'clans-leaderboard/tournamentCupX/{clan_id}/')


class UIApi(Api):
    """ Customised api requests from parent Api class for UI automation needs """

    def get_available_season(self):
        """
        Get available season names

        :return: dict - available tournament seasons
        """
        response = super().get_seasons().json()['results']
        return [item['title'] for item in response]

    def search_clan(self, clan_info):
        """
        Get all leaderboard clans with custom settings.

        :param clan_info: clan name or tag to search for
        :return: dict - available clans data
        """
        return super().search_clan(clan_info).json()['results']

    def get_clans(self, page=1, size=DEFAULT_PAGE_SIZE, gte=1, lte=RANKED_CLANS_COUNT):
        """
        Get all leaderboard clans with custom settings.

        :param page: page number
        :param size: page size
        :param gte: starting index
        :param lte: stopping index
        :return: dict - available clans data
        """
        return super().get_clans(page=page, size=size, gte=gte, lte=lte).json()['results']

    def get_clan_rewards(self, clan_id):
        """
        Get clan rewards for each team

        :param clan_id: clan id
        :return: dict - rewards data for each team in clan
        """
        return super().get_clan_rewards(clan_id=clan_id).json()

    def get_clans_with_rewards(self, more_than=6, **kwargs):
        """
        Get clans with custom rewards count from different teams

        :param more_than: more than *value* rewards count
        :param kwargs: kwargs of self.get_clans()
        :return: dict - clans with specified value of teams rewards
        """
        clans_with_large_rewards = []
        for clan in self.get_clans(**kwargs):
            clan_rewards_response = self.get_clan_rewards(clan['clan']['id'])
            if len(clan_rewards_response['teams']) > more_than:
                clans_with_large_rewards.append(clan_rewards_response)

        return clans_with_large_rewards
