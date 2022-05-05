import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, InvalidSessionIdException
from jobhunting.utils import timer, alert

from jobhunting.config import setSelenium
from jobhunting.credentails import vagasUser, vagasPassword
# from jobhunting.utils.output import output
import urllib3
from time import sleep


class VagasCom:
    appName = "[Vagas.com]"
    targetLink = []

    def __init__(self, chromedriver_path="", headless=True):
        self.chromedriver_path = chromedriver_path
        self.headless = headless
        self.driver = setSelenium("https://www.vagas.com.br", self.chromedriver_path, headless=self.headless)
        logging.info(f'{self.appName} Iniciando...')

    def login(self, login, password):
        driver = self.driver
        
        try:
            logging.info(f'{self.appName} Tentando logar...')

            # Click on login page
            driver.find_element_by_id('main-navigation__signin').click()
            timer()

            # insert credentials and login-in
            login_url = driver.current_url
            driver.find_element_by_xpath('//*[@id="login_candidatos_form_usuario"]').send_keys(login or vagasUser)
            driver.find_element_by_xpath('//*[@id="login_candidatos_form_senha"]').send_keys(password or vagasPassword)
            driver.find_element_by_xpath('//*[@id="submitLogin"]').click()
            timer()
            if self.driver.current_url == login_url:
                logging.info(f'{self.appName} Login inválido ou campos errados!')
                # check if this message was sent
                self.quitSearch()
                return False

        except Exception as error:
            logging.info(f"{self.appName} Error: {error}")
            self.quitSearch()
            return

        logging.info(f'{self.appName} Logado com sucesso')
        timer()
        return True

    def insertJob(self, job):
        driver = self.driver

        logging.info(f'{self.appName} A selecionar vaga...')
        # Insert a select job type and click it!
        try:
            driver.implicitly_wait(220)
            driver.find_element_by_xpath('//*[@id="root"]/div/header/div[1]/div[3]/div/section/div[1]/div[1]/input').send_keys(job)
            
            driver.find_element_by_xpath('//*[@id="root"]/div/header/div[1]/div[3]/div/section/div[1]/div[3]/button').click()

        except ElementClickInterceptedException:
            sleep(5)
            driver.find_element_by_xpath('//*[@id="root"]/div/div/div[5]/div[2]').click()
            self.insertJob(job)
        
        else:
            driver.implicitly_wait(220)

        logging.info(f'{self.appName} Vaga selecionada!')

    def searchOptions(self):
        # filter jobs-options
        logging.info(f'{self.appName} A ajustar opções...')
        try:
            driver = self.driver
            timer()

            try:
                # get container of location links
                
                driver.implicitly_wait(0)
                logging.info(f'{self.appName} Ajustando para São paulo...')
                filterSp = driver.find_elements_by_partial_link_text('São Paulo')[0]
                if filterSp:
                    logging.info(f'{self.appName} São paulo achadado')
                    driver.execute_script("arguments[0].click();", filterSp)
            
            except IndexError:
                logging.info(f'{self.appName} Erro aconteceu com a localidade...')
                pass
        
            
            driver.implicitly_wait(220)
            logging.info(f'{self.appName} Ajustado com sucesso!')
            
            timer()
            try:
                driver.implicitly_wait(0)
                logging.info(f'{self.appName} Ajustando para Júnior/Trainee...')
                filterJunior = driver.find_elements_by_partial_link_text('Júnior/Trainee')[0]
                if filterJunior:
                    logging.info(f'{self.appName} Júnior/Trainee achadado')
                    driver.execute_script("arguments[0].click();", filterJunior)

            except IndexError:
                logging.info(f"{self.appName} Não há vagas para junior :(")
                pass
            
            timer()
        
        except Exception as e:
            logging.error(e)
            pass
        logging.info(f'{self.appName} Feito!')

    def selectJobs(self):
        # output(f'{self.appName} Listando Vagas...')
        driver = self.driver

        container = driver.find_element_by_id('pesquisaResultado')
        #return container.get_attribute('outerHTML')

        links = container.find_elements_by_tag_name('a')

        # save all links 
        self.targetLink = [link.get_attribute('href') for link in links]
        
        # output(f'{self.appName} Feito!')
        return True

    @staticmethod
    def saveFile(html):
        with open('file.html','w') as file:
            file.write(html)

    def subscribeJob(self, link):
        # output(f'{self.appName} Se inscrevendo na vaga...')
        driver = self.driver

        # Job page            
        driver.get(link)
        
        try:
            driver.find_element_by_name('bt-candidatura').click()
            
            try:
                timer()
                alert(driver)
                driver.find_element_by_xpath('//*[@id="LtC"]/td[1]/table/tbody/tr/td[1]/a').click()
                return 'Inscrição realizada com sucesso :) '

            except:
                return 'Inscrição realizada com sucesso :) '
                driver.back()
            
        except NoSuchElementException:
            return f'Inscrição realizada anteriormente ;) '

        except Exception as error: 
            return f'Erro na inscrição :( \nError: {error}'

    def quitSearch(self):
        logging.info(f'{self.appName} Saindo... volte sempre :)')
        self.driver.quit()