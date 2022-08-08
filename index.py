from sqlalchemy import true
from jobhunting.credentails import vagasPassword, vagasUser, user, password
from jobhunting.controllers.vagasComController import searchVagasCom
from jobhunting.controllers.infojobsController import searchInfojob
from scrapper_boilerplate import setSelenium

import logging
import sys
import warnings


if not sys.warnoptions:
    warnings.simplefilter("ignore")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

def main():
    with setSelenium(headless=True, remote_webdriver=True, profile=False) as driver:
    # driver = setSelenium(headless=False, remote_webdriver=True, profile=False)
        # searchVagasCom('javascript', vagasUser, vagasPassword, driver)
        driver.set_window_size(1200, 800)
        searchInfojob('php', user, password, driver)
        

if __name__ == "__main__":
    main()
