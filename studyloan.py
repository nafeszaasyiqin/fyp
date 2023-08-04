import requests
from bs4 import BeautifulSoup

# Send a GET request to the webpage
url = 'https://example.com'
response = requests.get(url)

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the unordered list and get its text content
ul_tag = soup.find('ul')
if ul_tag:
    list_items = ul_tag.find_all('li')
    for item in list_items:
        print(item.get_text().strip())
else:
    print('No unordered list found on the webpage.')
