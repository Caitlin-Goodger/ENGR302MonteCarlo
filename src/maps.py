import plotly.graph_objects as go
import plotly as plotly
import pandas as pd
import webview
import os
import matplotlib.pyplot as plt

df = pd.read_csv("./out.csv")
df.head()

# open(".mapbox_token").read()
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5LWRvY3MiLCJhIjoiY2s1MnNtODFwMDE4YjNscG5oYWNydXFxYSJ9.AquTxb6AI-oo7TWt01YQ9Q"

fig = go.Figure(go.Scattermapbox(
    lat=df.Latitude,
    lon=df.Longitude,
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=9
    ),
    # text=["Sim 1"],
))

fig.update_layout(
    autosize=False,
    hovermode='closest',
    width=800,
    height=800,
    margin=go.layout.Margin(
        l=0,
        r=0,
        b=0,
        t=0,
        pad = 0
    ),
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=df.Latitude.mean(),
            lon=df.Longitude.mean()
        ),
        pitch=0,
        zoom=17
    ),
)

# https://plotly.com/python/renderers/#setting-the-default-renderer
fig.show(renderer="iframe")
# conda install -c plotly plotly-orca
# print(fig.show(renderer="png"))
# fig.show()
f = os.path.isfile('./iframe_figures/figure_0.html')
print (f)
if not f:
    x = df.Longitude
    y = df.Latitude
    colors = (0,0,0)
    area = np.pi*3

    # Plot
    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    plt.title('Scatter plot pythonspot.com')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
if f:
    ht = open("./iframe_figures/figure_0.html", "r")
    webview.create_window('Simulations', html=ht.read(),width=840,height=860)
    webview.start()
    ht.close()
