import os
import unittest 
from jobhunting.Models.Infojobs import Infojobs
from scrapper_boilerplate import setSelenium
from dotenv import load_dotenv


class TestLogin(unittest.TestCase):
    
    def setUp(self) -> None:
        load_dotenv()
        
    def test_login(self):
        self.driver = setSelenium(headless=False, remote_webdriver=True)
        self.infojobs = Infojobs(self.driver)
        status = self.infojobs.login(os.getenv('USER'), os.getenv('PASSWORD'))
        self.assertTrue(status)

    def test_login_headless(self):
        self.driver = setSelenium(headless=True, remote_webdriver=True)
        self.infojobs = Infojobs(self.driver)
        status = self.infojobs.login(os.getenv('USER'), os.getenv('PASSWORD'))
        self.assertTrue(status)

    def tearDown(self) -> None:
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
    