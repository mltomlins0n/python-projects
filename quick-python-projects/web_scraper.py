import requests
from bs4 import BeautifulSoup as bs # web scraping library

github_user = input('Input Github username to find: ')
url = 'https://github.com/'+github_user
r = requests.get(url)
soup = bs(r.content, 'html.parser')
profile_img = soup.find('img', {'class' : 'avatar avatar-user width-full border color-bg-primary'})['src']
print('Profile image: ' + profile_img)