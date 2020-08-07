import plotly.graph_objects as go
import plotly as plotly
import pandas as pd
import webview
import numpy as np
from threading import Timer

df = pd.read_csv("./out.csv")
df.head()

f = open("./iframe_figures/figure_0.html", "w")

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5LWRvY3MiLCJhIjoiY2s1MnNtODFwMDE4YjNscG5oYWNydXFxYSJ9.AquTxb6AI-oo7TWt01YQ9Q"

markers=""

for index, row in df.iterrows():
    markers+="L.marker([{lat},{long}]).addTo(map);".format(long=row["Longitude"],lat=row["Latitude"])
    
base="""
<link rel="stylesheet" href="./leaf/leaflet.css" />
<script src="./leaf/leaflet.js"></script>
<body style="margin:0px;">
    <div id="mapid" style="width: 100%;height: 100%;"></div>
    <script>
        var map = L.map('mapid').setView([""" +np.format_float_positional(df.Latitude.min())+","+np.format_float_positional(df.Longitude.min())+ """], 17);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

"""+markers+"""
    </script>    
</body>    
"""
f.write(base)
f.close()

window =webview.create_window('Simulations', url="./iframe_figures/figure_0.html",width=900,height=900)
def evaluate_js(window):
    result = window.evaluate_js(
        r"""
        "Latitude,Longitude\n"+Object.values(map._layers).filter(a=>!!a._latlng).map(a=>Object.values(a._latlng).join()).join("\n")
        """
    )

    print(result)

def autoClose():
    # print("Auto closed")
    window.destroy()

r = Timer(5.0, autoClose)
r.start()

webview.start(evaluate_js,window,debug=True, http_server=True,gui="qt")

