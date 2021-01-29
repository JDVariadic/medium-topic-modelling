import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
tags = ['life', 'self', 'love', 'relationships', 'life-lessons', 'personal-development']
years = ['2019', '2020']
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#tags = ['relationships']
days = []
#years = ['2019']
#months =['05']

for i in range(1, 32):
    if len(str(i)) > 1:
        days.append(str(i))
    else:
        days.append(str(0) + str(i))

links = []
link_data = []
'''
def generate_links():
    print('Generating Links')
    for tag in tags:
        for year in years:
            for month in months:
                for day in days:
                    links.append('https://medium.com/tag/'+tag+'/archive/'+year+'/'+month+'/'+day)
    print('Done Generating')
'''
def generate_links_v2():
    print('Generating Links')
    for tag in tags:
        for year in years:
            for month in months:
                for day in days:
                    links.append({'URL':'https://medium.com/tag/'+tag+'/archive/'+year+'/'+month+'/'+day,
                                  'Tag': tag,
                                  'Year': year,
                                  'Month': month,
                                  'Day': day})
    print('Done Generating')
                    
def retrieve_url_data(link):
    page = requests.get(link['URL'])
    soup = BeautifulSoup(page.content, 'lxml')
    try:
        article_containers = [article for article in soup.find_all('div', class_='cardChromeless')]
        print(len(article_containers))
        for article in article_containers:
            read_more_section = article.find('a', class_='button')
            title = ''
            try:
                title = article.find('h3').contents[0]
            except:
                print('No Title Found')
                
            if title != '':
                post_id = read_more_section.attrs['data-post-id']
                article_link = read_more_section.attrs['href']
                '''
                link_data.append({
                    'post_id': post_id,
                    'article_title': title,
                    'link': link
                })
                '''
                link_data.append({'post_id': post_id,
                                'tag': link['Tag'],
                                'day': link['Day'],
                                'month': link['Month'],
                                'year': link['Year'],
                                'article_title': title,
                                'link': article_link
                                })
    except Exception as e:
        print(e)
        
            
        

    
def main():
    generate_links_v2()
    with ThreadPoolExecutor(max_workers=600) as executor:
        executor.map(retrieve_url_data, links)
        executor.shutdown(wait=True)
    df = pd.DataFrame(link_data)
    df.to_csv('medium_self_links_test.csv')

    
main()

# Link Format: https://medium.com/tag/covid-19-crisis/archive/2020/03/06
# 'https://medium.com/tag/'+tag+'/archive/'+year+'/'+month+'/'+day