from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests

session = HTMLSession()

def get_page(city, type, beds, page):
  
    url = f'https://www.torontorentals.com/{city}/{type}?beds={beds}%20&p={page}'
    
    result = requests.get(url)
    
    # check HTTP response status codes to find if HTTP request has been successfully completed
    if result.status_code >= 100  and result.status_code <= 199:
        print('Informational response')
    if result.status_code >= 200  and result.status_code <= 299:
        print('Successful response')
        soup = BeautifulSoup(result.content, "lxml")
    if result.status_code >= 300  and result.status_code <= 399:
        print('Redirect')
    if result.status_code >= 400  and result.status_code <= 499:
        print('Client error')
    if result.status_code >= 500  and result.status_code <= 599:
        print('Server error')
        
    return soup

soup_page = get_page('toronto', 'condos', '1', 1)
listingStreet = []
    # grab listing street
for tag in soup_page.find_all('div', class_='listing-brief'):
    for tag2 in tag.find_all('span', class_='replace street'):
        # to check if data point is missing
        if not tag2.get_text(strip=True):
            listingStreet.append("empty")
        else:
            listingStreet.append(tag2.get_text(strip=True))

# # URL of the website to be scraped
# url = "https://www.rentboard.ca/london-on"
# url = "https://www.torontorentals.com/toronto/condos?beds=1%20&p=2"

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.49",
# }
# res = requests.get(url, headers=headers)

# soup = BeautifulSoup(res.content, "html.parser")
# # Send a request to the website to fetch the HTML content
# r = session.get(url) 
# r.html.render(timeout=200)
# r.html.html

# soup = BeautifulSoup(r.html.html)

# soup.find_all('div', class_="listing-content")

# r.html.find('title')[0].text

# r.html.find('#listing-content')

# # Find the table containing the rent prices
# table = soup.find("table", attrs={"id": "ctl00_ContentPlaceHolder1_dgRentals"})

# # Extract the data from the table
# rent_prices = []
# for row in table.find_all("tr")[1:]:
#     rent_price = {}
#     columns = row.find_all("td")
#     rent_price["type"] = columns[0].text.strip()
#     rent_price["price"] = columns[1].text.strip()
#     rent_price["beds"] = columns[2].text.strip()
#     rent_price["baths"] = columns[3].text.strip()
#     rent_prices.append(rent_price)

# # Print the rent prices
# for rent_price in rent_prices:
#     print(rent_price)
