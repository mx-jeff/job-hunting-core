from jobhunting.Models.Infojobs import Infojobs
import sys


def searchInfojob(jobTarget, user, password, headless):
    """
    Infojobs automatic subscription job

    :jobTarget: target job to subsscribe
    :login: infojobs user to login
    :password: password to login
    """
    jobs = Infojobs(chromedriver_path="C:\Selenium\chromedriver.exe", headless=headless)
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
