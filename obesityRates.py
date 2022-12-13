import sqlite3
import os
import json
import requests
import time
from bs4 import BeautifulSoup
import walking


def getCities():
    dir = os.path.dirname(__file__) + os.sep
    conn = sqlite3.connect(dir + 'sqliteMove.db')
    curr = conn.cursor()

    curr.execute("SELECT Cities.name FROM Cities")
    cityList = curr.fetchall()
    return cityList

def fetchAPI(cityList):
    base = "https://chronicdata.cdc.gov/resource/bjvu-3y7d.json"
    
    temp = []
    for city in cityList:
        vars = {'year':'2017', 'cityname': city[0]}
        r = requests.get(base, params=vars)
        j = json.loads(r.text)
        
        if (len(j) > 0):
            c = j[0].get("cityname", None)
            d = j[0].get("data_value", None)
    
            tup = (c, d)
            temp.append(tup)
            
    return temp


def insertObData(curr, conn, dataLst):
    numItems = walking.countInsertions(curr, conn, "Obesity")
    for i in range(len(dataLst)):
        currentItems = walking.countInsertions(curr, conn, "Obesity")
        if (currentItems <= numItems + 24):
            # select from the other table we made and set the id as the first value
            c = dataLst[i][0]
            d = dataLst[i][1]

            # statement = f"SELECT Cities.id FROM Cities WHERE Cities.name = {c}"
            curr.execute("SELECT Cities.id FROM Cities WHERE Cities.name = ?", (c,))
            idnum = curr.fetchone()[0]
            curr.execute('INSERT OR IGNORE INTO Obesity (city_id, data_value) VALUES (?, ?)',(idnum, d))
            conn.commit()
            
        else:
            break 

def main():
    file = "sqliteMove.db"
    walkingInfo = getCities()
    curr, conn = walking.setUpBase("CREATE TABLE IF NOT EXISTS Obesity (city_id INTEGER PRIMARY KEY, data_value REAL NOT NULL)", file)
    data = fetchAPI(walkingInfo)
    insertObData(curr, conn, data)
    print("25 insertions complete")

if __name__ == "__main__":
    main()



