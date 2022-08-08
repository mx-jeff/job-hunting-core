from time import sleep
import logging

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, InvalidSessionIdException

from jobhunting.utils import timer, alert
from jobhunting.utils.sanitize_input import sanitize_input
from jobhunting.credentails import vagasUser, vagasPassword

from scrapper_boilerplate import explicit_wait


class VagasCom:
    appName = "[Vagas.com]"
    targetLink = []

    def __init__(self, driver):
        self.driver = driver
        # self.driver.setWindowSize(1920, 1080)
        logging.info(f'{self.appName} Iniciando...')

    def login(self, login, password):
        driver = self.driver
        
        try:
            logging.info(f'{self.appName} Tentando logar...')

            # Click on login page
            driver.get('https://www.vagas.com.br/login-candidatos')
            timer()

            # insert credentials and login-in
            login_url = driver.current_url
            driver.find_element(By.ID, 'login_candidatos_form_usuario').send_keys(login or vagasUser)
            driver.find_element(By.ID, 'login_candidatos_form_senha').send_keys(password or vagasPassword)
            driver.find_element(By.ID, 'submitLogin').click()
            timer()
            if self.driver.current_url == login_url:
                logging.info(f'{self.appName} Login inválido ou campos errados!')
                # check if this message was sent
                return

        except Exception as error:
            logging.info(f"{self.appName} Error: {error}")
            return

        logging.info(f'{self.appName} Logado com sucesso')
        timer()
        return True

    def insertJob(self, job, city="sao-paulo"):
        driver = self.driver
        job = sanitize_input(job)

        logging.info(f'{self.appName} A selecionar vaga...')
        driver.get(f'https://www.vagas.com.br/vagas-de-{job}-em-{city}')
        explicit_wait(driver, By.TAG_NAME, 'body')

        logging.info(f'{self.appName} Vaga selecionada!')
        return True

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
        logging.debug(f'{self.appName} Listando Vagas...')
        driver = self.driver

        explicit_wait(driver, By.TAG_NAME, 'h1')
        try:
            container = driver.find_element(By.ID, 'pesquisaResultado')

            links = container.find_elements(By.TAG_NAME, 'a')

            # save all links 
            self.targetLink = [link.get_attribute('href') for link in links]
            
            logging.debug(f'{self.appName} Feito!')
        
        except Exception:
            raise

        return True

    @staticmethod
    def saveFile(html):
        with open('file.html','w') as file:
            file.write(html)

    def subscribeJob(self, link):
        logging.info(f'{self.appName} Se inscrevendo na vaga...')
        driver = self.driver

        # Job page            
        driver.get(link)
        timer()
        explicit_wait(driver, By.TAG_NAME, 'h1')
        title = driver.find_element(By.TAG_NAME, 'h1').text
        logging.info(link)
        logging.info(title)

        try:
            try:
                job_imconpatility = driver.find_element(By.CSS_SELECTOR, 'div.job-incompatibility.is-expanded').text
                logging.info(f'{self.appName} Vaga inválida: {job_imconpatility}')
                return False
            
            except NoSuchElementException:
                pass

            try:
                driver.find_element(By.NAME, 'bt-candidatura').click()
            
            except NoSuchElementException:
                try:
                    logging.info(f'{self.appName} Tentando novamente...')
                    try:
                        driver.find_element(By.XPATH, "//*[contains(text(), 'Já me candidatei')]").click()        

                    except NoSuchElementException:
                        driver.find_element(By.XPATH, "//*[contains(text(), 'Candidate-se novamente')]").click() 

                except NoSuchElementException:
                    logging.info(f'{self.appName} Não foi possível se inscrever...')
                    raise
                    return False

            alert(driver)
            timer()

            if "confirmada" in driver.current_url:
                logging.info(f'{self.appName} Inscrição realizada com sucesso!')
                return True

            try:
                driver.find_element(By.XPATH, '//*[@id="LtC"]/td[1]/table/tbody/tr/td[1]/a').click()
                return True

            except Exception as e:
                logging.error(e)
                return False
                
        except Exception as error: 
            logging.error(f"{self.appName} Error: {error}")
            raise
            return False

    def quitSearch(self):
        logging.info(f'{self.appName} Saindo... volte sempre :)')
        self.driver.quit()
        