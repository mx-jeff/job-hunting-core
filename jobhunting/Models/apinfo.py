from selenium.webdriver.common.keys import Keys
from time import sleep
from src.config import setSelenium


class Apinfo:
    appName = '[APinfo]'
    jobsLink = []

    def __init__(self):
        '''
        init the webrowser

        return:=> none
        '''
        self.driver = setSelenium('https://www.apinfo.com/apinfo/')
        print(f'{self.appName} Iniciando...')

    def searchJob(self, job):
        '''
        job:=> insert a job for require to insert
        return:=> none
        '''

        print(print(f'{self.appName} Selecionando vaga...'))
        driver = self.driver
        self.searchBar = driver.find_element_by_id('i-busca')
        self.searchBar.send_keys(job)
        self.searchBar.send_keys(Keys.ENTER)
        print(f'{self.appName} Feito!, buscando vagas para {job}')      

    def selectJob(self):
        print(f'{self.appName} Vaga localizada!')
        
        # try click on button
        # self.button = self.driver.find_element_by_class_name('btn3 ')
        # self.button.click()

        container = self.driver.find_element_by_id('vagas')
        buttons = container.find_elements_by_class_name('btn3 ')
        for button in buttons:
            print(button.get_attribute('href'))

    def subscribeJob(self):
        CPF = '######'
        PASSWORD = '######'

        driver = self.driver

        driver.find_element_by_id('cpf').send_keys(CPF)
        driver.find_element_by_id('chave3').send_keys(PASSWORD)

        driver.find_element_by_xpath('//*[@id="form-incluir-cv"]/div[6]/input').click()

    def wait(self, secs=10):
        '''
        wait actions, give time to load if necessary

        secs => seconds that you want to wait
        return => none
        '''
        print(f'{self.appName} Waiting {secs} secs')
        sleep(secs)

    def close(self):
        '''
        quit the web browser

        return:=> none
        '''
        print(f'{self.appName} closing...')
        self.driver.quit()
