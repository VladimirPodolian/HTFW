from src.rest.api import Api
from src.data_for_testing.leaderboard_data import DEFAULT_PAGE_SIZE, RANKED_CLANS_COUNT


class UIApi:
    """ Wrapper of Api object """
    def __init__(self):
        self.wrapped_api = Api()

    def get_available_season(self):
        """
        Get available season names

        :return: dict - available tournament seasons
        """
        response = self.wrapped_api.get_seasons().json()['results']
        return [item['title'] for item in response]

    def search_clan(self, clan_info):
        """
        Get all leaderboard clans with custom settings.

        :param clan_info: clan name or tag to search for
        :return: dict - available clans data
        """
        return self.wrapped_api.search_clan(clan_info).json()['results']

    def get_clans(self, page=1, size=DEFAULT_PAGE_SIZE, gte=1, lte=RANKED_CLANS_COUNT):
        """
        Get all leaderboard clans with custom settings.

        :param page: page number
        :param size: page size
        :param gte: starting index
        :param lte: stopping index
        :return: dict - available clans data
        """
        return self.wrapped_api.get_clans(page=page, size=size, gte=gte, lte=lte).json()['results']

    def get_clan_rewards(self, clan_id):
        """
        Get clan rewards for each team

        :param clan_id: clan id
        :return: dict - rewards data for each team in clan
        """
        return self.wrapped_api.get_clan_rewards(clan_id=clan_id).json()

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
