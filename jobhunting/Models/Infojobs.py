from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException,  ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from time import sleep
from jobhunting.config import setSelenium
from jobhunting.credentails import user, password
from jobhunting.utils import remove_duplicates_from_list


class Infojobs:
    appName = '[Infojobs]'
    jobsLink = []

    def __init__(self, chromedriver_path="", headless=True):
        self.chromedriver_path = chromedriver_path
        self.headless = headless
        self.driver = setSelenium('http://www.infojobs.com.br', self.chromedriver_path, headless=self.headless)

    def login(self, login, user_password):
        """
        Login to Infojobs, with credentials
        :return: None
        """
        # output(f'{self.appName} Tentando logar...')        
        
        try:
            self.driver.get('https://login.infojobs.com.br/Account/Login')
        
        except:
            # output(f"{self.appName} Passando verificação de cookies")
            self.clearCookie()
            sleep(5)
            self.loginForm = self.driver.find_element_by_xpath('//*[@id="ctl00_cAccess_aLogin"]')
            self.loginForm.click()


        current_url = self.driver.current_url
        self.inputForm = self.driver.find_element_by_xpath('//*[@id="Username"]')
        self.inputForm.send_keys(login or user)

        self.passwordForm = self.driver.find_element_by_xpath('//*[@id="Password"]')
        self.passwordForm.send_keys(user_password or password)

        try:
            self.submitButton = self.driver.find_element_by_css_selector('[value="login"]')
            self.submitButton.click()

        except (ElementClickInterceptedException, ElementNotInteractableException):
            print(f'{self.appName} limpando popup')
            self.clear_popup()
            print(f'{self.appName} popup limpo!')
            self.submitButton = self.driver.find_element_by_css_selector('[value="login"]')
            self.submitButton.click()

        else:
            sleep(5)
        
        if self.driver.current_url == current_url:
            self.quitSearch()
            return False
            # check if this message was sent

        return True

    def searchList(self, jobType):
        """
        Go to main page and get the selected job
        :param jobType: Type of job - String
        :return: None
        """
        # output(f'{self.appName} Selecionando vaga...')
        try:
            self.searchJob = self.driver.find_element_by_name('Palabra')
        except:
            try:
                self.searchJob.find_element_by_name('Palabra')

            except:
                raise

        self.searchJob.send_keys(str(jobType))
        self.searchJob.send_keys(Keys.ENTER)

    def searchOptions(self):
        """
        Select the options to customize job options
        :return: None
        """
        # output(f'{self.appName} Ajustando opções...')
        try:
            # Select to São Paulo
            self.cityOptionSaoPaulo = self.driver.find_element_by_xpath(
                '//*[@id="ctl00_phMasterPage_cFacetLocation3_rptFacet_ctl01_chkItem"]').click()
            # Select CLT
            self.cltOption = self.driver.find_element_by_xpath(
                '//*[@id="ctl00_phMasterPage_cFacetContractWorkType_rptFacet_ctl01_chkItem"]').click()

        except:
            sleep(10)
            #if falls, try to click again
            self.cltOption = self.driver.find_element_by_xpath(
                '//*[@id="ctl00_phMasterPage_cFacetContractWorkType_rptFacet_ctl01_chkItem"]').click()

        sleep(10)

    def getJob(self):
        """
        Get links from container of jobs to array and clicks one-by-one
        :return: none
        """
        # output(f'{self.appName} Selecionando vagas disponiveis...')

        job_offer = []

        for _ in range(0, 21):
            try:
                self.driver.implicitly_wait(30)
                
                #jobs container
                self.jobsContainer = self.driver.find_element_by_id('filterSideBar')
                
                # get links
                for items in self.jobsContainer.find_elements_by_tag_name('div'):
                    try:
                        self.driver.implicitly_wait(0)
                        job_link = items.find_element_by_css_selector('a.text-decoration-none').get_attribute('href')

                    except NoSuchElementException:
                        continue

                    else:
                        self.driver.implicitly_wait(30)
                    
                    job_offer.append(job_link)

                self.driver.find_element_by_css_selector('[title="Próxima"]').click()

            except Exception as error:
                # output(error)
                break        

        job_offer = remove_duplicates_from_list(job_offer)

        # print(job_offer)
        if len(job_offer) == 0:
            print(f'{self.appName} Erro ao pegar vagas!')
            return

        self.jobsLink = [link for link in job_offer]
            
    def subscribeJob(self, link):
        #get driver
        driver = self.driver

        driver.get(link)
        sleep(5)
        try:
            # click in link of jobs
            driver.find_element_by_xpath('//*[@id="VacancyHeader"]/div[2]/div[1]/a').click()
            sleep(5)
            # subscribe or not?
            # output(f'{self.appName} Vaga cadastrada!')
            # print(driver.find_element_by_id('ctl00_phMasterPage_divAlert').text)
            return "Vaga cadastrada!"

            # back to jobs container - depreciated
            # driver.back()
            # sleep(5)
            # driver.back()

        except Exception as error:
            return 'Vaga não encontrada!'

    def clearCookie(self):
        try:
            self.driver.find_element_by_id('AllowCookiesButton').click()
        except Exception:
            self.driver.find_element_by_id('didomi-notice-agree-button').click()

    def clear_popup(self):
        self.driver.find_element_by_id('didomi-notice-agree-button').click()

    def quitSearch(self):
        # output(f'{self.appName} Saindo... volte sempre :)')
        self.driver.quit()
