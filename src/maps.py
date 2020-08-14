import pandas as pd
import webview
import numpy as np
from threading import Timer
import urllib.request

from flask import Flask,send_from_directory,Response
flaskServer = Flask(__name__)

df = pd.read_csv("./maps_test.csv")
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
    
    //L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        L.tileLayer('./tiles/{s}/{z}/{x}/{y}.png', {

        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

    }).addTo(map);
"""+markers+"""
    </script>    
</body>    
"""
f.write(base)
f.close()


@flaskServer.route('/')
def index():
    print("Base get")
    return base
@flaskServer.route('/leaf/<path:path>')
def leafServe(path):
    return send_from_directory('./iframe_figures/leaf/',path)

@flaskServer.route('/tiles/<string:s>/<string:z>/<string:x>/<string:y>.png')
def tileServe(s,z,x,y):
    print("Tile serve")
    req = urllib.request.Request(
    url="https://"+s+".tile.openstreetmap.org/"+z+"/"+x+"/"+y+".png", 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
    }
    )
    print("https://"+s+".tile.openstreetmap.org/"+z+"/"+x+"/"+y+".png")
    return Response(urllib.request.urlopen(req).read(), mimetype='image/png')
@flaskServer.after_request
def add_header(response):
    response.cache_control.max_age = 86400
    response.cache_control.public=True
    response.cache_control.immutable=True
    return response

# window =webview.create_window('Simulations', url="./iframe_figures/figure_0.html",width=900,height=900)
window =webview.create_window('Simulations', flaskServer,width=900,height=900)
def evaluate_js(window):
    result = window.evaluate_js(
        r"""
        "Latitude,Longitude\n"+Object.values(map._layers).filter(a=>!!a._latlng).map(a=>Object.values(a._latlng).join()).join("\n")
        """
    )

    print(result)

# def autoClose():
#     # print("Auto closed")
#     window.destroy()

# r = Timer(5.0, autoClose)
# r.start()

# webview.start(evaluate_js,window,debug=True, http_server=True,gui="qt")
# webview.start(window,debug=True,gui="qt")
# input("a")
if __name__ == '__main__':
    flaskServer.config['PROPAGATE_EXCEPTIONS'] = True
    flaskServer.config['TESTING'] = True
    flaskServer.run(host='0.0.0.0', port=80,debug=True,threaded=False,processes=1)