from typing import *
import database as db
import numpy as np

class ToaDo:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __str__(self):
        return str((self.x,self.y))
    def __add__(self,toado):
        return ToaDo(self.x+toado.x,self.y+toado.y)
    def __sub__(self,toado):
        return ToaDo(self.x-toado.x,self.y-toado.y)
    def calDistance(self,todo):
        temp = self - todo
        return np.sqrt(temp.x*temp.x+temp.y*temp.y)
class ProcessData:
    def __init__(self,data:dict):
        self.data = data.copy()
        self.process()
    
    def process(self):
        sum=np.sum(list(self.data["main"].values()))

        for i in list(self.data["main"].keys()):
            self.data["main"][i]=self.data["main"][i]/sum
        self.data["main"]["env_p"]*=0.9
        for sub,dataSub in self.data["sub"].items():
            sum = np.sum(list(dataSub.values()))
            for k in self.data["sub"][sub].keys():
                self.data["sub"][sub][k]=self.data["sub"][sub][k]*self.data["main"][sub]/sum
        order = ['location_p', 'price_p', 'area_p', 'sleep_p',
         'wc_p', 'school_p', 'market_p', 'entertainment_p']
        temp = {}
        for i in order:
            if i in self.data["main"].keys():
                d = self.data["main"][i]
            else:
                for sub in self.data["sub"].keys():
                    if i in self.data["sub"][sub].keys():
                        d = self.data["sub"][sub][i]
                        break
            temp.update({i:d})
        self.data = [self.data.copy(),temp]
class CanHo:
    def __init__(self, info:dict):
        self.info = info
        self.name = info["key"]
        self.toado = ToaDo(info["X"], info["Y"])
        #self.aroundenv = AroundEnv(**{info[i] for i in ["schools","markets","entertainment","hospitals","restaurants","buses","atm"]})
        self.convDataKeys = ["rates","bedrooms","wc","areas"]
        self.NN={"ch":[],"dis":[]}
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

    def scoreIntSet(self,num,set):
        if set[0]<= num <= set[1]:
            return 1
        return 1/np.float_power(min(abs(num-set[0]),abs(num - set[1])),2)
    def score2Set(self,set1,set2):
        a = np.power(set1[0]-set2[0],2)
        b = np.power(set1[1]-set2[1],2)
        return 1/(a+b)

    def setQuan(self, quan:object):
        self.inQuan = quan
    def setPhuong(self, phuong:object):
        self.inPhuong = phuong
    
    def distance(self,canho):
        return self.toado.calDistance(canho.toado)
    
    def getNN(self):
        tempC = []
        tempD = []
        for quanNN in self.inQuan.NN:
            for phuongNN in quanNN.listPhuong.keys():
                for canho in quanNN.listPhuong[phuongNN].listCanHo:
                    tempC.append(canho)
                    tempD.append(self.distance(canho))
        for idx in np.argsort(tempD)[:min(3,len(tempD))]:
            if tempC[idx] in self.NN["ch"]:
                if tempD[idx] < self.NN["dis"][self.NN["ch"].index(tempC[idx])]:
                    self.NN["dis"][self.NN["ch"].index(tempC[idx])]=tempD[idx]
            else:
                self.NN["ch"].append(tempC[idx])
                self.NN["dis"].append(tempD[idx])
        return self.NN["ch"]
    
    def calScore(self,canho,query,weight,dis):
        #{'location_p': 10, 'price_p': 10, 'area_p': 7, 'sleep_p': 8,
        # 'wc_p': 8, 'school_p': 8, 'market_p': 8, 'entertainment_p': 8
        #}
        origin_data,weight = weight
        score = np.array([1/np.exp(dis), # Quan
                          self.score2Set([query["bottom_money"],query["top_money"]],canho.getData("rates")), #
                          self.score2Set(query["area"],canho.getData("areas")),
                          self.scoreIntSet(query["sleep"],canho.getData("bedrooms")),
                          self.scoreIntSet(query["vs"],canho.getData("wc")),
                          canho.getData("schools"),
                          canho.getData("markets"),
                          canho.getData("entertainment"),
                        ])
        weight_ = np.array(list(weight.values()))
        score = np.dot(score.T,weight_)
        s = ["hospitals","restaurants","buses","atm"]
        ss = 0
        for i in s:
            ss+=canho.getData(i)
        return score + origin_data["main"]["env_p"]*0.1*ss/0.9
    
    def getNNScore(self,query,weight, include=1):
        if self.NN["ch"]==[] or self.NN["dis"]==[]:
            self.getNN()
        if include: scoreList={"ch":[self],"score":[self.calScore(self,query,weight,0)]}
        else: scoreList={"ch":[],"score":[]}
        tempC = []
        tempD = []
        for quanNN in self.inQuan.NN:
            for phuongNN in quanNN.listPhuong.keys():
                for canho in quanNN.listPhuong[phuongNN].listCanHo:
                    tempC.append(canho)
                    tempD.append(self.calScore(self,query,weight,self.distance(canho)))
        for idx in np.argsort(tempD)[:min(3,len(tempD))]:
            if tempC[idx] in scoreList["ch"]:
                if tempD[idx] < scoreList["dis"][scoreList["ch"].index(tempC[idx])]:
                    scoreList["score"][scoreList["ch"].index(tempC[idx])]=tempD[idx]
            else:
                scoreList["ch"].append(tempC[idx])
                scoreList["score"].append(tempD[idx])
        return scoreList
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
                        '1' : ['2', '3', '4', '5', '10', 'B??nh Th???nh', 'Ph?? Nhu???n' ], 
                        '2' : ['1', '4', '7', '9', 'B??nh Th???nh'],
                        '3' : ['1', '5' ,'10', 'T??n B??nh', 'Ph?? Nhu???n'],
                        '4' : ['1', '2', '5', '7', '8'],
                        '5' : ['1', '3', '4', '6', '8', '10', '11'], 
                        '6' : ['5', '8', '11', 'T??n Ph??', 'B??nh T??n'],
                        '7' : ['2', '4', '8', 'B??nh Ch??nh', 'Nh?? B??'],
                        '8' : ['4', '5', '6', '7', 'B??nh T??n', 'B??nh Ch??nh'],
                        '9' : ['2'],
                        '10' : ['1', '3', '5', '11', 'T??n B??nh'],
                        '11' : ['5', '6', '10', 'T??n B??nh', 'T??n Ph??'],
                        '12' : ['12', 'B??nh Th???nh', 'G?? V???p', 'T??n B??nh', 'T??n Ph??', 'B??nh T??n'],
                        'H??c M??n' : ['12', 'C??? Chi', 'T??n B??nh', 'G?? V???p','B??nh Ch??nh'],
                        'B??nh Th???nh' : ['1', '2', 'Ph?? Nhu???n', 'G?? V???p'],
                        'G?? V???p' : ['12', 'H??c M??n', 'B??nh Th???nh'],
                        'Ph?? Nhu???n' : ['1', '3', 'B??nh Th???nh', 'G?? V???p', 'T??n B??nh'],
                        'T??n B??nh' : ['3', '10', '11', '12', 'Ph?? Nhu???n', 'G?? V???p', 'T??n Ph??'],
                        'T??n Ph??' : ['6', '11', '12', 'B??nh T??n'],
                        'B??nh T??n' : ['6', '8', '12', 'T??n Ph??'],
                        'Nh?? B??' : ['7' , 'B??nh Ch??nh'],
                        'C??? Chi' : ['H??c M??n'],
                        'B??nh Ch??nh': ['7', '8', 'Nh?? B??', 'H??c M??n'] 
                      }

    def addNewQuan(self, quanName:str):
        if quanName not in list(self.listQuan.keys()):
            self.listQuan[quanName] = Quan(quanName)
    def getQuan(self,quanName:str):
        if quanName not in list(self.listQuan.keys()):
            self.addNewQuan(quanName)
        return self.listQuan[quanName]

    def addNewCanHo(self):
        for data_CanHo in self.data:
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

    def addRecommend(self,canho,q,w, include=1):
        listR = canho.getNNScore(q,w,include)
        for ich in listR["ch"]:
            if ich in self.recommend_list["ch"]:
                a = self.recommend_list["score"][self.recommend_list["ch"].index(ich)]
                b = listR["score"][listR["ch"].index(ich)]
                if b>a:
                    self.recommend_list["score"][self.recommend_list["ch"].index(ich)] = b
            else:
                self.recommend_list["ch"].append(ich)
                self.recommend_list["score"].append(listR["score"][listR["ch"].index(ich)])
        accept = np.argsort(self.recommend_list["score"])
        accept = [accept[i] for i in range(len(accept)-1,-1,-1)]
        newReL = {"ch":[],"score":[]}
        for index in accept[:min(len(accept),self.n_re)]:
            newReL["ch"].append(self.recommend_list["ch"][index])
            newReL["score"].append(self.recommend_list["score"][index])
        self.recommend_list = newReL
    
    def search(self, requirments):
        keys = list(requirments.keys())
        query = {key:requirments[key] for key in keys if key!="priority"}
        priority = ProcessData(requirments["priority"])
        self.n_re = 10
        list_canho ={}
        self.recommend_list ={"ch":[],"score":[]}
        for quan in query["quan"]:
            quan_obj = self.listQuan.get(quan,None)
            if quan_obj==None:
                continue
            list_canho[quan]=[]
            for phuong_name in quan_obj.listPhuong.keys():
                phuong_obj = quan_obj.listPhuong[phuong_name]

                for canho in phuong_obj.listCanHo:
                    price = canho.getData("rates")

                    if query["bottom_money"]>price[0] or query["top_money"]<price[1]:
                        self.addRecommend(canho,query,priority.data)
                        continue

                    areas = canho.getData("areas")
                    if query["area"][0]>areas[0] or query["area"][1]<areas[1]:
                        self.addRecommend(canho,query,priority.data)
                        continue

                    wc = canho.getData("wc")
                    if query["vs"]<wc[0] or query["vs"]>wc[1]:
                        self.addRecommend(canho,query,priority.data)
                        continue

                    bedrooms = canho.getData("bedrooms")
                    if query["sleep"]<bedrooms[0] or query["sleep"]>bedrooms[1]:
                        self.addRecommend(canho,query,priority.data)
                        continue
                    self.addRecommend(canho,query,priority.data,0)
                    list_canho[quan].append(canho.info)
        return list_canho,[i.info for i in self.recommend_list["ch"]]

class Connect_Backend():
    def __init__(self):
        self.data = db.fetch_all_apartments()
        self.Manager = Manage(self.data)
        self.Manager.addNewCanHo()
    def Update_Database(self):
        self.data = db.fetch_all_apartments()
        self.Manager = Manage(self.data)
        self.Manager.addNewCanHo()