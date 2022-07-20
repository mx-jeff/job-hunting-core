from jobhunting.Models.Infojobs import Infojobs
from scrapper_boilerplate import setSelenium
from dotenv import load_dotenv
from jobhunting.utils.load_txt import load_jobs_in_txt

from time import sleep
import os
import unittest


class TestSubscribeJob(unittest.TestCase):

    def setUp(self) -> None:
        load_dotenv()
        self.jobs = load_jobs_in_txt()

    def test_subscribe_job(self):
        self.driver = setSelenium(headless=False, remote_webdriver=True, profile=True)
        self.infojobs = Infojobs(self.driver)
        self.infojobs.login(os.getenv('INFOJOBS_USER'), os.getenv('INFOJOBS_PASSWORD'))

        sucess = 0
        fail = 0

        for jobs in self.jobs[:10]:
            status = self.infojobs.subscribeJob(jobs)
            # self.assertTrue(status)
            if status:
                print(f'{self.infojobs.appName} Vaga inscrita com sucesso!')
                sucess += 1
            else:
                print(f'{self.infojobs.appName} Erro de inscrição!')
                fail += 1
        
        print(f'{self.infojobs.appName} Vagas inscritas com sucesso: {sucess}')
        print(f'{self.infojobs.appName} Vagas com erro de inscrição: {fail}')

    def tearDown(self) -> None:
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
