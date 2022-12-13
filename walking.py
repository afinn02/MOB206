import sqlite3
import os
import json
import requests
import time
from bs4 import BeautifulSoup

def setUpBase(sq, file):
    conn = sqlite3.connect(file)
    curr = conn.cursor()
    curr.execute(sq)
    return curr, conn

def getSiteData():
    
    url = "https://www.walkscore.com/cities-and-neighborhoods/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('div', class_ = "list-wrap state-list-wrap stripe-table small-phone")
    info = table.find_all('tr')
    # remove the header information
    info.pop(0)

    dataLst = []
    for i in range(len(info)):
        state = info[i].find('td', class_ = "state").text
        if state[:3] == "CA-":
             continue
        else:

            tDcity = info[i].find('td', class_ = "city")
            city = tDcity.find('a').text
            score = info[i].find('td', class_ = "score").text
            biking = info[i].find('td', class_ = "bsc").text
            
            rowData = (city, state, score, biking)
            
            dataLst.append(rowData)
    return dataLst

def countInsertions(curr, conn, basename):
    curr.execute(f"SELECT * FROM {basename}")
    items = curr.fetchall()
    return len(items)


def insertData(curr, conn, dataLst):
    numItems = countInsertions(curr, conn, "Movement")
    for i in range(len(dataLst)):
        currentItems = countInsertions(curr, conn, "Movement")
        if (currentItems <= numItems + 24):
            city = dataLst[i][0]
            state = dataLst[i][1]
            score = dataLst[i][2]
            biking = dataLst[i][3]


            curr.execute('INSERT OR IGNORE INTO Cities (id, name) VALUES (?, ?)',(i,city))

            curr.execute('INSERT OR IGNORE INTO Movement (city_id, walking, biking) VALUES (?, ?, ?)',(i, score, biking))
            conn.commit()
            
        else:
            break

def main():
    file = "sqliteMove.db"
    curr, conn = setUpBase("CREATE TABLE IF NOT EXISTS Movement (city_id INTEGER PRIMARY KEY, walking REAL, biking REAL)", file)
    curr.execute("CREATE TABLE IF NOT EXISTS Cities (id INTEGER PRIMARY KEY, name TEXT)")
    info = getSiteData()
    insertData(curr, conn, info)
    print("25 Insertions Complete")

# main()

if __name__ == "__main__":
    main()