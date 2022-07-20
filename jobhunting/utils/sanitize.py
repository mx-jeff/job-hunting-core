import logging


def sanitizeWords(dados):
    dados = [str(linha).replace('\n','') for linha in dados]
    
    for dado in dados:
        if dado == "":
            dados.remove(dado)
    return dados


# def credentialsFile():
#     with open('users.txt','r') as txt:
#         linhas = (txt.readlines())
#         dados = sanitizeWords(linhas)    
#         return dados


def getStatusJob(url):
    """
    Sanitize the url to check the status of the job
    :param url: url to check the status of the job
    :return: job status
    """
    
    status = url.split('&')
    logging.debug("status before: ", status)
    status = [ link for link in status if not link.startswith('aff') ]
    status = int(status[-1].split('=')[-1])
    logging.debug("status after: ", status)
    return status
