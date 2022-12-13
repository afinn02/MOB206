import sqlite3
import os
import json
import requests
import numpy as np
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression

def createConnection(filename):
    dir = os.path.dirname(__file__) + os.sep
    conn = sqlite3.connect(dir + filename)
    curr = conn.cursor()
    return conn, curr

def joinTables(conn, curr):
    curr.execute("SELECT Cities.name, Obesity.data_value, Movement.walking, Movement.biking FROM Cities JOIN Obesity ON Cities.id = Obesity.city_id JOIN Movement ON Cities.id = Movement.city_id")
    dataLst = curr.fetchall()
    obesityRate = []
    walkingIndex = []
    bikingIndex = []
    cityNames =[]
    for i in range(len(dataLst)):
        if (i != 28):
            obesityRate.append(dataLst[i][1])
            walkingIndex.append(dataLst[i][2])
            bikingIndex.append(dataLst[i][3])
            cityNames.append(dataLst[i][0])
    return walkingIndex, obesityRate, bikingIndex, cityNames

def getCorrelation(var1, var2):
    # getting correlation with walkingRate to Obesity
    # getting correlation with Biking to Obesity
    pearsonsCo = np.corrcoef(var1, var2)
    return pearsonsCo[1][0]

def makeGraph(var1, var2, labelx, labely, color):
    plt.scatter(var1, var2, c= color)
    plt.xlabel(labelx)
    plt.ylabel(labely)
    plt.title(label = f"Graph of {labelx} vs Obesity Rate of 100 US Cities")
    z = np.polyfit(var1, var2, 1)
    p = np.poly1d(z)
    plt.plot(var1,p(var1),c=color)
    plt.show()
    m = z[0]
    b = z[1]
    return f"y = {m}x + {b}"
    

       
def makeDoubleGraph(x1,x2,y):
    plt.title(label="Graph of Bike and Walk Score vs Obesity Rate in 100 US Cities")
    plt.xlabel("Walk/Bike Score")
    plt.ylabel("Obesity Rate")
    plt.scatter(x1, y, c="blue", marker='o')
    plt.scatter(x2, y, c='orange', marker='s')
    z = np.polyfit(x1, y, 1)
    p = np.poly1d(z)
    plt.plot(x1, p(x1))
    q = np.polyfit(x2, y, 1)
    w = np.poly1d(q)
    plt.plot(x2,w(x2))
    plt.legend(['Walk Score', 'Bike Score'], loc = "upper left", fontsize=12)
    plt.show()

def calculationOutput(filename, correlation1, correlation2, line1, line2):
    fh = open(filename, 'w')
    fh.write(f"The correlation coefficient for walkability and decreased obesity rates: {correlation1}\n")
    fh.write(f"Line of best fit: {line1}\n")
    fh.write(f"The correlation coefficient for bike-ability and decreased obesity rates: {correlation2}\n")
    fh.write(f"Line of best fit: {line2}\n")
    fh.close()


def main():
    conn, curr = createConnection("sqliteMove.db")
    walk, ob, bike, cityNames = joinTables(conn, curr)
    coefWalkability = getCorrelation(walk, ob)
    coefBike = getCorrelation(bike, ob)
    eq1 = makeGraph(walk, ob, "City Walkability", "Obesity Rates", "red")
    
    eq2 = makeGraph(bike, ob, "City Bike-ablilty", "Obesity Rates", "green")
   
    makeDoubleGraph(walk, bike, ob)

    #write calculations to file
    calculationOutput("AdventureTime.txt", coefWalkability, coefBike, eq1, eq2)
    print(coefWalkability, coefBike)
    print(eq1, eq2)


if __name__ == "__main__":
    main()






