# HTFW

Автоматизация UI и API для страницы [лидербордов](https://ru.wotblitz.com/ru/clans-leaderboard/)

Найденные баги на странице - [ссылка](https://github.com/VladimirPodolyan/HTFW/issues)

## Зависимости (ручная установка):
1. [Tox](https://pypi.org/project/tox/)
2. [Chromedriver](https://chromedriver.chromium.org/)

## Зависимости (автоматическая установка):
1. [httpx](https://pypi.org/project/httpx/)
2. [pytest](https://pypi.org/project/pytest/)
3. [allure-pytest](https://pypi.org/project/allure-pytest/)
4. [selenium](https://pypi.org/project/selenium/)
5. [pytest-xdist](https://pypi.org/project/pytest-xdist/)
6. [PyHamcrest](https://pypi.org/project/PyHamcrest/)

Для запуска тестов и создания venv'a используется `Tox`. Установить его можно с помощью команды `pip3 install tox`.

Для UI тестов небходимо наличие `chromderiver` в  переменной окружения `PATH`. 
Для MacOS можно поставить с помощью `brew install chromedriver` 


## Запуск тестов и отчет


### UI & API запуск:
С помощью команды `tox`. UI тесты будут запущены в `headless` режиме в 6 потоков


### UI запуск:
С помощью команды `tox -e py39-ui --`. Тесты будут запущены в `headless` режиме в 6 потоков

### UI отчет:
C помощью `allure serve .tox/.tmp/allure/ui_tests`. Если allure не поставлен на устройство,
то можно запустить из-под venv: `source .tox/dependencies/ui/bin/activate.<terminal> & allure serve..`


### API запуск:
С помощью команды `tox -e py39-api --`

### API отчет:
C помощью `allure serve .tox/.tmp/allure/api_tests`. Если allure не поставлен на устройство,
то можно запустить из-под venv: `source .tox/dependencies/ui/bin/activate.<terminal> & allure serve..`
