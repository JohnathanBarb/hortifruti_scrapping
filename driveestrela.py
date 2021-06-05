from requests import get
from bs4 import BeautifulSoup as bs4
from datetime import date

base_url = 'https://drive.supermercadoestrelaazul.com.br'
produtos = []

url_get = f'{base_url}/t/departamentos/hortifruti'
while True:
    page_source = get(url_get).text
    print(f'getting {url_get}')
    soup = bs4(page_source, 'html.parser')
    boxes = soup.find_all('div', {'class': 'product'})
    
    for box in boxes:
        link = box.find('div', {'class': 'text'}).find('a')['href']
        page_box = get(f'{base_url}{link}').text
        print(f'getting {base_url}{link}')
        soup_box = bs4(page_box, 'html.parser')
        title = soup_box.find('h2', {'class': 'product-name'}).text
        descricao = title.strip().split('\n')[0]
        ref = title.strip().split('\n')[1].strip()[6:-1]
        preco = soup_box.find('h4', {'class': 'principal'}).find('span').text
        produtos.append({'descricao': descricao, 'preco': preco, 'ref': ref})

    try:        
        next = soup.find('a', {'class': 'btn btn-light btn-block-responsive'})['href']
        url_get = f'{base_url}{next}'
    except TypeError:
        break


date_now = date.today()
dia = date_now.strftime('%d')
mes = date_now.strftime('%m')
ano = date_now.strftime('%Y')


with open('./output/{}{}{}_hortifrutiestrela.csv'.format(ano, mes, dia), 'w+') as _file:
    _file.write('Codigo;Descricao;Preco\n')
    for produto in produtos:
        _file.write('{};{};{}\n'.format(produto['ref'], produto['descricao'], produto['preco']))



