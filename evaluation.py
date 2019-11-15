import string 
import os
import math
import numpy as np

from geopy import distance
# https://pypi.org/project/geopy/

# 返回单位为m
def GNSSdistance( c1, c2 ):
    # long1 = c1[0]
    # lat1 = c1[1]
    # long2 = c2[0]
    # lat2 = c2[1]
	# # Convert the latitudes and longitudes from degree to radians. 
    # lat1 = (math.pi) *(lat1)/ 180
    # long1 = (math.pi) *(long1)/ 180
    # lat2 = (math.pi) *(lat2)/ 180
    # long2 = (math.pi) *(long2)/ 180

	# # Haversine Formula 
    # dlong = long2 - long1
    # dlat = lat2 - lat1

    # ans =  (math.sin(dlat / 2))**2 +  math.cos(lat1) *  math.cos(lat2) *  (math.sin(dlong / 2))**2
    # ans = 2 *  math.asin( math.sqrt(ans))

	# # Radius of Earth in Kilometers, R = 6371 Use R = 3956 for miles 
    # R = 6371

	# # Calculate the result 
    # ans = ans * R

    # return (ans*1000)
    return distance.distance(c1, c2).meters



query = "Dusk1"
database = "Afternoon1-GPS"

queryGPS = os.path.join(query, "GPS.txt")
databaseGPS = os.path.join(database, "GPSNew.txt")
databaseOverlap = os.path.join(query, "Overlap.txt")


qCoordinate = []
fq = open(queryGPS)
while True:
    line = fq.readline()  
    if line:
        strs = line.split()
        lon = float(strs[0])
        lat = float(strs[1])
        #coordinate = (lon,lat)
        coordinate = [lat,lon]
        qCoordinate.append(coordinate)
    else:
        break
fq.close()
ratioq = len(qCoordinate) / 857

dCoordinate = []
fd = open(databaseGPS)
while True:
    line = fd.readline()  
    if line:
        strs = line.split()        
        lon = float(strs[0])
        lat = float(strs[1])
        #coordinate = (lon,lat)
        coordinate = [lat,lon]
        dCoordinate.append(coordinate)
    else:
        break
fd.close()
ratiod = len(dCoordinate) / 629

overlap = []
f = open(databaseOverlap)
while True:
    line = f.readline()  
    if line:
        flag = int(line)
        overlap.append(flag)
    else:
        break
f.close()


#ret = 'E:\\PreciseLocalization\\OpenMultiPR\\OpenMultiPR\\result.txt'
#fr = open(ret)

# prediction = np.loadtxt('features_4parts/predictions-a1-a2.txt')
prediction = np.loadtxt('a1-d1-window.txt')
dis = []
#while True:py
    #line = fr.readline()
    # if line:
    #     ii=ii+1        
    #     idx = int(line)
    #     if idx != -1:
    #         idx = int(idx*ratiod)
    #         i = int(ii*ratioq)
    #         distance = GNSSdistance(qCoordinate[i], dCoordinate[idx-1])
    #         dis.append(distance)
    # else:
    #     break

qSeqlat=[]
qSeqlon=[]
dbSeqlat=[]
dbSeqlon=[]
falsePositive = 0
for ii, idx in enumerate(prediction):
    if idx != -1:
        idx = min(int(idx*ratiod), len(dCoordinate)-1)
        i = int(ii*ratioq)
        dist = GNSSdistance(qCoordinate[i], dCoordinate[idx])#-1?
        if dist<50:
            qSeqlat.append(qCoordinate[i][0])
            qSeqlon.append(qCoordinate[i][1])
        # if dist<100:
        #     dbSeqlat.append(dCoordinate[idx][0])
        #     dbSeqlon.append(dCoordinate[idx][1])
        #print(qCoordinate[i], dCoordinate[idx], dist)
        dis.append(dist)   
        if overlap[ii] == 0:
            falsePositive += 1
    #else:



for coor in dCoordinate:
    dbSeqlat.append(coor[0])
    dbSeqlon.append(coor[1])


count = 0
for d in dis:
    if d<50:
        count  = count +1
#print(dis)

print(count,len(dis),count/len(dis),falsePositive/len(dis))

import matplotlib.pyplot as plt

plt.plot(np.asarray(dbSeqlon), np.asarray(dbSeqlat), c = 'r')
plt.scatter(np.asarray(qSeqlon), np.asarray(qSeqlat))

# plt.figure()
# plt.plot(np.asarray(list(range(len(dis)))),np.asarray(dis))
plt.show()