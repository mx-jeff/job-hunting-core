# job-hunting

A automated job finder that find and subscribe in job

## instalation

Installed via pip:

```python
pip install job-hunting
```

or from source:

```python
python setup.py
```

and make sure that you download [chromedriver]("https://chromedriver.chromium.org/downloads") that matches your chrome browser version

and create a ".env" file in your root directory and input the chromdrive path on it

```.env
CHROMEDRIVER_PATH="Your chromedrive path"
```

## Usage 

with vagas.com

```Python
from jobhunting.Models.vagasCom import VagasCom


def searchVagasCom(targetJob, vagasUser, vagasPassword, headless):
    vagas = VagasCom(chromedriver_path="C:\Selenium\chromedriver.exe", headless=headless)
    targetJob = "bots"
    job_site = vagas.appName
    
    print(f'{job_site} Iniciando...')
    try:
        print(f'{job_site} Tentando logar...')
        if not vagas.login(vagasUser, vagasPassword):
            print(f'{job_site} Login inválido ou campos errados!')
            vagas.quitSearch()
            return 

        print(f'{job_site} logado com sucesso!')

        print(f'{job_site} A selecionar vaga...')
        vagas.insertJob(targetJob)
        print(f'{job_site} Vaga selecionada!')

        print(f'{job_site} A ajustar opções...')
        vagas.searchOptions()
        print(f'{job_site} Feito!')

        print(f'{job_site} Listando Vagas...')
        vagas.selectJobs()
        print(f'{job_site} Feito!')
        print(f"{len(vagas.targetLink)} vagas encontradas!")

        success = 0
        fail = 0
        print(f"{job_site} Se inscrevendo nas vagas...")
        
        try:
            for index, target in enumerate(vagas.targetLink):
                if target.startswith("https://") or target.startswith("http://"):
                    status = vagas.subscribeJob(target)
                    if status == "Vaga cadastrada!":
                        success += 1

                    else:
                        fail += 1

                    print(f"{job_site} {index + 1} vaga, status: {status}")
        
        except Exception:  
            print(f"{job_site} erro ao se inscrever!")
        
        finally:
            vagas.quitSearch()

        print(f'Vagas inscritas {success}')
        print(f'Vagas ja inscritas anteriomente ou requer preenchimento adicional: {fail}')

    except Exception as error:
        print("Algum problema ocorreu e/ou as informações estão erradas!")
        # vagas.quitSearch()
        raise

    except KeyboardInterrupt:
        print('Saindo, volte sempre!')
        vagas.quitSearch()
        

```
or with infojobs

```python
from jobhunting.Models.Infojobs import Infojobs


def searchInfojob(jobTarget, user, password, headless):
    """
    Infojobs automatic subscription job

    :jobTarget: target job to subsscribe
    :login: infojobs user to login
    :password: password to login
    """
    jobs = Infojobs(chromedriver_path="Your chromedriver path", headless=headless)
    site_job = jobs.appName
    job_type = jobTarget

    try:
        print(f'{site_job} Iniciando...')
        print(f'{site_job} Tentando logar...')
        
        if not jobs.login(user, password):
            print(f"{site_job} Login inválido ou campos errados!")
            jobs.quitSearch()
            sys.exit()

        print(f'{site_job} Selecionando vaga...')
        jobs.searchList(job_type)
        print(f'{site_job} Feito!, buscando vagas para {site_job}')

        print(f'{site_job} Ajustando opções...')
        jobs.searchOptions()
        print(f"{site_job} Feito!")

        print(f'{site_job} Selecionando vagas disponiveis...')
        jobs.getJob()
        print(f'{site_job} {len(jobs.jobsLink)} Vagas selecionadas!')

        success = 0
        fail = 0
        print(f"{site_job} Se inscrevendo nas vagas...")
        
        for index, target in enumerate(jobs.jobsLink):
            if target.startswith("https://") or target.startswith("http://"):
                status = jobs.subscribeJob(target)
                if status == "Vaga cadastrada!":
                    success += 1

                else:
                    fail += 1

                print(f"{site_job} {index + 1} vaga, status: {status}")

        jobs.quitSearch()

        print(f'Vagas inscritas {success}')
        print(f'Vagas ja inscritas anteriomente ou requer preenchimento adicional: {fail}')

    except Exception as error:
        jobs.quitSearch()
        print("Algum problema ocorreu e/ou as inforamções estão erradas!")
        print(f"Erro {error}, contate o adminstrador do sistema")

    except KeyboardInterrupt:
        print('Saindo, volte sempre!')
        jobs.quitSearch()

```