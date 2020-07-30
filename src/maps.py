import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("./out.csv")
df.head()

# BBox = ((np.format_float_positional(df.Longitude.min()), np.format_float_positional(df.Longitude.max()),      
#          np.format_float_positional(df.Latitude.min()),  np.format_float_positional(df.Latitude.max())))
# BBox = (174.76557 ,174.78242,-41.28333,-41.29030)
# BBox =(174.76840,174.77690,-41.28903,-41.28461)
BBox =(174.76840,174.77690,-41.28903,-41.28461)

print(BBox)

# http://openstreetmap.org/#map=17/-41.28682/174.77212
ruh_m = plt.imread("./map.png")

fig, ax = plt.subplots(figsize = (8,7))
# fig, ax=plt.subplots()
ax.scatter(df.Longitude, df.Latitude, zorder=1, alpha= 0.2, c='b', s=10)
ax.set_title('Plotting Spatial Data')
ax.set_xlim(BBox[0],BBox[1])
ax.set_ylim(BBox[2],BBox[3])
ax.imshow(ruh_m, zorder=0, extent = BBox)#, aspect= 'equal')
# fig.show(block=True)
plt.show()
# input("idk")