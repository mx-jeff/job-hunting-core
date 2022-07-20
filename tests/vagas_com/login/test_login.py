import unittest
import os

from dotenv import load_dotenv
from jobhunting.credentails import vagasPassword, vagasUser
from scrapper_boilerplate import setSelenium
from scrapper_boilerplate.warnings import disable_warnings
from jobhunting.Models.vagasCom import VagasCom
import logging


class TestVagasLogin(unittest.TestCase):
    def setUp(self):
        # disable_warnings()
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filename='test_login.log', filemode='w')
        load_dotenv()
        self.user = os.getenv('VAGAS_USER')
        self.password = os.getenv('VAGAS_PASSWORD')
        self.driver = setSelenium(headless=False, remote_webdriver=True, profile=False)
        self.vagas = VagasCom(self.driver)
    
    def test_login(self):
        status = self.vagas.login(vagasUser, vagasPassword)
        self.assertTrue(status)

    def tearDown(self) -> None:
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
        