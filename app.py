import requests
from bs4 import BeautifulSoup
import pandas as pd

url="https://www.amazon.in/s?k=skincare&rh=p_72%3A1318479031&dc&crid=HET2HKBZALSW&qid=1709397904&rnid=1318475031&sprefix=skincare%2Caps%2C370&ref=sr_nr_p_72_4&ds=v1%3AdOJQt7PLHJq%2BWTp2s9XQBXVQq%2BOsvQXE7d%2BIe7dCOlM"

headers=({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
          'Accept-Language':'en-US, en;q=0.5'})

def get_response(url,headers):
    response=requests.get(url,headers=headers)
    if response.status_code == 200:
        
        return response
    else:
        
        assert response.status_code == 200, "Failed to fetch the webpage. Status Code: {}".format(response.status_code)
response=get_response(url,headers)

soup=BeautifulSoup(response.content,'html.parser')

links=soup.find_all('a',attrs={'class':"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal" })
name=[]
cost=[]
manufacturer=[]
for i in range(2):
    link=links[i].get('href')
    product_link='https://www.amazon.in'+link

    product=get_response(product_link,headers=headers)

    soup1=BeautifulSoup(product.content,'html.parser')
    title=soup1.find('span',attrs={'id':'productTitle'}).text.strip()
    name.append(title)
    price=soup1.find('span',attrs={'class':'a-price-whole'}).text.strip()
    cost.append((price))   
    table=soup1.find('table',attrs={'id':"productDetails_detailBullets_sections1"})
    man=table.find_all('td',attrs={'class':'a-size-base prodDetAttrValue'})
    man=man[0]
    manufacturer.append(man.text.strip())
    


data={
    "product name":name,
    "cost":cost,
    "manufacturer":manufacturer
}
df=pd.DataFrame(data)
print(df)