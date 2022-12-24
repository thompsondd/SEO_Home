import os
from deta import Deta
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import streamlit as st
#
load_dotenv(".env")
DETA_KEY = st.secrets["DETA_KEY"]

deta = Deta(DETA_KEY)

db = deta.Base("rec_apartments")

#insert
def insert_apartments(names,links,districts,wards,addresses,areas,bedrooms,wc,rates,schools,markets,entertainment,hospitals,restaurants,buses,atm,X,Y):
    
    return db.put({"key":names, "links":links, "districts":districts, "wards":wards, "addresses":addresses, "areas":areas, "bedrooms":bedrooms, "wc":wc,
                   "rates":rates, "schools":schools, "markets":markets, "entertainment":entertainment, "hospitals":hospitals, "restaurants":restaurants,
                   "buses":buses, "atm":atm, "X":X, "Y":Y})
                   
#insert all
def insert_all(names,links,districts,wards,addresses,areas,bedrooms,wc,rates,schools,markets,entertainment,hospitals,restaurants,buses,atm,X,Y):
    for (name,link,district,ward,address,area,bedroom,w,rate,school,market,entertain,hospital,restaurant,bus,at,x,y) in zip (names,links,districts,wards,addresses,areas,bedrooms,wc,rates,schools,markets,entertainment,hospitals,restaurants,buses,atm,X,Y):
        insert_apartments(name,link,district,ward,address,area,bedroom,w,rate,school,market,entertain,hospital,restaurant,bus,at,x,y)

#fetch all apartments from database
def fetch_all_apartments():
    
    res = db.fetch()
    return res.items

#get an apartment from database
def get_apartments(apartment):
    
    return db.get(apartment)

#delete an apartment from database
def delete_apartments(apartment):
    
    return db.delete(apartment)

#Pre-processing data
df = pd.read_csv('Database.csv')

df = np.array(df)
#
names = list(df[:,0])
links = list(df[:,1])
districts = list(df[:,2])
wards = list(df[:,3])
addresses = list(df[:,4])
areas = list(df[:,5])
bedrooms = list(df[:,6])
wc = list(df[:,7])
rates = list(df[:,8])
schools = list(df[:,9])
markets = list(df[:,10])
entertainment = list(df[:,11])
hospitals = list(df[:,12]) 
restaurants = list(df[:,13])
buses = list(df[:,14]) 
atm = list(df[:,15])
X = list(df[:,16])
Y = list(df[:,17])

#
insert_all(names,links,districts,wards,addresses,areas,bedrooms,wc,rates,schools,markets,entertainment,hospitals,restaurants,buses,atm,X,Y)