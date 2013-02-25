# Você pensa como o Alckmin?
## Aplicativo desenvolvido durante o ODHD

## Objetivo
A ideia do aplicativo é criar uma provocação em cima da relação entre o Executivo Estadual e seu legislativo.

## Instalação
O crawler, feito em python, lê uma [lista de projetos vetados](http://www.al.sp.gov.br/spl_consultas/consultaProposicoesAction.do?direction=inicio&lastPage=33&currentPage=1&act=detalhe&idDocumento=&rowsPerPage=500&currentPageDetalhe=1&tpDocumento=&method=search&text=&natureId=4002&legislativeNumber=&legislativeYear=&natureIdMainDoc=&anoDeExercicio=&legislativeNumberMainDoc=&legislativeYearMainDoc=&strInitialDate=&strFinalDate=&author=105&supporter=&politicalPartyId=&tipoDocumento=&stageId=&strVotedInitialDate=&strVotedFinalDate=&approved=&rejected=&advancedSearch=#inicio) e gera um arquivo projetos.json contendo informações básicas sobre a lei.
A função 'baixaIntegraLei' pega o id de um veto, busca seu projeto correlato, baixa e armazena a versão original (doc), uma conversão em html e outra em markdown - todos na pasta 'data' e usando o id do projeto como nome do arquivo.

## Pré requisitos
* Python
    * [lxml](http://lxml.de/) - para parsing e scraping
* [Unoconv](http://dag.wieers.com/home-made/unoconv/) - para conversão de doc em html
* [Pandoc](http://johnmacfarlane.net/pandoc/) - para conversão de html em markdown

