from lxml.html import parse
import pymongo, json

def save(keys, data):    
    keys_dict = {}
    for k in keys:
        keys_dict[k] = data[k]
    col.update(keys_dict,data,True)
    return data

soup = parse("http://www.al.sp.gov.br/spl_consultas/consultaProposicoesAction.do?direction=inicio&lastPage=33&currentPage=1&act=detalhe&idDocumento=&rowsPerPage=500&currentPageDetalhe=1&tpDocumento=&method=search&text=&natureId=4002&legislativeNumber=&legislativeYear=&natureIdMainDoc=&anoDeExercicio=&legislativeNumberMainDoc=&legislativeYearMainDoc=&strInitialDate=&strFinalDate=&author=105&supporter=&politicalPartyId=&tipoDocumento=&stageId=&strVotedInitialDate=&strVotedFinalDate=&approved=&rejected=&advancedSearch=#inicio").getroot()

counter = 0
projetos = []
for l in soup.cssselect("tr")[4:-25]:
    data = {}
    data["id"] = counter
    data["data"] = l.cssselect("td")[0].text_content().strip()
    data["ementa"] = l.cssselect("td font a")[0].text_content().strip()
    data["projeto"] = l.cssselect("td font b")[0].text_content().strip() 
    data["url"] = l.cssselect("td font a")[0].get("href")
    data["veto"] = { "governador" : True }
    if data["data"].split("/")[2] == "2013":
        projetos.append(data)
        counter = counter + 1
    

arquivo = open("projetos.json", "w")
arquivo.write(json.dumps(projetos, sort_keys=True, indent=4, separators=(',', ': ')))
arquivo.close()
