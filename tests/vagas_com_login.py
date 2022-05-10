import logging
from scrapper_boilerplate.parser_handler import init_parser
from scrapper_boilerplate import save_to_html
# from jobhunting.utils.output import output
import requests
from time import sleep
import os
import json

user = os.getenv('VAGAS_USER')
password = os.getenv('VAGAS_PASSWORD')


class VagasCom:
    appName = "[Vagas.com]"
    targetLink = []

    def __init__(self, chromedriver_path="", headless=True):
        self.chromedriver_path = chromedriver_path
        self.headless = headless
        # self.driver = setSelenium("https://www.vagas.com.br", self.chromedriver_path, headless=self.headless)
        logging.info(f'{self.appName} Iniciando...')
        self.session = requests.Session()

    def login(self, login, password):
        before_login = requests.get('https://www.vagas.com.br/login-candidatos')
        if before_login.status_code != 200:
            raise Exception('Não foi possível acessar o site')
        
        # Login page
        soap = init_parser(before_login.text)
        auth_token = soap.find('input', {'name': 'authenticity_token'})['value']
        if not auth_token:
            raise Exception('Não foi possível pegar o token de autenticação')
        
        print(f'Token: {auth_token}')

        with self.session as session:
            headers = {
                "content-type": "application/x-www-form-urlencoded",
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                "cookie": "_gid=GA1.3.1675867930.1652125017; _hjid=7eb62814-2988-44a0-8ba2-6de00ca52f90; _hjSessionUser_872841=eyJpZCI6IjUxNDJkMjlmLTdiYjEtNWM5Mi04Y2ExLTI4ZGI1NjRkNmQwNSIsImNyZWF0ZWQiOjE2NTIxMjUwMzc2MjYsImV4aXN0aW5nIjp0cnVlfQ==; _gcl_au=1.1.1120965670.1652125043; tt.u=0100007FDE3DE061B40693A7028A9017; __Secure-Spvll=97cfb434f6ba328ab09efcc9b3c3bd2002400011b1cbd65c2dc9c9c9f9dfb7b9.746fb5c5959043be38b5a740f18f549b29f89a39b5dbddf289b27f366e0141b9.8398; tt.nprf=; uuid=6308974f5a1f508f8fd44927d328bd5317ae5ee811f410dc09; _hjSession_872841=eyJpZCI6ImJjODgyNzNkLWEwZWMtNDVhMS1iNzc2LTM4ZDI4YmE5OWJjNiIsImNyZWF0ZWQiOjE2NTIxODgwMjg5OTQsImluU2FtcGxlIjpmYWxzZX0=; tt_c_vmt=1652188042; tt_c_m=direct; tt_c_s=direct; tt_c_c=direct; _ttdmp=E:1|X:3|LS:|CA:CA14877; vagas_portinari_locale=pt-BR; IntegracaoParamPesq=h%5B%5D%3D30%26q%3Dpython%26c%5B%5D%3DS%C3%A3o+Paulo; IntegracaoUrlPesq=%2Fvagas-de-python-em-sao-paulo%3Fh%5B%5D%3D30%26c%5B%5D%3DS%C3%A3o+Paulo; IntegracaoIdioma=_ptBR; IntegracaoCodigoDaVaga=2370984; IntegracaoReferer=https%3A%2F%2Fwww%2Evagas%2Ecom%2Ebr%2F; VagasColorCust=0; NovoCand=; VagasMultilingue=1; PAPesq=; VagasIdiomaNav=%5FptBR; VagasCode=57872399; VagasType=c; IntegracaoUrl=https%3A%2F%2Fwww.vagas.com.br%2Fvagas-de-python-em-sao-paulo%3Fh%255B%255D%3D30; IntegracaoServico=finalizar_sessao; IntegracaoCodigo=; IntegracaoTipo=; IntegracaoHash=; IntegracaoLoginTipo=; IntegracaoLoginCodigo=; IntegracaoLoginHash=; __cf_bm=aX6E.1Nmfwc90V7rJHRdZUEjvLmsRKkXB4T5dmSdkBs-1652189113-0-AWzr1cxZmwHedwnIgY2KxD680iZkZAQDzG6QXTIpZ6DhaMZhXQfGGrs4YYeVAer4958KHlQS+PfWpE493Doe6Hn5/eMf0HC3vqahJ3VhmPkzYqLKl8nStl0sAKzrSW8XN1cB/ngBGg1S5J4SRvDD3k1wZphMx1fDGqhrbfNVzagL; _gat=1; _dc_gtm_UA-19374950-30=1; vagas.com.br=eUZjNnFMK2x2dTVjTWFlaVNYbkZ0QWFrRmxNMzlkUE1SemlzKzFRU3Mzd0E4bWVWQXc2T1hSeTFMTlV5MXQ1RjlYUlowb0h2MEx4RElTTFlDTTBPS004VXpWeEhPZ1RwOG5Ud3FDaGFFWEp5RDlnd2N3c3pXRFdObEdtNFM3Z3A2NmhWL3QyZXV4d0tiZ3R3R2o4aHV0Z28zY014QUc5RkJSa2FXSE5BcUFYdEV1eXcwSFY2TWc1VnpjZENjTjQvdko1Z1cwTnRERkZTTEN3VUFwYjRsQXViM3NYZzJ0T2RnVW1FMGhyRUdBUFNPaGl0eUYyWFA4eTZsa3pVZFNiM3NOaFF6Vlk3dlpIYkRQUmx0QU1zcjl5RGkwWkQyaGpUbnhIK0JVVitBdnY2ZWtmb2JUSTFkMFFHM0VScGpLN3BUSUxyTlhseWpxMlRNN1JvL2ZKdXJ4dFhSd0JScTc5Ymt0L3Y3ZDBkNDhrPS0tL1FxUXlGWkE3aTV1c2tZclZvZFVDQT09--15c079aed4b77538de6dfe3e63d9d3ab11778d9b; _ga_9QXBCPYCMW=GS1.1.1652188039.3.1.1652189114.50; _ga=GA1.3.979970721.1652125017; _dc_gtm_valor-indisponivel=1; _ttuu.s=1652189120666"
            }

            payload = {
                "utf8": "✓",
                "authenticity_token": auth_token,
                'login_candidatos_form[usuario]:': login, 
                'login_candidatos_form[senha]': password,
                "login_candidatos_form[idioma_id]:": '', 
                "commit": "Entrar"
            }
            req = session.post('https://www.vagas.com.br/login-candidatos', headers=headers, data=json.dumps(payload))
            print(req)
            if req.status_code == 200:
                req = session.get('https://www.vagas.com.br/vagas-de-python-em-sao-paulo?h%5B%5D=30')
                soap = init_parser(req.text)

                print('Usuário:', soap.find('a', id="usuario-logado").text)
                links = soap.find_all('a', {'class': 'link-detalhes-vaga'})
                for link in links:
                    print(link['href'])


    def insertJob(self, job):
        pass

    def searchOptions(self):
        # filter jobs-options
       pass

    def selectJobs(self):
        pass

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


vagas = VagasCom()
vagas.login(user, password)