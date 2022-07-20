import os
import unittest
import logging

from dotenv import load_dotenv
from time import sleep

from scrapper_boilerplate import setSelenium, explicit_wait
from scrapper_boilerplate.warnings import disable_warnings

from jobhunting.Models.vagasCom import VagasCom


class TestVagasLogin(unittest.TestCase):
    def setUp(self):
        # disable_warnings()
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filename='test_login.log', filemode='w')
        load_dotenv()
        self.user = os.getenv('VAGAS_USER')
        self.password = os.getenv('VAGAS_PASSWORD')

    def test_search(self):
        self.driver = setSelenium(headless=False, remote_webdriver=True, profile=True)
        self.vagas = VagasCom(self.driver)


        self.driver.get('https://www.vagas.com.br/vagas-de-python')
        status = self.vagas.selectJobs()
        [ print(job) for job in self.vagas.targetLink ]
        sleep(5)
        # with open('tests/vagas_com/mock/jobs.txt', 'a') as f:
        #     for job in self.vagas.targetLink:
        #         f.write(job + '\n')

        self.assertGreater(len(self.vagas.targetLink), 1)

    def test_search_headless(self):
        self.driver = setSelenium(headless=True, remote_webdriver=True, profile=True)
        self.vagas = VagasCom(self.driver)

        self.driver.get('https://www.vagas.com.br/vagas-de-python')
        status = self.vagas.selectJobs()
        [ print(job) for job in self.vagas.targetLink ]
        sleep(5)
        # with open('tests/vagas_com/mock/jobs.txt', 'a') as f:
        #     for job in self.vagas.targetLink:
        #         f.write(job + '\n')

        self.assertGreater(len(self.vagas.targetLink), 1)

    def tearDown(self) -> None:
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
