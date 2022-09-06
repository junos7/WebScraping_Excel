import os
import requests
import openpyxl
from config import user, senha

idInicial = 39437
idFinal = 85433
#idFinal = 80321

planilha = openpyxl.load_workbook('planilha.xlsx')
planilhaIds = planilha['Estudantes']

with requests.session() as s:
    s.post('https://www.prppg.ufpr.br/siga/login', data={'login': user, 'password': senha})
    s.get('https://www.prppg.ufpr.br/siga/selecionanivelacesso?comboAcesso=TXSEPX40001016070G0XSEPX47XSEPX6XSEPXXSEPX0XSEPX1')

    for id in range(idInicial, idFinal):

        rInfo = s.get(f'https://www.prppg.ufpr.br/siga/graduacao/discente?d={id}&aba=informacoes')
        nomeDoc = f'arquivos/Aluno - {id}.txt'

        if rInfo.status_code == requests.codes.OK:
            with open(nomeDoc,'wb') as novoArquivo:
                novoArquivo.write(rInfo.content)
                print(f"Documento salvo em {nomeDoc}")

            with open(nomeDoc,'r',encoding='iso8859-1') as arquivo:
                texto = arquivo.readlines()
                for linha in texto:
                    if "grr" in linha:
                        sep1 = linha.split('grr')[1]
                        sep2 = linha.split('grr')[0]
                        idCurriculoAtual = sep2.split('\"')[8].replace(':', '').replace(',', '')
                        status = sep1.split('\"')[24]
                        grr = sep1.split('\"')[2]
                        idCurso = sep1.split('\"')[5].replace(':', '').replace(',', '')
                        nome = sep1.split('\"')[12]
                        lista = [id, idCurso, idCurriculoAtual, grr, nome, status]

                        # passando cada aluno para uma planilha
                        planilhaIds.append(lista)

        else:
            rInfo.raise_for_status()

    planilha.save('novaPlanilha.xlsx')



