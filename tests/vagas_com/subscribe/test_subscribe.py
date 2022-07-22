import os
import logging
import unittest

from time import sleep
from dotenv import load_dotenv
from scrapper_boilerplate import setSelenium
from jobhunting.Models.vagasCom import VagasCom


class TestSubscribe(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

        self.driver = setSelenium(headless=False, remote_webdriver=True)
        self.vagas = VagasCom(self.driver)
        self.user = os.getenv('VAGAS_USER')
        self.password = os.getenv('VAGAS_PASSWORD')

    def test_subscribe(self):
        self.vagas.login(self.user, self.password)
        # with open('tests/vagas_com/mock/jobs.txt', 'r') as f:
        #     jobs = f.readlines()

        success = 0
        fail = 0
        # for job in jobs:
        status = self.vagas.subscribeJob("https://www.vagas.com.br/vagas/v2398620/developer-front-end")
        sleep(10)
        if status == 1:
            success += 1
        else:
            fail += 1

        print(f'Success: {success}')
        print(f'Fail: {fail}')


    def tearDown(self):
        self.driver.quit()
    

if __name__ == "__main__":
    unittest.main()
