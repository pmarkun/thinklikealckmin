from lxml.html import parse
import pymongo, json
import urllib, subprocess, os


PL_DIR = "data/"

def baixaIntegraLei(veto_id):
    if not os.path.isfile(PL_DIR + veto_id + ".d"):
        url = "http://www.al.sp.gov.br/spl_consultas/consultaDetalhesAcessorio.do?act=detalhe&tpDocumento=20&idDocumento=" + str(veto_id)
        soup = parse(url).getroot()
        pl_id = soup.xpath('//font[text()=" Propositura\r\n\t\t\t\t\t"]/following::a')[0].get("href").split("'")[1]
        url = "http://www.al.sp.gov.br/spl_consultas/consultaDetalhesProposicao.do?id=" + str(pl_id) + "&rowsPerPage=1000"
        soup = parse(url).getroot()
        pl_url = soup.xpath('//font[text()=" Documento "]/following::a')[0].get("href")
        pl_cache = urllib.urlopen(pl_url)
        filename = PL_DIR + pl_id + ".doc"
        pl_file = open(filename, 'w')
        pl_file.write(pl_cache.read())
        pl_file.close()
        #converting to markdown
        subprocess.call(["unoconv", "-f", "html", filename])
        subprocess.call(["pandoc", filename[:-4] + ".html", "--strict", "-f", "html","-t", "markdown", "-o", filename[:-4] + ".md"])
        return pl_id
    else:
        print "File " + PL_DIR + veto_id + ".md already exists"

def save(keys, data):    
    keys_dict = {}
    for k in keys:
        keys_dict[k] = data[k]
    col.update(keys_dict,data,True)
    return data

def scrape():
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
        data["veto_id"] = data["url"].split("idDocumento=")[1].split("&")[0]
        data["veto"] = { "governador" : True }
        if data["data"].split("/")[2] == "2013":
            print "Baixando integra..."
            data["pl_id"] = baixaIntegraLei(data["veto_id"])
            projetos.append(data)
            counter = counter + 1
            
        

    arquivo = open("projetos.json", "w")
    arquivo.write(json.dumps(projetos, sort_keys=True, indent=4, separators=(',', ': ')))
    arquivo.close()
