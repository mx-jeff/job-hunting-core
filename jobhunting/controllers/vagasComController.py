from jobhunting.Models.vagasCom import VagasCom


def searchVagasCom(targetJob, vagasUser, vagasPassword, headless):
    vagas = VagasCom(chromedriver_path="C:\Selenium\chromedriver.exe", headless=headless)
    targetJob = "python"
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

        # print(f'{job_site} A ajustar opções...')
        # vagas.searchOptions()
        # print(f'{job_site} Feito!')

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
        vagas.quitSearch()
        raise

    except KeyboardInterrupt:
        print('Saindo, volte sempre!')
        vagas.quitSearch()
        
