import requests
from bs4 import BeautifulSoup

url = 'https://afterschool.my/scholarship'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
scholarship_divs = soup.find_all('div', {'class': 'common'})

for scholarship_div in scholarship_divs:
    h_left_div = scholarship_div.find('div', {'class': 'h-left'})
    if h_left_div:
        a_tag = h_left_div.find('a')
        if a_tag:
            name = a_tag.text.strip()
            link = a_tag['href']
            deadline = scholarship_div.find('p', {'class': 'pull-left deadline'}).find('b').text.strip()
            study_level = scholarship_div.find('h6', string='Study Level').find_next_sibling('p').text.strip()
            print(name)
            print(link)
            print(deadline)
            print(study_level)
