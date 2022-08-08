import sys
from jobhunting.Models.Infojobs import Infojobs
from scrapper_boilerplate import setSelenium


def searchInfojob(jobTarget, user, password, driver):
    """
    Infojobs automatic subscription job

    :jobTarget: target job to subsscribe
    :login: infojobs user to login
    :password: password to login
    """
        
    jobs = Infojobs(driver)
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
        print(f'{site_job} Feito!, buscando vagas para {job_type}')

        print(f'{site_job} Selecionando vagas disponiveis...')
        jobs.getJob()
        print(f'{site_job} {len(jobs.jobsLink)} Vagas selecionadas!')

        success = 0
        fail = 0
        print(f"{site_job} Se inscrevendo nas vagas...")
        
        for index, target in enumerate(jobs.jobsLink):
            try:
                print(f'{site_job} Inscrevendo na vaga {index+1} de {len(jobs.jobsLink)}')
                if target.startswith("https://") or target.startswith("http://"):
                    status = jobs.subscribeJob(target)
                    if status:
                        print(f'{jobs.appName} Vaga inscrita com sucesso!')
                        success += 1
                    else:
                        print(f'{jobs.appName} Erro de inscrição!')
                        fail += 1
            
            except KeyboardInterrupt:
                print(f'{site_job} Interrompendo...')
                jobs.quitSearch()
                break

        print(f'{jobs.appName} Vagas inscritas com sucesso: {success}')
        print(f'{jobs.appName} Vagas com erro de inscrição: {fail}')

    except Exception as error:
        # jobs.quitSearch()
        print(f"{jobs.appName} Algum problema ocorreu e/ou as inforamções estão erradas!")
        print(f"{jobs.appName} Erro {error}, contate o adminstrador do sistema")    

    except KeyboardInterrupt:
        print('Saindo, volte sempre!')
        jobs.quitSearch()
