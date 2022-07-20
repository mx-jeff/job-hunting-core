from jobhunting.credentails import vagasPassword, vagasUser, user, password
from jobhunting.controllers.vagasComController import searchVagasCom
from jobhunting.controllers.infojobsController import searchInfojob
from scrapper_boilerplate import setSelenium

import sys
import warnings


if not sys.warnoptions:
    warnings.simplefilter("ignore")


def main():
    with setSelenium(headless=False, remote_webdriver=True, profile=False) as driver:
        # searchVagasCom('robot', vagasUser, vagasPassword, headless=True)
        searchInfojob('bot', user, password, driver)
        

if __name__ == "__main__":
    main()
