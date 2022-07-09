import os
import unittest
from jobhunting.Models.Infojobs import Infojobs
from scrapper_boilerplate import setSelenium
from dotenv import load_dotenv


class TestLogin(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
    
    def test_search(self):
        self.driver = setSelenium(headless=False, remote_webdriver=True, profile=True)
        infojobs = Infojobs(self.driver)
        infojobs.login(os.getenv('USER'), os.getenv('PASSWORD'))
        status = infojobs.searchList('Desenvolvedor')
        print(self.driver.current_url)
        self.assertTrue(status)
        # https://www.infojobs.com.br/empregos.aspx?Palabra=Desenvolvedor&Provincia=64

    def test_search_headless(self):
        self.driver = setSelenium(headless=True, remote_webdriver=True, profile=True)
        infojobs = Infojobs(self.driver)
        infojobs.login(os.getenv('USER'), os.getenv('PASSWORD'))
        status = infojobs.searchList('Desenvolvedor')
        print(self.driver.current_url)
        self.assertTrue(status)

    def tearDown(self) -> None:
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
