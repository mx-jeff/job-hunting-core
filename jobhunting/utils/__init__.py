import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException

def table(href, text):
    tamanho = len(href) + 4
    print('~' * tamanho)
    print(str(text).center(tamanho))
    print()
    print(str(href))
    print('~' * tamanho)
    print()

def timer(secs=5):
    from time import sleep

    sleep(secs)


def alert(driver, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
        driver.switch_to.alert.accept()   
    
    except TimeoutException:
        pass


def remove_duplicates_from_list(x:list):
    return list(dict.fromkeys(x))
