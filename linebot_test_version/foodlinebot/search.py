#!/usr/bin/env python
# coding: utf-8

# In[3]:


from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import pandas as pd
import requests
import folium
import geopandas as gpd
import matplotlib.pyplot as plt
from math import radians , cos , sin , asin , sqrt
 
def heversine(lng1,lat1,lng2,lat2):
    # 將10進位制轉為弧度
    lng1 , lat1 , lng2 , lat2 = map(radians , [lng1,lat1,lng2,lat2])
    d_lng = lng2 - lng1
    d_lat = lat2 - lat1
    a = sin(d_lat/2)**2 + cos(lat1) * cos(lat2) * sin(d_lng/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # 地球半徑
    return c*r*1000

class Search(ABC):
 
    def __init__(self, target , category):
        self.target = target  # 目標場所
        self.category = category  # 類別
 
#     @abstractmethod
#     def scrape(self):
#         pass
    @abstractmethod
    def Toilet(self):
        pass
 
 
# 愛食記爬蟲
# class IFoodie(Food):
 
#     def scrape(self):
#         response = requests.get(
#             "https://ifoodie.tw/explore/" + self.area +
#             "/list?sortby=popular&opening=true")
 
#         soup = BeautifulSoup(response.content, "html.parser")
 
#         # 爬取前五筆餐廳卡片資料
#         cards = soup.find_all(
#             'div', {'class': 'jsx-1776651079 restaurant-info'}, limit=5)
 
#         content = ""
#         for card in cards:
 
#             title = card.find(  # 餐廳名稱
#                 "a", {"class": "jsx-1776651079 title-text"}).getText()
 
#             stars = card.find(  # 餐廳評價
#                 "div", {"class": "jsx-1207467136 text"}).getText()
 
#             address = card.find(  # 餐廳地址
#                 "div", {"class": "jsx-1776651079 address-row"}).getText()
 
 
             #將取得的餐廳名稱、評價及地址連結一起，並且指派給content變數
#             content += f"{title} \n{stars}顆星 \n{address} \n\n"
 
#         return content


class Toilet():
    def __init__(self, target , category):
        self.target = target  # 目標場所
        self.category = category  # 類別
    
    def nearby_target(self):
        
        my_lng,my_lat = 120.162974 , 23.063961 # 預設中心為中信金融管理學院 ， 之後會根據定位
        
        data = pd.read_csv(f'{self.target}_{self.category}.csv') # target data
        # 計算距離
        distence = []
        for lng,lat in zip(data['Longitude'],data['Latitude']):
            distence.append(heversine(my_lng,my_lat,lng,lat))
        data['distence'] = distence
        data['distence'] = data['distence'].apply(lambda x : round(x))
        content = ''
        nearby = data.iloc[data['distence'].sort_values().index[:5]] # 取距離最近的n個，預設5
        nearby = nearby[['distence','Type','Type2','Address']]
        for i in range(len(nearby)):
            content += f'距離{nearby.iloc[i,0]}公尺,{nearby.iloc[i,1]},{nearby.iloc[i,2]},{nearby.iloc[i,3]}\n\n'
            
        return content
