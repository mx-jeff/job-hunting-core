import sys


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

def alert(browser):
    alert = browser.switch_to.alert
    alert.accept()    

def remove_duplicates_from_list(x:list):
    return list(dict.fromkeys(x))
