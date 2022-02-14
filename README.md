# HTFW
UI and API automation for the [leaderboard page](https://ru.wotblitz.com/ru/clans-leaderboard/)

Reported bugs on the page - [link](https://github.com/VladimirPodolyan/HTFW/issues)

---

# Tests executing:

## Docker
### Image
From root directory run `docker build -t wg-automation .` After it's finished you can run automation. 

### UI automation:
With the command `docker-compose run --rm ui`

Tests are running in `4 threads` by default.

### API automation:
With the command `docker-compose run --rm api`

## Local:
### UI automation:
#### Dependencies (manual installing):
1. [Tox](https://pypi.org/project/tox/)
2. [Chromedriver](https://chromedriver.chromium.org/)

`Tox` is used to run tests and create venv.
You can install `Tox` with the `pip3 install tox` command.
It also requires the presence of `chromderiver` in the `PATH` environment variable.
For MacOS, `chromderiver` can be installed with `brew install chromedriver`

With the command `tox -e py39-ui --`

Tests are running in `headless mode` and in `4 threads` by default.

### API automation:
With the command `tox -e py39-api --`

---

# Allure report:
Allure report can be generated after `local` and `docker` automation runs by:
- `allure serve .tox/.tmp/allure/ui_tests` for ui automation
- `allure serve .tox/.tmp/allure/api_tests` for api automation
