import requests
from bs4 import BeautifulSoup
import re

url = "https://play.google.com/store/apps/details?id=my.socar.flex"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the elements containing the desired information
title = soup.find("h1", class_=re.compile(r"(?i)AHFaub"))
developer = soup.find("a", class_=re.compile(r"(?i)hrTbp"))
rating = soup.find("div", class_=re.compile(r"(?i)BHMmbe"))
description = soup.find("div", class_=re.compile(r"(?i)DWPxHb"))

# Extract the text from the elements if they are found
title_text = title.text.strip() if title else "N/A"
developer_text = developer.text.strip() if developer else "N/A"
rating_text = rating.text.strip() if rating else "N/A"
description_text = description.text.strip() if description else "N/A"

# Print the extracted information
print("Title:", title_text)
print("Developer:", developer_text)
print("Rating:", rating_text)
print("Description:", description_text)
