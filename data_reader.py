import json
import folium
import geopy.distance
from math import cos, sin, radians

class DataReader:
    def __init__(self):
        f_atm = open("data/atms.txt")
        self.atm_info = json.load(f_atm)
        f_off = open("data/offices.txt")
        self.off_info = json.load(f_off)
    
    def getServicesAtm(atm):
        ret = dict()
        for i in atm['services'].keys():
            ret[i] = atm['services'][i]['serviceCapability'] == "SUPPORTED" and atm['services'][i]['serviceActivity'] == "AVAILABLE"
        return ret
    
    
    def getAtmInfo(self, userAddress, distance = 0, allDay = False, wheelchair = False, blind = False, nfcForBankCards = False, qrRead = False, suppurtsUsd = False, suppurtsChargeRub = False, suppurtsEur=False, suppurtsRub=False):
        needs = {"wheelchair": wheelchair, "blind":blind, "nfcForBankCards":nfcForBankCards, "qrRead": qrRead, "supportsUsd":suppurtsUsd, "supportsChargeRub":suppurtsChargeRub, "supportsEur":suppurtsEur, "supportsRub":suppurtsRub}
        ret = []
        for i in self.atm_info["atms"]:
            x, y = float(i['latitude']), float(i['longitude'])
            _allDay = i['allDay'] == "false"
            d = geopy.distance.geodesic([x,y], userAddress).km
            if (distance==0 or d <= distance) and allDay <= _allDay:
                serv = DataReader.getServicesAtm(i)
                skip = False
                for j in needs.keys():
                    if not(needs[j] <= serv[j]):
                        skip = True
                        break
                if skip:
                    continue
                ret.append(folium.Marker(location=[x, y], popup='<p>'+i['address']+f'<\p><form method="post" action="/" enctype = "multipart/form-data"><input type="hidden" value="{x} {y} {userAddress[0]} {userAddress[1]}" name="coords"><input name="check" type="submit" value="Составить маршрут"></form>'))
        return ret
    
    def hoursToSeg(st):
        if st == "выходной":
            return [0,0,0,0]
        return [int(st[0:2]), int(st[3: 5]), int(st[6: 8]), int(st[9:11])]
    
    def daysToSeg(st):
        d = {"пн":0, "вт":1, "ср":2, "чт":3, "пт":4, "сб":5, "вс":6, "перерыв":7}
        if "-" in st:
            return list(range(d[st[0:2]], d[st[3:5]]+1))
        ret = []
        if "," in st:
            for i in range(0, len(st), 3):
                ret.append(d[st[i:i+2]])
            return ret
        if st not in d.keys():
            #print("Error key "+st)
            return []
        return [d[st]]

    def procSchedule(office):
        ret = [dict(), dict()]
        for i in office["openHours"]:
            for j in DataReader.daysToSeg(i["days"]):
                ret[0][j] = DataReader.hoursToSeg(i["hours"])
            if 7 not in ret[0].keys():
                ret[0][7] = []
        for i in office["openHoursIndividual"]:
            for j in DataReader.daysToSeg(i["days"]):
                ret[1][j] = DataReader.hoursToSeg(i["hours"])
            if 7 not in ret[1].keys():
                ret[1][7] = []
        return ret
    
    def checkTime(state, schedule, currentTime):
        return ((schedule[state][currentTime[0]][0] < currentTime[1] or schedule[state][currentTime[0]][0]==currentTime[1] and schedule[state][currentTime[0]][1] <= currentTime[2]) and
          (schedule[state][currentTime[0]][2] > currentTime[1] or schedule[state][currentTime[0]][2]==currentTime[1] and schedule[state][currentTime[0]][3] >= currentTime[2]) 
        #and not (
        #    schedule[state][7] != [] and
        #    schedule[state][7][0] <= currentTime[1] and 
        #    schedule[state][7][1] <= currentTime[2] and
        #    schedule[state][7][2] >= currentTime[1] and
        #    schedule[state][7][3] >= currentTime[2]
        #)
        ) 
    
    def initedSchedule(sch):
        return sorted(list(sch[0].keys())) == list(range(8)) and sorted(list(sch[1].keys())) == list(range(8))

    def getOfficeInfo(self, userAddress, currentTime, distance = 0, userState = 0):
        ret = []
        for i in self.off_info:
            x, y = float(i['latitude']), float(i['longitude'])
            sch = DataReader.procSchedule(i)
            d = geopy.distance.geodesic(userAddress, [x,y]).km
            if (distance == 0 or d <= distance) and DataReader.initedSchedule(sch) and DataReader.checkTime(userState, sch, currentTime):
                ret.append(folium.Marker(location=[x, y], popup = '<p>'+i['address']+f'<\p><form method="post" action="/" enctype = "multipart/form-data"><input type="hidden" value="{x} {y} {userAddress[0]} {userAddress[1]}" name="coords"><input name="check" type="submit" value="Составить маршрут"></form>'))
        return ret