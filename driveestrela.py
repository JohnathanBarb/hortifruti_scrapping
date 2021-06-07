from requests import get
from bs4 import BeautifulSoup as bs4
from datetime import date
import os


# variaveis iniciais para inicio das requisições
base_url = 'https://drive.supermercadoestrelaazul.com.br'
produtos = []
url_get = f'{base_url}/t/departamentos/hortifruti'

while True:

    # requisição para pagina
    page_source = get(url_get).text
    print(f'getting {url_get}')

    # parseamento do codigo fonte do site
    soup = bs4(page_source, 'html.parser')

    # divisão da pagina em boxes
    boxes = soup.find_all('div', {'class': 'product'})

    # iteirar em todas as boxes
    # cada box é um container do produto 
    for box in boxes:

        # ir para a pagina de cada produto
        link = box.find('div', {'class': 'text'}).find('a')['href']
        page_box = get(f'{base_url}{link}').text
        print(f'getting {base_url}{link}')

        # parseamento do codigo fonte de cada produto
        soup_box = bs4(page_box, 'html.parser')
        title = soup_box.find('h2', {'class': 'product-name'}).text
        descricao = title.strip().split('\n')[0]
        ref = title.strip().split('\n')[1].strip()[6:-1]
        preco = soup_box.find('h4', {'class': 'principal'}).find('span').text

        # append à lista de produtos
        produtos.append({'descricao': descricao, 'preco': preco, 'ref': ref})

    # verificar existencia de botão
    try:        
        next = soup.find('a', {'class': 'btn btn-light btn-block-responsive'})['href']
        url_get = f'{base_url}{next}'
    except TypeError:
        break

# data nomeacao de arquivo
date_now = date.today()
dia = date_now.strftime('%d')
mes = date_now.strftime('%m')
ano = date_now.strftime('%Y')


# saida para arquivo YYYYmmdd_hostifrutiestrela.csv
# passando por toda a lista produto e adicionando uma linha à ela
dir_path = os.path.dirname(os.path.realpath(__file__))

outputfolder = os.path.join(dir_path, 'output/')

with open(outputfolder + '{}{}{}_hortifrutiestrela.csv'.format(ano, mes, dia), 'w+') as _file:
    _file.write('Codigo;Descricao;Preco\n')
    for produto in produtos:
        _file.write('{};{};{}\n'.format(produto['ref'], produto['descricao'], produto['preco']))
