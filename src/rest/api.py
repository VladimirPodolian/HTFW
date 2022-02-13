from framework.utils import log

from src.rest.api_builder import ApiBuilder
from src.data_for_testing.leaderboard_data import DEFAULT_PAGE_SIZE, RANKED_CLANS_COUNT


class Api:
    def __init__(self):
        self.api = ApiBuilder()

    def get_seasons(self):
        """
        Get available season names for leaderboard page

        :return: dict - available tournament seasons
        """
        log(f'Get available seasons for leaderboard')
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
        base_url = 'clans-leaderboard/tournamentCupX/'
        request = self.api.get(f'{base_url}?page={page}&page_size={size}&rank__gte={gte}&rank__lte={lte}')
        return request

    def get_clan_rewards(self, clan_id):
        """
        Get clan rewards for each team

        :param clan_id: clan id
        :return: dict - rewards data for each team in clan
        """
        log(f'Get clan rewards by clan id: "{clan_id}"')
        return self.api.get(f'clans-leaderboard/tournamentCupX/{clan_id}/')
