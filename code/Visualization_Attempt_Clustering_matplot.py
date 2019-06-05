#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os

os.environ['PROJ_LIB'] = r'c:\Users\Khalil Sayid\.conda\pkgs\proj4-4.9.3-hcf24537_7\Library\share'


# In[9]:


import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from itertools import chain
home_x, home_y = d[1011811424][0][2], d[1011811424][0][1]
similar_x = list(chain.from_iterable(d[1011811424][i][2] for i in range(1,4)))
similar_y = list(chain.from_iterable(d[1011811424][i][1] for i in range(1,4)))
'''
plt.scatter(home_x, home_y, label = "User")
plt.scatter(similar_x, similar_y, label = "Similar Users")
plt.scatter(similar_x, similar_y)
plt.legend(loc='upper left')
'''
map = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
        projection='lcc',lat_1=32,lat_2=45,lon_0=-95)

map.readshapefile(r'C:/Users/Khalil Sayid/Desktop/st99_d00', name='states', drawbounds=True)

new_x,new_y = map(home_x,home_y)
map.plot(new_x,new_y,marker='o',color='blue',markersize=5, label = "User")
flag = True
for (x,y) in zip(similar_x, similar_y):
    new_x, new_y = map(x,y)
    if flag:
        map.plot(new_x,new_y,marker='o',color='orange',markersize=5, label = "Similar Users")
        flag = False
        continue
    map.plot(new_x,new_y,marker='o',color='orange',markersize=5)
plt.legend(loc='upper left')
userid = str(1)
filename = "analysis_" + str(userid) + ".png"
plt.savefig(filename)
plt.show()


# In[ ]:


plt.contour


# In[3]:


with open("cluster2.txt", "r") as f:
    d = {}
    errors = []
    for line in f:
        try:
            cleaner = "".join(line.replace("\t\t", ', '))
            cleaner = "".join(line.replace("\t", ', '))
            cleaner = cleaner.replace("..", ".")
            cleaner = eval(cleaner)
            d[cleaner[0]] = cleaner[1]
        except:
            errors.append(line)
            


# In[11]:


with open("sentiment_clusters.txt", "r") as f:
    d = {}
    errors = []
    for line in f:
        square, stats = eval("".join(line.replace("\t", ', ')))
        d[tuple(square)] = stats[0]


# In[12]:


n = 100 #number of partitions
dy = (-65 - (-125)) / n
dx = (50 - 24) / n 
rectangles = {(i,j) : [-125 + dx * i, -125 + dx * (i+1), 24 + dy * j, 24 + dy * (j+1)] for i in range(n) for j in range(n)}


# In[30]:


d2 = {i : d.get(i, 0) for i in rectangles}


# In[31]:


d3 = {tuple(rectangles[i]) : d.get(i,0) for i in d2}


# In[61]:


len(d3)


# In[47]:


f = lambda x :( (x[0] + x[1]) / 2, (x[2] + x[3]) / 2 )


# In[62]:


[map(list(d3.keys()[i]), f) for i in range(len(d3))]


# In[60]:


list(d3.keys())


# In[57]:


list(d3.items())[0]


# In[39]:


[0,1,2][:1]


# In[23]:


n = 100 #number of partitions
dy = (-65 - (-125)) / n
dx = (50 - 24) / n 
rectangles = {(i,j) : [-125 + dx * i, -125 + dx * (i+1), 24 + dy * j, 24 + dy * (j+1)] for i in range(n) for j in range(n)}

