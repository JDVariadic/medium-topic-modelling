import requests
from bs4 import BeautifulSoup
import pandas as pd

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
        
    



df = pd.read_csv('medium_links.csv')
scrape_text(df)