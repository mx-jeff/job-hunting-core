import logging
from time import sleep

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException,  ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from jobhunting.credentails import user, password
from jobhunting.utils import remove_duplicates_from_list
from jobhunting.utils.sanitize import getStatusJob
from jobhunting.const import DEBUG, QUANTITY_OF_PAGES
from scrapper_boilerplate import explicit_wait, load_code
from uuid import uuid4


class Infojobs:
    appName = '[Infojobs]'
    jobsLink = []

    def __init__(self, driver):
        self.driver = driver

    def login(self, login, user_password):
        """
        Login to Infojobs, with credentials
        :return: None
        """
        login_url = 'https://login.infojobs.com.br/Account/Login'
        logging.info(f'{self.appName} Tentando logar...')        
        self.driver.get(login_url)

        explicit_wait(self.driver, By.TAG_NAME, 'body')
        if self.driver.current_url != login_url:
            logging.info(f'{self.appName} Já está logado!')
            return

        logging.info(f"{self.appName} Passando verificação de cookies")
        explicit_wait(self.driver, By.TAG_NAME, 'body')
        self.clearCookie()

        self.inputForm = self.driver.find_element(By.XPATH, '//*[@id="Username"]')
        self.inputForm.send_keys(login or user)

        self.passwordForm = self.driver.find_element(By.XPATH, '//*[@id="Password"]')
        self.passwordForm.send_keys(user_password or password)

        self.submitButton = self.driver.find_element(By.CSS_SELECTOR, '[value="login"]')
        self.submitButton.click()

        return True

    def searchList(self, jobType):
        """
        Go to main page and get the selected job
        :param jobType: Type of job - String
        :return: None
        """
        logging.info(f'{self.appName} Selecionando vaga...')
        try:
            self.searchJob = self.driver.find_element(By.NAME, 'Palabra')
        except:
            try:
                self.searchJob.find_element(By.NAME, 'Palabra')

            except:
                return

        self.searchJob.send_keys(str(jobType))
        self.searchJob.send_keys(Keys.ENTER)
        return True

    def searchOptions(self):
        """
        Select the options to customize job options
        :return: None
        """
        logging.info(f'{self.appName} Ajustando opções...')
        try:
            # Select to São Paulo
            self.cityOptionSaoPaulo = self.driver.find_element(By.XPATH, 
                '//*[@id="ctl00_phMasterPage_cFacetLocation3_rptFacet_ctl01_chkItem"]').click()
            # Select CLT
            self.cltOption = self.driver.find_element(By.XPATH, 
                '//*[@id="ctl00_phMasterPage_cFacetContractWorkType_rptFacet_ctl01_chkItem"]').click()

        except:
            sleep(10)
            #if falls, try to click again
            self.cltOption = self.driver.find_element(By.XPATH, 
                '//*[@id="ctl00_phMasterPage_cFacetContractWorkType_rptFacet_ctl01_chkItem"]').click()

        sleep(10)

    def getJob(self):
        """
        Get links from container of jobs to array and clicks one-by-one
        :return: none
        """
        logging.info(f'{self.appName} Selecionando vagas disponiveis...')

        job_offer = []

        for i in range(0, QUANTITY_OF_PAGES):
            logging.info(f'{self.appName} Buscando vagas: {i + 1}')
            try:
                #jobs container
                self.jobsContainer = explicit_wait(self.driver, By.ID, "filterSideBar") # self.driver.find_element(By.ID, 'filterSideBar'
                code = load_code(self.jobsContainer)

                # get links
                for items in code.find_all('div'): #self.jobsContainer.find_elements(By.TAG_NAME, 'div'):
                    try:
                        job_link = items.select_one("h2").parent #find_element(By.CSS_SELECTOR, 'a.text-decoration-none').get_attribute('href')
                        job_link = "https://www.infojobs.com.br" + job_link['href']

                    except (NoSuchElementException, AttributeError):
                        continue
                    
                    job_offer.append(job_link)

                self.driver.find_element(By.CSS_SELECTOR, '[title="Próxima"]').click()

            except Exception as error:
                logging.error(error) if DEBUG else logging.error(f'{self.appName} Erro ao buscar vagas')
                continue       

        job_offer = remove_duplicates_from_list(job_offer)

        if len(job_offer) == 0:
            print(f'{self.appName} Erro ao pegar vagas!')
            return

        self.jobsLink = [link for link in job_offer]

    def subscribe(self, driver):
        """
        Subscribe to job
        
        :param driver: Driver of browser"""

        subscribe = explicit_wait(driver , By.CSS_SELECTOR, '.btn.btn-primary.btn-block.js_btApplyVacancy')
        subscribe.click()
        # subscribe or not?
        logging.info(self.driver.current_url)
        status = getStatusJob(self.driver.current_url)
        
        if status == 0:
            logging.info(f'{self.appName} Vaga inscrita com sucesso!')
            return True
        else:
            logging.info(f'{self.appName} Erro de cadastro!')
            driver.save_screenshot(f'screenshot/{self.appName}-{uuid4()}.png') if DEBUG else None
            return

    def subscribeJob(self, link):

        #get driver
        status = False
        driver = self.driver
        driver.get(link)
        logging.info(driver.current_url)
        explicit_wait(driver, By.TAG_NAME, 'body')
        
        try:
            # click in link of jobs
            status = self.subscribe(driver)    

        except Exception as error:
            logging.error(error) if DEBUG else None
            try:
                self.clearCookie()
                status = self.subscribe(driver)
            except Exception as err:
                logging.error(err) if DEBUG else None
                return

        return status

    def clearCookie(self):
        try:
            logging.info(f"{self.appName} Limpando cookies...")
            self.driver.find_element(By.ID, 'AllowCookiesButton').click()
            explicit_wait(self.driver, By.ID, 'AllowCookiesButton').click()
        except Exception:
            pass
        
        try:
            logging.info(f"{self.appName} Removendo popup...")
            self.driver.find_element(By.ID, 'didomi-notice-agree-button').click()

        except Exception:
            pass

    def quitSearch(self):
        logging.info(f'{self.appName} Saindo... volte sempre :)')
        self.driver.quit()
