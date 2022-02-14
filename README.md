# HTFW
UI and API automation for the [leaderboard page](https://ru.wotblitz.com/ru/clans-leaderboard/)

Reported bugs on the page - [link](https://github.com/VladimirPodolyan/HTFW/issues)

---

# Tests executing:

## Docker
### General:
Install and start [docker](https://www.docker.com/) in your computer.

### UI automation:
Start by command `docker-compose run --rm tests tox -e py39-ui --`

Tests are running in `4 threads` by default.

### API automation:
Start by command `docker-compose run --rm tests tox -e py39-api --`

## Local:
### UI automation:
#### Dependencies (manual installing):
1. [Tox](https://pypi.org/project/tox/)
2. [Chromedriver](https://chromedriver.chromium.org/)

`Tox` is used to run tests and create venv.
You can install `Tox` with the `pip3 install tox` command.
It also requires the presence of `chromderiver` in the `PATH` environment variable.
For MacOS, `chromderiver` can be installed with `brew install chromedriver`

Start by command `tox -e py39-ui --`

Tests are running in `headless mode` and in `4 threads` by default.

### API automation:
Start by command `tox -e py39-api --`

---

# Allure report:
Allure report can be generated after `local` or `docker` automation by:
- `allure serve .tox/.tmp/allure/ui_tests` for ui automation
- `allure serve .tox/.tmp/allure/api_tests` for api automation
