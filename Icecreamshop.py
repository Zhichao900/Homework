#!/usr/bin/env python
# coding: utf-8

# In[5]:


from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import time
import random


# In[24]:


Rank=[]
Name=[]
Rate=[]
Reviews=[]
Phone =[]
Address=[]
District=[]

number = 0
while number < 91:
    url = 'https://www.yelp.com/search?find_desc=ice%20cream%20shops&find_loc=10023&start='+str(number)
    ourUrl=urllib.request.urlopen(url)
    soup=BeautifulSoup(ourUrl,'html.parser')
    
    for i in soup.find_all('div',class_="lemon--div__373c0__1mboc largerScrollablePhotos__373c0__3FEIJ arrange__373c0__UHqhV border-color--default__373c0__2oFDT"):  
        #extract ranking
        pre_rank = i.find('p',class_='lemon--p__373c0__3Qnnj text__373c0__2pB8f text-color--black-regular__373c0__38bRH text-align--left__373c0__2pnx_ text-size--inherit__373c0__2gFQ3').text
        pre_rank=str(pre_rank).split(".",1) #split rank and name
        rank=pre_rank[0]
        
        if rank.isnumeric():
            #extract name
            name=i.find('a').text.encode('utf-8')


            #extract rate
            rate = str(i.find('span',class_='lemon--span__373c0__3997G display--inline__373c0__1DbOG border-color--default__373c0__2oFDT'))
            if rate[107:110] == 'div':
                pre_rate = i.find('span',class_='lemon--span__373c0__3997G display--inline__373c0__1DbOG border-color--default__373c0__2oFDT').find('div')
                pre_rate=str(pre_rate)
                rate= pre_rate[17:20]
                rate= rate.replace('s','')
            else:
                rate='No rating information'

            #extract Number of reviews
            if rate =='No rating information':
                reviews = 'No Information'
            else:
                reviews = i.find('span',class_='lemon--span__373c0__3997G text__373c0__2pB8f reviewCount__373c0__2r4xT text-color--mid__373c0__3G312 text-align--left__373c0__2pnx_').text

            #extract phone number, Address, and District
            ContactInfo = i.find_all('p',class_='lemon--p__373c0__3Qnnj text__373c0__2pB8f text-color--normal__373c0__K_MKN text-align--right__373c0__3ARv7')
            list=[]
            for k in ContactInfo:
                list.append(k.text)

            if len(list)==3:    #In case of missing value among three attributes
                phone=list[0]
                address = list[1]
                district = list[2]
            else:
                if len(list[0])==14:
                    phone = list[0]
                    address = list[1]
                    district = 'No Information'
                else:
                    phone = 'No information'
                    address = list[0]
                    district = list[1]
            

            print(rank)
            print(name.decode('utf-8'))
            print(rate)
            print(reviews)
            print(phone)
            print(address)
            print(district)
            Rank.append(rank)
            Name.append(name.decode('utf-8'))  # append name
            Rate.append(rate)
            Reviews.append(reviews)
            Phone.append(phone)
            Address.append(address)
            District.append(district)

    if len(Rank)-number > 5: #Check if the number is continuous, or the webite denied access
        number = number + 10
        time.sleep(2+3*random.random())
    else:
        print('Reconnecting')
        time.sleep(2+3*random.random())
    


# In[25]:


dataframe = pd.DataFrame({'Rank':Rank,'Name':Name,'Rate':Rate,'Reviews Number':Reviews,'Phone Number':Phone, 'Address':Address,'District':District})
dataframe.to_csv("icecreamshop.csv",index=False,sep=',')


# In[26]:


df = pd.read_csv("icecreamshop.csv", encoding='utf-8')


# In[27]:


df


# In[28]:



number_of_shop=df.District.value_counts()   
xticks = []
yticks = []
for i in number_of_shop.keys():
    xticks.append(i)
    value=number_of_shop[i]
    yticks.append(value)

print(xticks,yticks)


# In[31]:


import matplotlib.pyplot as plt
fig = plt.figure()
plt.bar(xticks, yticks,0.8, align='center')
plt.xticks(rotation=90)
plt.xlabel('District')
plt.ylabel('Number of shops')

plt.show()


# In[30]:


max = len(df)
Avg = []
for item in xticks:
    count = 0
    total = 0
    for i in range(0,max):
        if df['District'][i] == item:
            if df['Rate'][i][0].isnumeric():
                count+=1
                total = total + float(df['Rate'][i])
    if count == 0: # in case of division by zero
        count = 1
    avg = total/count
    Avg.append(round(avg,2))
print(Avg)


# In[151]:


plt.bar(xticks, Avg,0.8, align='center')
plt.xticks(rotation=90)
plt.xlabel('District')
plt.ylabel('Number of shops')

plt.show()


# In[ ]:




