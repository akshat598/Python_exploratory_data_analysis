#!/usr/bin/env python
# coding: utf-8

# Api call from website coinmarketcap.com

# In[171]:


#code to call the api from coinmarketcap.com
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'15',
  'convert':'IND'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '5d97b4e5-781a-48e4-8ff9-6bdef101d49d',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)


# In[28]:


type(data)


# In[38]:


import pandas as pd

pd.set_option('display.max_columns',None)#this allows us to see all the columns


# In[39]:


pd.json_normalize(data['status'])


# In[41]:


df = pd.json_normalize(data['data'])
df['timestamp'] = pd.to_datetime('now')
df


# data cleaning and transformation

# In[45]:


df.isnull()


# In[172]:


df.dropna(axis=1,inplace=True)
pd.set_option('display.float_format', lambda x: '%.5f' % x)#changing the foemat of display of market value
df


# In[139]:


#sorting the cryptocurrencies by the market value cap
df_sorted = df.sort_values(by='quote.IND.market_cap', ascending=False)
#finding out the top 5 cryptocurrencies
df2 = df_sorted.head(5).drop(df_sorted[df_sorted['name'] == 'Others'].index)
df2


# DATA VISUALISATION

# In[81]:


import seaborn as sns
import matplotlib.pyplot as plt


# Bar plot representing the value of top 5 crytpo currencies of india
# 

# In[145]:


plt.figure(figsize=(10, 6))
plt.bar(df2['name'],df_topten['quote.IND.price'])
plt.ylabel('Price (INR)')
plt.xlabel('Names')
plt.title('Cryptocurrency Prices')
plt.gca().invert_yaxis() 


# Distribution of cryptocurrency market in india using pie chart
# 

# In[155]:


plt.figure(figsize=(8, 6))

plt.pie(df2['quote.IND.market_cap_dominance'],labels=df2['name'],autopct='%1.1f%%',shadow=False,startangle=140)


# In[167]:


df3 = df2.groupby('name', sort=False)[['quote.IND.percent_change_24h','quote.IND.percent_change_7d','quote.IND.percent_change_30d','quote.IND.percent_change_60d','quote.IND.percent_change_90d']].mean()
df3


# In[168]:


df4 = df3.stack()
df4


# In[174]:


#changes the stack back to the dataframe
df5 = df4.to_frame(name='values')
# Set the above DataFrame index object as the index
# using set_index() function
df6 = df5.reset_index()
#renaming the level 1 column to percentage change
df7 = df6.rename(columns={'level_1': 'percent_change'})
#renaming all the other columns for better visibility in the pie graph
df7['percent_change'] = df7['percent_change'].replace(['quote.IND.percent_change_24h','quote.IND.percent_change_7d','quote.IND.percent_change_30d','quote.IND.percent_change_60d','quote.IND.percent_change_90d'],['24h','7d','30d','60d','90d'])


# Depiction of change of price of various crytpocurrencies through the time

# In[176]:


sns.catplot(x='percent_change', y='values', hue='name', data=df7, kind='point')


# In[ ]:




