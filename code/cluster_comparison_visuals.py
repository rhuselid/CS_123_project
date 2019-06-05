# Installing geopy may be necessary
# sudo pip install geopy
# In order to get the files needed to have the US in the background, please download the 3
# st99_d00 files in the following repository: 
# https://github.com/matplotlib/basemap/tree/master/examples 

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from itertools import chain
import os
# This was necessary on my local laptop. Apparently, it's a bug in the module :(. 
os.environ['PROJ_LIB'] = r'c:\Users\[username]\.conda\pkgs\proj4-4.9.3-hcf24537_7\Library\share'

# Clean the data!
with open("cluster_comparison_final2.txt", "r") as f:
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

# In a sample of 7000 tweets, only 8 were considered to have an error. 
# Given that the point of this project is the analysis of big data, 
# we see that a significant proportion of lines are kept. 
# Thus, we neglect to fix the 0.1% of tweets that have errors. 

# Graph the data! 
for user in d.keys():
  home_x, home_y = d[user][0][2], d[user][0][1]
  similar_x = list(chain.from_iterable(d[user][i][2] for i in range(1,4)))
  similar_y = list(chain.from_iterable(d[user][i][1] for i in range(1,4)))

  map = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
          projection='lcc',lat_1=32,lat_2=45,lon_0=-95)

  #The first parameter is the location of the 3 st99_d00 files. 
  map.readshapefile(r'st99_d00', name='states', drawbounds=True)

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
  userid = str(user)
  filename = "analysis_" + str(user) + ".png"
  plt.savefig(filename)
