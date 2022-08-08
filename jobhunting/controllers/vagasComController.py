from asyncio.log import logger
from jobhunting.Models.vagasCom import VagasCom
import logging


def searchVagasCom(targetJob, vagasUser, vagasPassword, driver):

    vagas = VagasCom(driver)
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

        print(f'{job_site} Listando Vagas...')
        vagas.selectJobs()
        print(f'{job_site} Feito!')
        print(f"{job_site} {len(vagas.targetLink)} vagas encontradas!")

        success = 0
        fail = 0
        print(f"{job_site} Se inscrevendo nas vagas...")
        
        try:
            for index, target in enumerate(vagas.targetLink):
                try:
                    print(f'{job_site} Inscrevendo na vaga {index+1} de {len(vagas.targetLink)}\nVaga: {target}')
                    if target.startswith("https://") or target.startswith("http://"):
                        status = vagas.subscribeJob(target)
                        if status:
                            success += 1

                        else:
                            fail += 1

                        print(f"{job_site} {index + 1} vaga, status: {'cadastrada' if status else 'já cadastrada ou erro de inscrição'}")
                        
                except KeyboardInterrupt:
                    print(f'{job_site} Interrompido!')
                    break
        
        except Exception:
            # raise  
            print(f"{job_site} erro ao se inscrever!")

        print(f'Vagas inscritas {success}')
        print(f'Vagas ja inscritas anteriomente ou requer preenchimento adicional: {fail}')

    except Exception as error:
        logging.error(error)
        print("Algum problema ocorreu e/ou as informações estão erradas!")
        raise

    except KeyboardInterrupt:
        print('Saindo, volte sempre!')        
        return
