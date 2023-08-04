import csv
import requests
from bs4 import BeautifulSoup

url = 'https://www.biasiswamalaysia.com/'
max_pages = 21

with open('sch.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Description'])

    for page_number in range(1, max_pages+1):
        page_url = url + 'page/' + str(page_number) + '/'
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        sch = soup.find_all('article')

        if len(sch) == 0:
            break

        for article in sch:
            title_element = article.find('h2')

            if title_element is not None:
                title = title_element.text.strip()
            else:
                title = 'No title available'

            description_element = article.find('div', class_='entry-content')

            if description_element is not None and description_element.p is not None:
                description = description_element.p.text.strip()
            else:
                description = 'No description available'

            writer.writerow([title, description])
