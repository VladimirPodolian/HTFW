from random import choice, randint

import pytest
from hamcrest import assert_that, equal_to

from src.utils import random_string, parse_echelon_data
from src.page_object.components.social_block import SocialBlock
from src.data_for_testing.leaderboard_data import (
    DEFAULT_PAGE_SIZE,
    echelons_data,
    all_echelons_types,
    social_links,
    LOWER_RANKED_ECHELON,
    TOP_RANKED_ECHELON,
    RANKED_CLANS_COUNT,
)
from src.page_object.pages.leaderboard_page import (
    LeaderboardPage,
    LeaderboardTable,
    get_leader_info,
    Carousel,
)


@pytest.fixture
def leaderboard_page():
    return LeaderboardPage().open_page()


@pytest.fixture
def specified_echelon(request):
    return LeaderboardPage().open_page(url=echelons_data[request.param]['url'])


@pytest.fixture
def random_echelon():
    return LeaderboardPage().open_page(url=echelons_data[choice(all_echelons_types)]['url'])


@pytest.fixture(params=echelons_data, ids=all_echelons_types)
def all_echelons_regular_clan_data(request):
    size, start, stop, url = parse_echelon_data(echelons_data[request.param])
    clan_data = choice(request.node.uiapi.get_clans(size=size, gte=start, lte=stop))
    team_data = request.node.uiapi.get_clan_rewards(clan_data['clan']['id'])
    return get_leader_info(clan_data=clan_data, team_data=team_data, url=url, page_start=start)


@pytest.fixture
def all_echelons_pages_with_clan_data(all_echelons_regular_clan_data):
    page = LeaderboardPage().open_page(url=all_echelons_regular_clan_data['page_url'])
    if all_echelons_regular_clan_data['row_id'] > DEFAULT_PAGE_SIZE:  # Load all rows
        page.table.scroll_to_table()
    return page


class TestLeaderboardPage:

    @pytest.mark.parametrize('action', ['accept', 'decline'])
    def test_cookie_footer_closed_after_action(self, random_echelon, action):
        """ Cookie footer should be closed after decline of accept button iteration """
        page = LeaderboardPage().wait_page_table_loaded()
        button = page.cookie_footer.close_button if action == 'decline' else page.cookie_footer.accept_button
        button.click()
        assert not page.cookie_footer.wait_element_hidden().is_displayed()

    def test_leaderboard_default_echelon(self, leaderboard_page):
        """ Platinum echelon should be selected by default """
        echelon_with_title = leaderboard_page.carousel.echelon_with_title(echelons_data['platinum']['title'])
        assert echelon_with_title.wait_element().is_displayed()

    @pytest.mark.xfail(reason='https://github.com/VladimirPodolyan/HTFW/issues/1')
    def test_leaderboard_switch_season(self, leaderboard_page, request):
        """ Switch season and check echelon with title """
        leaderboard_page.switch_season(choice(request.node.uiapi.get_available_season()))
        echelon_with_title = leaderboard_page.carousel.echelon_with_title(echelons_data['platinum']['title'])
        assert echelon_with_title.wait_element().is_displayed()

    def test_leaderboard_page_social_links_displayed(self, random_echelon):
        """ Check visibility of social links in leaderboard page footer """
        for social_app_link in social_links.values():
            assert SocialBlock().social_link(social_app_link).wait_element().is_displayed()

    @pytest.mark.parametrize('social_name', social_links.keys(), ids=social_links.keys())
    def test_leaderboard_page_navigate_to_social_page(self, driver, leaderboard_page, social_name):
        """ Navigate to social app by link in page footer and check current url in browser """
        link = social_links[social_name]
        LeaderboardPage().wait_page_table_loaded()
        SocialBlock().social_link(link).wait_element().scroll_to_viewport(block='start').click()
        driver.switch_to_tab()
        if social_name in ('discord', 'instagram'):
            link = social_name
        assert link in driver.current_url


class TestLeaderboardSearch:

    @pytest.fixture()
    def unranked_clan(self, request, random_echelon):
        case = random_string(length=(2, 2))
        all_ranked_clans_data = request.node.uiapi.get_clans(size=RANKED_CLANS_COUNT)
        all_ranked_clans_names = [item['clan']['name'] for item in all_ranked_clans_data]
        all_ranked_clans_names.extend([item['clan']['tag'] for item in all_ranked_clans_data])

        search_result = request.node.uiapi.search_clan(case)
        searching_data = [data['name'] if case in data['name'].lower() else data['tag'] for data in search_result]

        for item in searching_data:
            if item not in all_ranked_clans_data:
                return item

    def test_leaderboard_page_clan_search_empty_result_table(self, random_echelon, unranked_clan):
        """ Check empty search result in table for unranked clan """
        random_echelon.searching_form.search_and_select_item(unranked_clan)
        rows_disappear = not random_echelon.table.all_rows.is_available()
        random_echelon.table.back_to_table_button.click()
        rows_appear = random_echelon.table.all_rows.wait_element().is_available()
        assert all((rows_disappear, rows_appear))

    @pytest.mark.xfail(reason='Flaky test. Stable markers needed. Check "ROAR" value')
    def test_leaderboard_page_clan_search_and_select(self, request, random_echelon):
        """ Search and select ranked clan and check unique visibility in table """
        page = LeaderboardPage()
        random_clan_name = choice(request.node.uiapi.get_clans(size=32))['clan']['name']
        page.searching_form.search_and_select_item(random_clan_name)
        assert_that(
            (
                page.table.row_by_name(random_clan_name).wait_element().is_displayed(),
                LeaderboardTable(search=True).all_rows.get_elements_count()
            ),
            equal_to((True, 1)))

    def test_leaderboard_page_clan_search_empty_result_popup(self, random_echelon):
        """ Check empty search result in popup for unavailable clan """
        page = LeaderboardPage()
        page.searching_form.search_input.click().type_slowly(random_string())
        assert page.searching_form.empty_search_result.wait_element().is_displayed()


class TestLeaderboardCarousel:

    @pytest.mark.parametrize('specified_echelon', [TOP_RANKED_ECHELON], indirect=['specified_echelon'])
    def test_echelon_navigation_to_next(self, specified_echelon):
        """ Switching to next echelon by clicking into the next medals """
        echelons_carousel = Carousel()
        for item in all_echelons_types[1:]:
            echelons_carousel.select_echelon(next_echelon=True)
            assert echelons_carousel.echelon_with_title(echelons_data[item]['title']).is_displayed()

    @pytest.mark.parametrize('specified_echelon', [LOWER_RANKED_ECHELON], indirect=['specified_echelon'])
    def test_echelon_navigation_to_prev(self, specified_echelon):
        """ Switching to previous echelon by clicking into the previous medals """
        echelons_carousel = Carousel()
        for item in all_echelons_types[1::-1]:
            echelons_carousel.select_echelon(prev_echelon=True)
            assert echelons_carousel.echelon_with_title(echelons_data[item]['title']).is_displayed()


class TestLeaderboardTable:
    # Table sorting covered in api tests

    def test_table_clan_info(self, all_echelons_regular_clan_data, all_echelons_pages_with_clan_data):
        """
        Clan info (rank/icon/tag/name/efficient/points) in the table
        should be visible and accurate the api info
        """
        row_id = all_echelons_regular_clan_data['row_id']
        clan_data = all_echelons_regular_clan_data['leader_info']['clan']
        page_table = all_echelons_pages_with_clan_data.table
        assert_that(
            (
                clan_data['rank'],
                clan_data['title'],
                clan_data['efficient'],
                clan_data['points']
            ),
            equal_to(
                (
                    page_table.get_clan_rank_by_row_id(row_id),
                    page_table.get_clan_title_by_row_id(row_id),
                    page_table.get_clan_efficient_by_row_id(row_id),
                    page_table.get_clan_points_by_row_id(row_id),
                )))


class TestLeaderboardClanPopup:

    @pytest.fixture
    def clan_data_with_rewards(self, request):
        """ Clan with large count of rewards collection """
        size, start, stop, url = parse_echelon_data(echelons_data[choice(all_echelons_types)])
        clan_data = choice(request.node.uiapi.get_clans_with_rewards(more_than=6, size=size, gte=start, lte=stop))
        team_data = request.node.uiapi.get_clan_rewards(clan_data['clan']['id'])
        return get_leader_info(clan_data=clan_data, team_data=team_data, url=url, page_start=start)

    @pytest.fixture
    def clan_with_rewards_page(self, clan_data_with_rewards):
        """ Get page with prepared clan with large count of rewards """
        page = LeaderboardPage().open_page(url=clan_data_with_rewards['page_url'])
        if clan_data_with_rewards['row_id'] > DEFAULT_PAGE_SIZE:  # Load all rows
            LeaderboardTable().scroll_to_table()
        return page

    @pytest.mark.xfail(reason='https://github.com/VladimirPodolyan/HTFW/issues/3')
    def test_clan_popup_expand_rewards(self, clan_with_rewards_page, clan_data_with_rewards, request):
        """ Expand available rewards of selected clan in popup """
        clan_data = clan_data_with_rewards['leader_info']['clan']

        clan_popup = clan_with_rewards_page.table.open_clan(clan_data['name'])
        elements_count_before_expand = clan_popup.all_rows.get_elements_count()
        clan_popup.expand_button.click().wait_element_hidden()
        elements_count_after_expand = clan_popup.all_rows.get_elements_count()
        assert all(
            (
                elements_count_after_expand > elements_count_before_expand,
                len(request.node.uiapi.get_clan_rewards(clan_data['id'])['teams']) == elements_count_after_expand,
            )
        )

    def test_clan_popup_close_layout(self, random_echelon):
        """ Close clan popup by X button in the top right corner """
        table = LeaderboardTable().scroll_to_table()
        row_id = randint(1, table.all_rows.wait_element().get_elements_count())

        clan_popup = LeaderboardTable().open_clan(row_id=row_id)
        clan_popup.close_button.click()
        assert all(
            (
                not clan_popup.wait_element_hidden().is_available(),
                table.all_rows.is_displayed(),
            )
        )

    def test_clan_popup_header(self, all_echelons_regular_clan_data, all_echelons_pages_with_clan_data):
        """
        Clan info (tag/name/efficient/points) in the popup header
        should be visible and accurate the api info
        """
        clan_data = all_echelons_regular_clan_data['leader_info']['clan']
        clan_popup = LeaderboardTable().open_clan(clan_name=clan_data['name'])
        assert_that(
            (
                clan_data['title'],
                clan_data['efficient'],
                clan_data['points'],
            ),
            equal_to(
                (
                    clan_popup.get_clan_name(),
                    clan_popup.get_clan_efficient(),
                    clan_popup.get_clan_points(),
                )))

    def test_clan_popup_reward_info(self, all_echelons_regular_clan_data, all_echelons_pages_with_clan_data):
        """
        Reward info (tournament/clan_tag/team_name/efficient/points) in the clan popup
        should be visible and accurate the api info
        """
        data = all_echelons_regular_clan_data['leader_info']
        clan_popup = LeaderboardTable().open_clan(clan_name=data['clan']['name'])
        assert_that(
            (
                data['team']['tournament_name'],
                data['team']['title'],
                data['team']['efficient'],
                data['team']['points'],
            ),
            equal_to(
                (
                    clan_popup.get_team_tournament_by_row_id(data['team']['row_id']),
                    clan_popup.get_team_title_by_row_id(data['team']['row_id']),
                    clan_popup.get_team_efficient_by_row_id(data['team']['row_id']),
                    clan_popup.get_team_points_by_row_id(data['team']['row_id']),
                )))
