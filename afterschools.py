import requests
from bs4 import BeautifulSoup

url = 'https://afterschool.my/scholarship'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
head_div = soup.find('div', {'class': 'head'})

num_scholarships_label = head_div.find('label')
if num_scholarships_label:
    num_scholarships = num_scholarships_label.text.split()[-2]
else:
    num_scholarships = 'Unknown'

sorting_options_div = head_div.find('div', {'class': 'sort'})
sorting_options = sorting_options_div.find_all('a')
sort_by = []
for option in sorting_options:
    sort_by.append(option.text.strip())

print("Number of scholarships shown:", num_scholarships)
print("Sorting options:", sort_by)
