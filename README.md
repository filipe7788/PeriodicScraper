# PeriodicScraper

    Esse scraper tem como objetivo encontrar dados chaves da revista periódica da UFBA 
    Ponto de Acesso e formata-los para que seja feita uma análise sintática dos itens encontrados.


## Tecnologias

    O processo de obtenção do produto desse scraper é dividido em duas etapas:

### Scraper de dados

    Nessa etapa usa-se a linguagem [python](https://www.python.org/downloads/release/python-390/) 
    em sua versão 3.7 como base. 

    Também são utilizadas as dependencias [scrapy](https://scrapy.org/) 
    e [scrapy inline_requests](https://github.com/rmax/scrapy-inline-requests) instaladas via pip.

### Gerador de excel

    Nessa etapa, primeiro importamos o arquivo JSON gerado pelo scraper 
    e separamos a lista de arquivos de cada um em um dataframe específico. 
    
    Após transformar cada palavra-chave em uma coluna 
    com o json_normalize nós colocamos os dataframes 
    em diferentes folhas do mesmo arquivo excel.
    
    Dependencias usadas: pandas e xlsxwriter.

## Instruções de uso

    Para gerar o JSON com os dados do site, rode o comando:
    
    scrapy runspider PeriodicScraper.py -O items.json --set FEED_EXPORT_ENCODING=utf-8

    Após rodar o comando, aparecerá um arquivo "items.json" com todas 
    as informações encontradas no site.

    Para gerar o aquivo excel, rode o comando:

    python3 PeriodicFormatter.py 

    E será gerado um arquivo com os dados formatados corretamente.

## Informações extras

    Caso queira executar a busca pelas *mesmas* informações em outro site, 
    coloque o link dele na lista start_urls encontrada no arquivo PeriodicScraper.py.

