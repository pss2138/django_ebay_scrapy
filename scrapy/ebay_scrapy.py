# import modules for analysis
from ebaysdk.finding import Connection as finding
from bs4 import BeautifulSoup
import requests
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import datetime as dt

# import modules for data visualization
from sqlalchemy import create_engine
import io
import base64, urllib

# import modules for django
from django.conf import settings
from .models import Related

# link the data with database
user = settings.DATABASES['default']['USER']
password = settings.DATABASES['default']['PASSWORD']
database_name = settings.DATABASES['default']['NAME']
host = settings.DATABASES['default']['HOST']
port = settings.DATABASES['default']['PORT']

database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
    user=user,
    password=password,
    database_name=database_name,
)

engine = create_engine(database_url, echo=False)



def my_appid():
    YOURAPPID = 'YOUR EBAY DEVELOPER APP ID'
    return YOURAPPID


def get_keywords(YOURAPPID, text):
    api = finding(domain='svcs.ebay.com', debug=False, appid=YOURAPPID, config_file=None)
    api_request = {'keywords': text, 'outputSelector': 'SellerInfo'}

    response = api.execute('findItemsByKeywords', api_request)
    soup = BeautifulSoup(response.content, 'lxml')

    totalentries = str(int(soup.find('totalentries').text))
    items = soup.find_all('item')

    title = []
    data = []
    for item in items:
        item_info = []
        name = item.title.string.lower().strip()
        title = title + name.split(" ")
        category = item.categoryname.string.lower()
        cat_id = item.categoryid.string.lower()
        price = int(round(float(item.currentprice.string)))
        shippingcost = item.shippingservicecost
        if shippingcost is None:
            shippingcost = 0.0
        else:
            shippingcost = float(shippingcost.string.encode('utf-8'))
        starttime = item.starttime.string
        endtime = item.endtime.string
        url = item.viewurl
        if url is None:
            url = " "
        else:
            url = url.string
        
        item_info.extend((name, category, price, shippingcost, starttime, endtime, url))
        data.append(item_info)


    df_keyword = pd.DataFrame(data, columns=['title', 'category', 'price', 'shippingcost', 'starttime', 'endtime', 'url'])
    df_keyword['starttime'] = df_keyword['starttime'].apply(pd.to_datetime).dt.normalize()
    df_keyword['endtime'] = df_keyword['endtime'].apply(pd.to_datetime).dt.normalize()
    df_keyword['duration'] = (df_keyword['endtime'] - df_keyword['starttime']).dt.days

    # push dataframe by to_sql and to_html, plus touching views.py and keyword.html
    df_keyword.to_sql("results_table", engine, if_exists='append', index=False)
    
    recommendation = tuple(Counter(title).most_common(10))
    df_recommendation = pd.DataFrame(recommendation, columns=['keyword', 'counts'])
    df_recommendation.to_sql("table_recommendation", engine, if_exists='append', index=False)
    table_recommendation = df_recommendation.to_html()
    
    df_shippingcost = df_keyword['shippingcost'].value_counts(sort=True).rename_axis('cost').reset_index(name='counts')
    df_shippingcost.to_sql("table_shippingcost", engine, if_exists='append', index=False)
    table_shippingcost = df_shippingcost.to_html()
    
    table_keyword = df_keyword.to_html()

    return cat_id, table_keyword, df_keyword, table_recommendation, totalentries, table_shippingcost



def analyzing(df_keyword):

    df_category = df_keyword['category'].value_counts(normalize=True, sort=True).rename_axis('category').reset_index(name='counts')
    df_category.to_sql("table_category", engine, if_exists='append', index=False)
    table_category = df_category.to_html()

    df_price = df_keyword['price'].quantile([0, 0.25, 0.5, 0.75, 1]).rename_axis('percentage').reset_index(name='price')
    df_price.to_sql("table_price", engine, if_exists='append', index=False)
    table_price = df_price.to_html()

    df_duration = df_keyword['duration'].quantile([0, 0.25, 0.5, 0.75, 1]).rename_axis('percentage').reset_index(name='duration')
    df_duration.to_sql("table_duration", engine, if_exists='append', index=False)
    table_duration = df_duration.to_html()

    # draw graph visualization
    fig = plt.figure(figsize=(10,10))

    plt.subplot(2,2,1)
    cat_pie = df_keyword['category'].value_counts()
    cat_pie.plot(kind='pie', cmap=plt.cm.Pastel1, autopct='%.1f%%', labels=None)
    plt.title('Category Distribution')
    plt.legend(labels=cat_pie.index, loc="upper right", bbox_to_anchor=(1, 1))
    plt.ylabel('')
    
    plt.subplot(2,2,2)
    plt.title('Price Distribution ($)')
    df_keyword['price'].plot(kind='box', showfliers=False, labels=None)

    plt.subplot(2,2,3)
    df_keyword['starttime'].hist(bins=30, color='lightgreen')
    plt.title('Start Time Distribution (%)')
    plt.xticks(rotation=45)

    plt.subplot(2,2,4)
    df_keyword['duration'].hist(bins=30)
    plt.title('Duration (% / days)')
   

    fig.tight_layout()
    #convert graph into dtring buffer and then we convert 64 bit code into image    
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    graph =  urllib.parse.quote(string)
   
    
    return table_category, table_price, table_duration, graph



def get_related_items(YOURAPPID, cat_id):

    related_url = ('http://svcs.ebay.com/MerchandisingService?OPERATION-NAME=getMostWatchedItems&SERVICE-NAME=MerchandisingService&SERVICE-VERSION=1.1.0&CONSUMER-ID=' +
            YOURAPPID + '&RESPONSE-DATA-FORMAT=XML&REST-PAYLOAD&maxResults=20&categoryId=' + cat_id)
    related_url = related_url.replace(" ", "%20")
    api_result = requests.get(related_url)
    parsed_doc = BeautifulSoup(api_result.content, 'lxml')
    items = parsed_doc.find_all('item')
    
    data = []
    for item in items:
        item_info = []
        title = item.title.string.strip()
        category = item.primarycategoryname.string.lower()
        price = int(round(float(item.buyitnowprice.string)))
        shippingcost = int(float(item.shippingcost.string))
        url = item.viewurl
        if url is None:
            url = " "
        else:
            url = url.string
        watchcount = item.watchcount.string

        item_info.extend(
            (title, category, price, shippingcost, url, watchcount))
        data.append(item_info)

        #save the data into Related model
        item_obj = Related(title=title, category=category, price=price, shippingcost=shippingcost, url=url, watchcount=watchcount)
        item_obj.save()


    df_related = pd.DataFrame(data, columns=['title', 'category', 'price', 'shippingcost', 'url', 'watchcount']) 
    df_related.to_sql("related_table", engine, if_exists='append', index=False)
    table_related = df_related.to_html()

    return table_related

            
# main function to start analysis
def scrapy(text):
    YOURAPPID = my_appid()
    cat_id, table_keyword, df_keyword, table_recommendation, totalentries, table_shippingcost = get_keywords(YOURAPPID, text)
    table_category, table_price, table_duration, graph = analyzing(df_keyword)
    table_related = get_related_items(YOURAPPID, cat_id)
    return table_recommendation, totalentries, table_shippingcost, table_category, table_price, table_duration, table_keyword, table_related, graph
