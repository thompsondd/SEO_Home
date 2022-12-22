from typing import *
import database as db
from tqdm import tqdm
import numpy as np

class ProcessData:
    def __init__(self,data:dict):
        self.data = data.copy()
        self.process()
        
    def process(self):
        sum=np.sum(list(self.data.values()))
        for i in list(self.data.keys()):
            self.data[i]=self.data[i]/sum

class CanHo:
    def __init__(self, info:dict):
        self.info = info
        self.name = info["key"]
        self.toado = (info["X"], info["Y"])
        self.convDataKeys = ["rates","bedrooms","wc","areas"]
        self.convertData()

    def __eq__(self, __o: object) -> bool:
        return self.name==__o.name

    def convertData(self):
        self.convertedData={}
        for i in self.convDataKeys:
            d = self.info[i].strip(" ")
            if "-" in d:
                self.convertedData[i] = list(map(float,d.split("-")))
            else:
                self.convertedData[i] = (float(d),float(d))

    def getData(self,keys):
        if keys not in self.convDataKeys:
            return self.info[keys]
        return self.convertedData[keys]

    def __str__(self):
        return self.name

    def setQuan(self, quan:object):
        self.inQuan = quan
    def setPhuong(self, phuong:object):
        self.inPhuong = phuong

    def distance(self,toadoA, toadoB):
        a = np.array(toadoA).astype(np.float64)
        b = np.array(toadoB).astype(np.float64)
        c=a-b
        return np.sqrt(c[0]*c[0]+c[1]*c[1])
    def getNN(self):
        self.NN={"ch":[],"dis":[]}
        tempC = []
        tempD = []
        for quanNN in self.inQuan.NN:
            for phuongNN in quanNN.listPhuong.keys():
                for canho in quanNN.listPhuong[phuongNN].listCanHo:
                    tempC.append(canho)
                    tempD.append(self.distance(self.toado, canho.toado))
        for idx in np.argsort(tempD)[:min(3,len(tempD))]:
            if tempC[idx] in self.NN["ch"]:
                if tempD[idx] < self.NN["dis"][self.NN["ch"].index(tempC[idx])]:
                    self.NN.update({tempC[idx]:tempD[idx]})
            else:
                self.NN["ch"].append(tempC[idx])
                self.NN["dis"].append(tempD[idx])
        return self.NN["ch"]
    def getScore(self,query,weight):
        pass
class Phuong:
    def __init__(self,name:str):
        self.name=name
        self.listCanHo=[]

    def setQuan(self, quan:object):
        self.inQuan = quan
    def addNewCanHo(self,CanHo:CanHo):
        self.listCanHo.append(CanHo)
class Quan:
    def __init__(self,name:str):
        self.name=name
        self.listPhuong={}
        self.NN = []

    def addNewPhuong(self, phuongName:str):
        if phuongName not in list(self.listPhuong.keys()):
            self.listPhuong[phuongName] = Phuong(phuongName)

    def getPhuong(self,phuongName:str):
        if phuongName not in list(self.listPhuong.keys()):
            self.addNewPhuong(phuongName)
        return self.listPhuong[phuongName]

class Manage:
    def __init__(self, infoCanHo:dict):
        self.listQuan={}
        self.data = infoCanHo
        self.infoNN = {
            '1' : ['2', '3', '4', '5', '10', 'Bình Thạnh', 'Phú Nhuận' ], 
            '2' : ['1', '4', '7', '9', 'Bình Thạnh'],
            '3' : ['1', '5' ,'10', 'Tân Bình', 'Phú Nhuận'],
            '4' : ['1', '2', '5', '7', '8'],
            '5' : ['1', '3', '4', '6', '8', '10', '11'], 
            '6' : ['5', '8', '11', 'Tân Phú', 'Bình Tân'],
            '7' : ['2', '4', '8', 'Bình Chánh', 'Nhà Bè'],
            '8' : ['4', '5', '6', '7', 'Bình Tân', 'Bình Chánh'],
            '9' : ['2'],
            '10' : ['1', '3', '5', '11', 'Tân Bình'],
            '11' : ['5', '6', '10', 'Tân Bình', 'Tân Phú'],
            '12' : ['12', 'Bình Thạnh', 'Gò Vấp', 'Tân Bình', 'Tân Phú', 'Bình Tân'],
            'Hóc Môn' : ['12', 'Củ Chi', 'Tân Bình', 'Gò Vấp','Bình Chánh'],
            'Bình Thạnh' : ['1', '2', 'Phú Nhuận', 'Gò Vấp'],
            'Gò Vấp' : ['12', 'Hóc Môn', 'Bình Thạnh'],
            'Phú Nhuận' : ['1', '3', 'Bình Thạnh', 'Gò Vấp', 'Tân Bình'],
            'Tân Bình' : ['3', '10', '11', '12', 'Phú Nhuận', 'Gò Vấp', 'Tân Phú'],
            'Tân Phú' : ['6', '11', '12', 'Bình Tân'],
            'Bình Tân' : ['6', '8', '12', 'Tân Phú'],
            'Nhà Bè' : ['7' , 'Bình Chánh'],
            'Củ Chi' : ['Hóc Môn'],
            'Bình Chánh': ['7', '8', 'Nhà Bè', 'Hóc Môn'] 
        }

    def addNewQuan(self, quanName:str):
        if quanName not in list(self.listQuan.keys()):
            self.listQuan[quanName] = Quan(quanName)
    def getQuan(self,quanName:str):
        if quanName not in list(self.listQuan.keys()):
            self.addNewQuan(quanName)
        return self.listQuan[quanName]
    def addNewCanHo(self):
        for data_CanHo in tqdm(self.data):
            canHo = CanHo(data_CanHo)
            quan = self.getQuan(data_CanHo["districts"])
            phuong = quan.getPhuong(data_CanHo["wards"])

            canHo.setPhuong(phuong)
            canHo.setQuan(quan)

            phuong.setQuan(quan)
            phuong.addNewCanHo(canHo)

        for i in self.infoNN.keys():
            if i in self.listQuan.keys():
                for j in self.infoNN[i]:
                    if j in self.listQuan.keys():
                        self.listQuan[i].NN.append(self.listQuan[j])
        

    def search(self, requirments):
        keys = list(requirments.keys())
        query = {key:requirments[key] for key in keys if key!="priority"}
        priority = ProcessData(requirments["priority"])
        #Search
        list_canho ={}
        temp = []
        for quan in query["quan"]:
            quan_obj = self.listQuan[quan]
            list_canho[quan]=[]

            for phuong_name in quan_obj.listPhuong.keys():
                phuong_obj = quan_obj.listPhuong[phuong_name]

                for canho in phuong_obj.listCanHo:
                    temp.extend(canho.getNN())
                    price = canho.getData("rates")

                    if query["bottom_money"]>price[0] or query["top_money"]<price[1]:
                        continue

                    areas = canho.getData("areas")
                    if query["area"][0]>areas[0] or query["area"][1]<areas[1]:
                        continue

                    wc = canho.getData("wc")
                    if query["vs"]<wc[0] or query["vs"]>wc[1]:
                        continue

                    bedrooms = canho.getData("bedrooms")
                    if query["sleep"]<bedrooms[0] or query["sleep"]>bedrooms[1]:
                        continue

                    list_canho[quan].append(canho.info)
        #Recommend
        list_canho_re ={}
        
        #print(list_canho)
        return list_canho


data = db.fetch_all_apartments()
#print(f"Căn hộ:\n{data[0]}")
#requirments = {'quan': ['1', '6', '3'], 'top_money': 200, 'bottom_money': 60, 
#               'area': (0, 500), 'sleep': 1, 'vs': 1, 
#               'priority': {'location_p': 10, 'price_p': 10, 'area_p': 7, 'sleep_p': 8,
#                            'wc_p': 8, 'school_p': 8, 'market_p': 8, 'entertainment_p': 8
#                           }
#            }

Manager = Manage(data)
Manager.addNewCanHo()