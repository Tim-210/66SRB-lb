#!/usr/bin/env python
# coding: utf-8

# In[3]:



from abc import ABC, abstractmethod
import pandas as pd

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
    my_lng = 120.162974
    my_lat = 23.063961
    def __init__(self, target , category):
        self.target = target  # 目標場所
        self.category = category  # 類別

class Toilet(Search):
    def __init__(self, target , category):
        super().__init__(target , category)
        self.data = pd.read_csv(f'{target}_{category}.csv')
        self.distence = [heversine(self.my_lng,self.my_lat,lng,lat) 
                         for lng,lat in zip(self.data['Longitude'],self.data['Latitude']) ]
        self.data['distence'] = self.distence
        self.data['distence'] = self.data['distence'].apply(lambda x : round(x))
    def nearbytarget_info(self,i):
        target = self.data.iloc[self.data['distence'].sort_values().index[i-1:i]] # 取第i近的target資料
        distence = target['distence'].values[0]
        Type = target['Type'].values[0]
        Type2 = target['Type2'].values[0]
        Address = target['Address'].values[0]
        return f'距離{distence}公尺,{Type},{Type2},{Address}'
    def nearbytarget_lng(self,i):
        target = self.data.iloc[self.data['distence'].sort_values().index[i-1:i]]
        lng = target['Longitude'].values[0]
        return lng
    def nearbytarget_lat(self,i):
        target = self.data.iloc[self.data['distence'].sort_values().index[i-1:i]]
        lat = target['Latitude'].values[0]
        return lat
    def nearbytarget_address(self,i):
        target = self.data.iloc[self.data['distence'].sort_values().index[i-1:i]]
        address = target['Address'].values[0]
        return address

class AED(Search):
    def __init__(self, target , category):
        super().__init__(target , category)
        self.data = pd.read_csv(f'{target}.csv')
        self.distence = [heversine(self.my_lng,self.my_lat,lng,lat) 
                         for lng,lat in zip(self.data['地點LNG'],self.data['地點LAT']) ]
        self.data['distence'] = self.distence
        self.data['distence'] = self.data['distence'].apply(lambda x : round(x))
    def nearbytarget_info(self,i):
        target = self.data.iloc[self.data['distence'].sort_values().index[i-1:i]] # 取第i近的target資料
        distence = target['distence'].values[0]
        Name = target['場所名稱'].values[0]
        Logcation = target['AED放置地點'].values[0]
        Phone = target['開放時間緊急連絡電話'].values[0]
        return f'距離{distence}公尺,場所名稱{Name},放置地點{Logcation},聯絡電話{Phone}'
    def nearbytarget_lng(self,i):
        target = self.data.iloc[self.data['distence'].sort_values().index[i-1:i]]
        lng = target['地點LNG'].values[0]
        return lng
    def nearbytarget_lat(self,i):
        target = self.data.iloc[self.data['distence'].sort_values().index[i-1:i]]
        lat = target['地點LAT'].values[0]
        return lat
    def nearbytarget_address(self,i):
        target = self.data.iloc[self.data['distence'].sort_values().index[i-1:i]]
        address = target['場所名稱'].values[0]
        return address

class Charger(Search):
    def __init__(self, target , category):
        super().__init__(target , category)
        self.data = pd.read_csv(f'{target}.csv')
        self.distence = [heversine(self.my_lng,self.my_lat,lng,lat) 
                         for lng,lat in zip(self.data['經度'],self.data['緯度']) ]
        self.data['distence'] = self.distence
        self.data['distence'] = self.data['distence'].apply(lambda x : round(x))
    def nearbytarget_info(self,i):
        target = self.data.iloc[self.data['distence'].sort_values().index[i-1:i]] # 取第i近的target資料
        distence = target['distence'].values[0]
        CA = target['主管機關'].values[0]
        Name = target['充電站名稱'].values[0]
        add = target['地址'].values[0]
        return f'距離{distence}公尺,場所名稱{Name},主管機關{CA},地址 {add}'
    def nearbytarget_lng(self,i):
        target = self.data.iloc[self.data['distence'].sort_values().index[i-1:i]]
        lng = target['經度'].values[0]
        return lng
    def nearbytarget_lat(self,i):
        target = self.data.iloc[self.data['distence'].sort_values().index[i-1:i]]
        lat = target['緯度'].values[0]
        return lat
    def nearbytarget_address(self,i):
        target = self.data.iloc[self.data['distence'].sort_values().index[i-1:i]]
        address = target['地址'].values[0]
        return address

class T_bike(Search):
    def __init__(self, target , category):
        super().__init__(target , category)
        self.data = pd.read_csv(f'{target}.csv')
        self.distence = [heversine(self.my_lng,self.my_lat,lng,lat) 
                         for lng,lat in zip(self.data['Longitude'],self.data['Latitude']) ]
        self.data['distence'] = self.distence
        self.data['distence'] = self.data['distence'].apply(lambda x : round(x))
    def nearbytarget_info(self,i):
        target = self.data.iloc[self.data['distence'].sort_values().index[i-1:i]] # 取第i近的target資料
        distence = target['distence'].values[0]
        StationName = target['StationName'].values[0]
        add = target['Address'].values[0]
        return f'距離{distence}公尺,場所名稱{StationName},地址 {add}'
    def nearbytarget_lng(self,i):
        target = self.data.iloc[self.data['distence'].sort_values().index[i-1:i]]
        lng = target['Longitude'].values[0]
        return lng
    def nearbytarget_lat(self,i):
        target = self.data.iloc[self.data['distence'].sort_values().index[i-1:i]]
        lat = target['Latitude'].values[0]
        return lat
    def nearbytarget_address(self,i):
        target = self.data.iloc[self.data['distence'].sort_values().index[i-1:i]]
        address = target['Address'].values[0]
        return address