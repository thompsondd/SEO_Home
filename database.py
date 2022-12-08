import os
from deta import Deta
from dotenv import load_dotenv
import pandas as pd
import numpy as np

load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")


deta = Deta(DETA_KEY)

db = deta.Base("rec_apartments")

"""def insert_apartments(names,addresses,areas,rates,utilities):
    
    return db.put({"key":names, "addresses":addresses, "areas":areas, "rates":rates, "utilities": utilities})"""
def insert_apartments(names,districts,wards,addresses,areas,bedrooms,wc,rates,schools,markets,entertainment,hospitals,restaurants,buses,atm):
    
    return db.put({"key":names, "districts":districts, "wards":wards, "addresses":addresses, "areas":areas, "bedrooms":bedrooms, "wc":wc,
                   "rates":rates, "schools":schools, "markets":markets, "entertainment":entertainment, "hospitals":hospitals, "restaurants":restaurants,
                   "buses":buses, "atm":atm})
                   

def insert_all(names,districts,wards,addresses,areas,bedrooms,wc,rates,schools,markets,entertainment,hospitals,restaurants,buses,atm):
    for (name,district,ward,address,area,bedroom,w,rate,school,market,entertain,hospital,restaurant,bus,at) in zip (names,districts,wards,addresses,areas,bedrooms,wc,rates,schools,markets,entertainment,hospitals,restaurants,buses,atm):
        insert_apartments(name,district,ward,address,area,bedroom,w,rate,school,market,entertain,hospital,restaurant,bus,at)

def fetch_all_apartments():
    
    res = db.fetch()
    return res.items

def get_apartments(apartment):
    
    return db.get(apartment)

df = pd.read_csv('Database.csv')
df = np.array(df)

#
names = list(df[:,0])
districts = list(df[:,1])
wards = list(df[:,2])
addresses = list(df[:,3])
areas = list(df[:,4])
bedrooms = list(df[:,5])
wc = list(df[:,6])
rates = list(df[:,7])
schools = list(df[:,8])
markets = list(df[:,9])
entertainment = list(df[:,10])
hospitals = list(df[:,11]) 
restaurants = list(df[:,12])
buses = list(df[:,13]) 
atm = list(df[:,14])

#
insert_all(names,districts,wards,addresses,areas,bedrooms,wc,rates,schools,markets,entertainment,hospitals,restaurants,buses,atm)