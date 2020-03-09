from bs4 import BeautifulSoup;
import requests;

agent = {"User-Agent":"Mozilla/5.0"}
res = requests.get("https://www.zomato.com/bangalore/south-bangalore-restaurants", headers = agent)
soup = BeautifulSoup(res.text, 'html.parser')

print(soup.prettify)