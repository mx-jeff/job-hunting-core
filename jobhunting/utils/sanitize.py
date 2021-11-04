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