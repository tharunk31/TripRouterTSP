#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import googlemaps
import csv
import gurobipy as gp
from gurobipy import GRB
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# In[2]:


gmaps = googlemaps.Client(key = "AIzaSyD6VnsCMzmSzFi-pB2CuLs138ay_xOnseA")
Locations = []

ImportList = input("Load previously saved csv file location list?\nEnter'Y' for yes and 'N' for no\n")
if (ImportList == 'Y'):
    with open("C:\TV\Locations.csv",newline='') as f:
        reader = csv.reader(f)
        Locations = list(reader)
        
    for i in range(len(Locations)):
        Locations[i] = Locations[i][0]

Entry = input("Enter place to visit:\nEnter 'stop' to stop\nFirst entry is starting location\n")
while (Entry != 'stop'):
    if (Entry not in Locations):
        Locations.append(Entry)
    Entry = input("Enter place to visit:\n Enter 'stop' to stop\n")


# In[3]:


print(Locations)


# In[4]:


RemoveLoc = input("Remove any location? 'Y' for yes and 'N' for no\n")
if RemoveLoc == 'Y':
    LocEntry = input("Enter Location:\n")
    Locations.remove(LocEntry)


# In[5]:


print(Locations)


# In[6]:


ImportedDistanceMatrix = np.genfromtxt("C:\TV\Distance.csv",delimiter=",")
# ImportedDistanceMatrix


# In[7]:


DistanceMatrix = np.zeros((len(Locations),len(Locations)))

if RemoveLoc == 'N':

    for i in range(len(Locations)):
        for j in range(len(Locations)):
            if ((i < len(ImportedDistanceMatrix)) and (j < len(ImportedDistanceMatrix))):
                DistanceMatrix[i][j] = ImportedDistanceMatrix[i][j]
            else:
                TestGeoCode = gmaps.distance_matrix(Locations[i],Locations[j])
                if (i != j):
                    if (TestGeoCode['rows'][0]['elements'][0]['status'] == 'OK'):
                        DistanceMatrix[i][j] = TestGeoCode['rows'][0]['elements'][0]['distance']['value']/1000
                    else:
                        DistanceMatrix[i][j] = np.inf
if RemoveLoc == 'Y':
    
    for i in range(len(Locations)):
        for j in range(len(Locations)):
                TestGeoCode = gmaps.distance_matrix(Locations[i],Locations[j])
                if (i != j):
                    if (TestGeoCode['rows'][0]['elements'][0]['status'] == 'OK'):
                        DistanceMatrix[i][j] = TestGeoCode['rows'][0]['elements'][0]['distance']['value']/1000
                    else:
                        DistanceMatrix[i][j] = np.inf    


# In[8]:


# DistanceMatrix = np.zeros((len(Locations),len(Locations)))

# for i in range(len(Locations)):
#     for j in range(len(Locations)):
#         if (TestGeoCode['rows'][i]['elements'][j]['status'] == 'OK'):
#             DistanceMatrix[i][j] = TestGeoCode['rows'][i]['elements'][j]['distance']['value']/1000
#         else:
#             DistanceMatrix[i][j] = np.inf


for i in range(len(Locations)):
    InfCount = 0
    for j in range(len(Locations)):
        if (DistanceMatrix[i][j] == np.inf):
            InfCount += 1
    if InfCount == len(Locations):
        DistanceMatrix = np.delete(DistanceMatrix, (i), axis=0)
        DistanceMatrix = np.delete(DistanceMatrix, (i), axis=1)
        Locations.pop(i)
    
print(DistanceMatrix)


# In[9]:


print(Locations)


# In[10]:


SaveList = input("Save locations and distances?\nEnter 'Y' for yes 'N' for no\n")

if (SaveList == 'Y'):
    with open("C:\TV\Locations.csv","w",newline='') as f:
        write = csv.writer(f,dialect='excel')
        for i in Locations:
            write.writerow([i])
    print("Location file saved")
    
    np.savetxt("C:\TV\Distance.csv", DistanceMatrix,
              delimiter=",")
    print("Distance file saved")


# In[11]:


model = gp.Model("RouteTSP")

x = model.addVars(len(Locations), len(Locations), name = "X", vtype = GRB.BINARY)

u = model.addVars(len(Locations), name="U", vtype=GRB.INTEGER,lb=1,ub=len(Locations))

RouteDistance = 0

for i in range(len(Locations)):
    for j in range(len(Locations)):
        RouteDistance += DistanceMatrix[i][j] * x[i,j]
        
InFlowConstraints = model.addConstrs(x.sum(i,"*") == 1 for i in range(1,len(Locations)))

OutFlowConstraints = model.addConstrs(x.sum("*",i) == 1 for i in range(1,len(Locations)))

StartFlowConstraint = model.addConstr(x.sum(0,"*") == 1)

EndFlowConstraint = model.addConstr(x.sum("*",0) == 1)

SubTourEliminationConstraints = model.addConstrs(u[i] - u[j] + 1 <= (len(Locations) - 1) * (1 - x[i,j]) for i in range(1,len(Locations)) for j in range(1,len(Locations)))

StayProhibitionConstraints = model.addConstrs(x[i,i] == 0 for i in range(len(Locations)))

model.setObjective(RouteDistance, GRB.MINIMIZE)
model.optimize()

if (model.Status == GRB.OPTIMAL):
    print("\n\n\n*********\nSolution Found\n*********")
    xValue = model.getAttr("X",x)
    obj = model.getObjective()
#     for i in range(len(Locations)):
#         for j in range(len(Locations)):
#             if (xValue[i,j] > 0):
#                 print("We visit",Locations[j], "from",Locations[i])
    print("Order of routing:")
    next = np.zeros(len(Locations))
    Routing = [0]
    for i in range(len(Locations)):
        for j in range(len(Locations)):
            if xValue[i,j] > 0:
                next[i] = j
    current = 0
    while next[current] != 0:
        Routing.append(int(next[current]))
        current = int(next[current])
        
    Routing.append(0)
    print(Routing)
    RouteString = ""
    Count = 0
    for i in Routing:
        if (Count < len(Locations)+1) and (Count > 0):
            RouteString += " -> "
        RouteString += Locations[i]
        Count += 1
    print(RouteString)
    print("The route takes",obj.getValue(),"kilometers.")


# In[12]:


RouteDistance = DistanceMatrix
LocationDict = {i:Locations[i] for i in range(len(Locations))}

for i in range(len(Locations)):
    for j in range(len(Locations)):
        if (xValue[i,j] > 0.1):
            RouteDistance[i][j] *= xValue[i,j]
        else:
            RouteDistance[i][j] *= 0


# In[13]:



G = nx.from_numpy_array(RouteDistance)

G = nx.DiGraph()

for i in range(len(Locations)):
    G.add_node(i)
    for j in range(len(Locations)):
        if (RouteDistance[i][j] != 0):
            G.add_edge(i,j,weight=RouteDistance[i][j])
        
nx.draw_networkx(G,with_labels=True)
handles_dict = {patches.Patch(color='white', label=f"{k}, {v}") for k,v in LocationDict.items()}
plt.legend(handles=handles_dict,loc='right',bbox_to_anchor=(1.75,0.5))
plt.figure(figsize=(8,20))
plt.show()


# In[14]:


Latitudes = np.zeros(len(Locations))
Longitudes = np.zeros(len(Locations))
for i in range(len(Locations)):
    Latitudes[i] = gmaps.geocode(Locations[i])[0]['geometry']['location']['lat']
    Longitudes[i] = gmaps.geocode(Locations[i])[0]['geometry']['location']['lng']


# In[ ]:




