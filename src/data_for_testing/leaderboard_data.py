from src.data_for_testing.general_data import BASE_URL

TOP_RANKED_ECHELON = 'platinum'
MEDIUM_RANKED_ECHELON = 'silver'
LOWER_RANKED_ECHELON = 'bronze'
DEFAULT_PAGE_SIZE = 8
RANKED_CLANS_COUNT = 32

leaderboard_page_url = f'{BASE_URL}/ru/clans-leaderboard'

social_links = {
    'vk': 'https://vk.com/wotblitz',
    'instagram': 'https://www.instagram.com/wotblitz_official',
    'discord': 'https://discord.gg/VV8ggDm',
    'youtube': 'https://www.youtube.com/channel/UCrh8Fd_QKmzhv4lhrS-k4sQ',
    'facebook': 'https://www.facebook.com/wotblitz',
    'ok': 'https://ok.ru/wotblitz',
}

echelons_data = {
    TOP_RANKED_ECHELON: {  # Default page
        'title': 'Высший эшелон',
        'places': range(1, 9),
        'url': f'{leaderboard_page_url}/#/leagues/0'
    },
    MEDIUM_RANKED_ECHELON: {
        'title': 'Средний эшелон',
        'places': range(9, 17),
        'url': f'{leaderboard_page_url}/#/leagues/1'
    },
    LOWER_RANKED_ECHELON: {
        'title': 'Нижний эшелон',
        'places': range(17, 33),
        'url': f'{leaderboard_page_url}/#/leagues/2'
    },
}

all_echelons_urls = list(map(lambda data: data['url'], echelons_data.values()))
all_echelons_titles = list(map(lambda data: data['title'], echelons_data.values()))
all_echelons_types = list(echelons_data.keys())

injections = {
    'js': "<script>alert('Executing JS')</script>",
    'html': "<blink>Hello there</blink>",
}
