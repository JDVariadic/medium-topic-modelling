import requests
from bs4 import BeautifulSoup
import pandas as pd

tags = ['covid19', 'coronavirus', 'pandemic', 'covid-19-crisis', 'quarantine']
years = ['2020']
months = ['03', '04']
days = []
for i in range(1, 32):
    if len(str(i)) > 1:
        days.append(str(i))
    else:
        days.append(str(0) + str(i))
link_data = []

def retrieve_urls():
    for tag in tags:
        for year in years:
            for month in months:
                for day in days:
                    URL = 'https://medium.com/tag/'+tag+'/archive/'+year+'/'+month+'/'+day
                    
                    page = requests.get(URL)
                    soup = BeautifulSoup(page.content, 'lxml')
                
                    article_containers = [article for article in soup.find_all('div', class_='cardChromeless')]
                    
                    for article in article_containers:
                        read_more_section = article.find('a', class_='button')
                        try:
                            title = article.find('h3').contents[0]
                            post_id = read_more_section.attrs['data-post-id']
                            link = read_more_section.attrs['href']
                            
                            link_data.append({'post_id': post_id,
                                            'tag': tag,
                                            'day': day,
                                            'month': month,
                                            'year': year,
                                            'article_title': title,
                                            'link': link
                                            })
                        except:
                            continue
                    
        
    df = pd.DataFrame(link_data)
    df.to_csv('medium_links.csv')
    

    
retrieve_urls()

# Link Format: https://medium.com/tag/covid-19-crisis/archive/2020/03/06
# 'https://medium.com/tag/'+tag+'/archive/'+year+'/'+month+'/'+day