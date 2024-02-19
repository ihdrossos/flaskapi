import requests

from bs4 import BeautifulSoup

url = "https://www.savoil.gr/"

r = requests.get(url)

print(r)
print(r.content)