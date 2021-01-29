import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
text_data = []
def scrape_text(df):
    text_data = []
    for i, j in df.iterrows():
        print(i)
        URL = j['link'] 
        try:
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'lxml').text
            text_data.append(soup)
        except Exception as e:
            print(e)
            text_data.append('')
            continue
        
    df['text_data'] = text_data
    df.to_csv('medium_final_data.csv')
        
    
def scrape_text_individual(url, idx):
    print(idx)
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml').text
        text_data.append(soup)
    except Exception as e:
        print(e)
        text_data.append('')
    
def main():
    df = pd.read_csv('medium_self_links_test.csv')
    with ThreadPoolExecutor(max_workers=500) as executor:
        executor.map(scrape_text_individual, [link for link in df.link], [idx for idx in df.index])
        executor.shutdown(wait=True)
    df['text_data'] = text_data
    df.to_csv('medium_final_data_multithreading.csv')

#df = pd.read_csv('medium_links.csv')
#scrape_text(df)

main()