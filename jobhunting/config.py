from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os import environ
import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def setSelenium(link, chromedrover_path, headless):
    options = Options()
    options.binary_location = environ.get('GOOGLE_CHROME_BIN')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-logging")

    # headles chrome, turn False to display screen
    if headless:
        options.add_argument('--headless')

    options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36')
    options.add_argument("--disable-blink-features")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)

    # path to chromedriver
    # Remove .env chromepath later
    path = chromedrover_path if chromedrover_path != "" else environ.get('CHROMEDRIVER_PATH')

    driver = webdriver.Chrome(path, options=options)
    driver.get(link)
    driver.implicitly_wait(10)

    return driver

