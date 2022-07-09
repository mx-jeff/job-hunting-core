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
        self.driver.get("https://www.infojobs.com.br/empregos.aspx?Palabra=robo&Provincia=64")
        infojobs.getJob()
        print(len(infojobs.jobsLink))
        self.assertGreater(len(infojobs.jobsLink), 0, msg="Done!")

    def test_search_headless(self):
        self.driver = setSelenium(headless=True, remote_webdriver=True, profile=True)
        infojobs = Infojobs(self.driver)
        self.driver.get("https://www.infojobs.com.br/empregos.aspx?Palabra=robo&Provincia=64")
        infojobs.getJob()
        print(len(infojobs.jobsLink))
        self.assertGreater(len(infojobs.jobsLink), 0, msg="Done!")

    def tearDown(self) -> None:
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
