from random import choice

import pytest
from src.rest.status_codes import SUCCESS, REQUEST_TOO_LARGE
from src.data_for_testing.leaderboard_data import RANKED_CLANS_COUNT, all_echelons_types, echelons_data, injections
from src.utils import parse_echelon_data, random_string


class TestApiLeaderboardGeneral:

    @pytest.mark.parametrize('case', all_echelons_types)
    def test_leaderboard_page_get_echelons(self, api, case):
        page_size, page_start, page_stop, _ = parse_echelon_data(echelons_data[case])
        request = api.get_clans(size=page_size, gte=page_start, lte=page_stop)
        assert request.status_code == SUCCESS


class TestApiLeaderboardClans:

    def test_leaderboard_page_clans_emblems_available(self, api):
        request = api.get_clans(size=RANKED_CLANS_COUNT).json()['results']
        for item in [item['clan']['emblems'] for item in request]:
            assert all((item['small'], item['big']))

    def test_leaderboard_page_clans_ranks_available(self, api):
        results = api.get_clans(size=RANKED_CLANS_COUNT).json()['results']
        api_ranks = [item['rank'] for item in results]
        assert sorted(api_ranks) == api_ranks

    def test_leaderboard_page_clans_tags_available(self, api):
        request = api.get_clans(size=RANKED_CLANS_COUNT).json()['results']
        api_tags = [item['clan']['tag'] for item in request]
        assert len(list(filter(str, api_tags))) == len(api_tags)

    def test_leaderboard_page_clans_names_available(self, api):
        request = api.get_clans(size=RANKED_CLANS_COUNT).json()['results']
        api_clan_names = [item['clan']['name'] for item in request]
        assert len(list(filter(str, api_clan_names))) == len(api_clan_names)

    def test_leaderboard_page_clans_efficient_available(self, api):
        request = api.get_clans(size=RANKED_CLANS_COUNT).json()['results']
        api_efficient = [item['clan_efficient'] for item in request]
        assert len(list(filter(float, api_efficient))) == len(api_efficient)

    def test_leaderboard_page_clans_sorted_by_points(self, api):
        results = api.get_clans(size=RANKED_CLANS_COUNT).json()['results']
        api_points = [item['rewards_count'] for item in results]
        assert sorted(api_points, reverse=True) == api_points


class TestApiLeaderboardSeasons:

    def test_leaderboard_page_seasons_available(self, api):
        """ Gets the available leaderboard seasons """
        results = api.get_seasons().json()['results']
        assert len(results)


class TestApiLeaderboardClanRewards:
    # team info blocked by https://github.com/VladimirPodolyan/HTFW/issues/2

    @pytest.mark.xfail(reason='https://github.com/VladimirPodolyan/HTFW/issues/2')
    @pytest.mark.parametrize('case', list(range(1, 4)))
    def test_leaderboard_page_get_clan_rewards_teams(self, api, case):
        """ Clan rewards should contain associated team data """
        random_clan = choice(api.get_clans(size=RANKED_CLANS_COUNT).json()['results'])
        for item in api.get_clan_rewards(random_clan['clan']['id']).json()['teams']:
            assert item["team"]

    def test_leaderboard_page_get_clan_rewards_team_id(self, api):
        """ Each team should contain team_id """
        random_clan = choice(api.get_clans(size=RANKED_CLANS_COUNT).json()['results'])
        teams_ids = [item['team_id'] for item in api.get_clan_rewards(random_clan['clan']['id']).json()['teams']]
        assert len(list(filter(int, teams_ids))) == len(teams_ids)

    def test_leaderboard_page_get_clan_team_efficient(self, api):
        """ Each team should contain efficient """
        random_clan = choice(api.get_clans(size=RANKED_CLANS_COUNT).json()['results'])
        rewards = api.get_clan_rewards(random_clan['clan']['id']).json()['teams']
        teams_efficient = [item['team_efficient'] for item in rewards]
        assert len(list(filter(float, teams_efficient))) == len(teams_efficient)

    def test_leaderboard_page_get_clan_team_points(self, api):
        """ Each team should contain rewarded points """
        random_clan = choice(api.get_clans(size=RANKED_CLANS_COUNT).json()['results'])
        rewards = api.get_clan_rewards(random_clan['clan']['id']).json()['teams']
        assert len([team_points['rewards'] for team_points in rewards]) == len(rewards)

    def test_leaderboard_page_get_clan_rewards_updated_date(self, api):
        """ Each reward should contain date info """
        random_clan = choice(api.get_clans(size=RANKED_CLANS_COUNT).json()['results'])
        teams_ids = [item['updated_at'] for item in api.get_clan_rewards(random_clan['clan']['id']).json()['teams']]
        assert len(list(filter(str, teams_ids))) == len(teams_ids)

    def test_leaderboard_page_get_clan_rewards_team_status(self, api):
        """ Each reward should contain team status info """
        random_clan = choice(api.get_clans(size=RANKED_CLANS_COUNT).json()['results'])
        rewards = api.get_clan_rewards(random_clan['clan']['id']).json()['teams']
        assert len([team_status['used'] for team_status in rewards]) == len(rewards)


class TestApiLeaderboardSearchInput:

    @pytest.mark.xfail(reason='Flaky test: https://github.com/VladimirPodolyan/HTFW/issues/8')
    @pytest.mark.parametrize('case', ['name', 'tag'])
    def test_leaderboard_page_search_clan(self, api, case):
        """ Check search response for random clan name/tag """
        clan_pattern = choice(api.get_clans(size=RANKED_CLANS_COUNT).json()['results'])['clan'][case]
        assert clan_pattern in [item[case] for item in api.search_clan(clan_pattern).json()['results']]

    def test_leaderboard_page_search_clan_large_input(self, api):
        """ Check search response for random clan name/tag """
        request = api.search_clan(random_string() * 1000)
        assert request.status_code == REQUEST_TOO_LARGE

    @pytest.mark.xfail(reason='https://github.com/VladimirPodolyan/HTFW/issues/6')
    def test_leaderboard_page_search_clan_medium_input(self, api):
        """ Check search response for random clan name/tag """
        request = api.search_clan(random_string() * 20)
        assert request.status_code == SUCCESS

    @pytest.mark.xfail(reason='https://github.com/VladimirPodolyan/HTFW/issues/6')
    @pytest.mark.parametrize('case', injections)
    def test_leaderboard_page_search_clan_injection(self, api, case):
        """ Check response status code for js/html injection """
        request = api.search_clan(injections[case])
        assert request.status_code == SUCCESS
