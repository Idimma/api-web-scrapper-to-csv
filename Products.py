
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
import csv


# In[ ]:


import requests
import pandas as pd
from time import sleep


# In[ ]:


brand = ' '
# header =['BRANDS', 'PRODUCT TITLE', 'PRODUCT GROUP', 'PRODUCT CODE',
#          'PRICE', 'PRODUCT IMAGE','PRODUCT', 'DESCRIPTION']
# with open('products_list.csv', 'w', newline='', encoding='utf-8') as csvfile:
#     writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     writer.writerow(header)


# In[ ]:


df = pd.read_csv("products_array.csv",  encoding = "utf-8")


# In[ ]:


def get_response(brand, page):
    url = "https://www.omnical.co/en/json/productresults"
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"page\"\r\n\r\n"+str(page)+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"q\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"autoclass\"\r\n\r\nfalse\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"postData\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"f_brand\"\r\n\r\n"+brand+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"getImages\"\r\n\r\ntrue\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'Cache-Control': "no-cache",
        'Postman-Token': "fd232235-7b6f-486b-a63c-d8e6b8572e0b"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    return response.json()

def get_total(resp):
    return resp[total]

def get_bs(resp):
    divs = BeautifulSoup(resp, 'html.parser')   
    return divs


# In[ ]:


def write_to_file(view):
    with open(r'products_list.csv', 'a', newline='') as f:
        global brand
        writer = csv.writer(f)        
        views  = view.findAll('div', attrs={'class':'tradeproduct product-row'})
        for i, vw in zip(range(len(views)), views):            
            product =  vw.find('div', attrs={'class':'tradeproduct-title'}).text    
            prod = product
            desc = vw.find('div', attrs={'class':'tradeproduct-generated-description-search'}).text            
            if len(product.split(" ")) >= 4:
                product_title = product.split(" ")[3]
                product_group = product.split(" ")[1]
                product_code = product.split(" ")[2]
            else:
                product_title = product
                product_group = product
                product_code = product            
            price = vw.find('span', 
                            attrs={'itemprop':'pricecurrency'}).text +" " + vw.find('span', 
                                                                                    attrs={'itemprop':'price'}).text
            product_detail_image = vw.find('img')['src']
            writer.writerow([brand, product_title, product_group, product_code, price,
                             product_detail_image, prod, desc])


# In[ ]:


def start(b_rand = -1, page = -1):
    global brand
    
    for index, value in df.iterrows():
        if index >  b_rand:
            brand = value['brand']
            print('Started '+ brand)
            html = get_response(brand, 1)
            maxi = html['numProducts']        
            for x in range(1 , maxi+1): 
                if x > page and page != 20:
                    resp = get_response(brand, x)            
                    print('Writing Page '+ str(x) + ' of ' +  str(maxi))
                    write_to_file(get_bs(resp['productView']))
            print('Done with ' + brand)
    


# In[ ]:


start(-1, -1) #START FROM THE VERY BEGINNING 


# In[ ]:




