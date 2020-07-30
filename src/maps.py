import plotly.graph_objects as go
import plotly as plotly
import pandas as pd
import webview

df = pd.read_csv("./out.csv")
df.head()

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5LWRvY3MiLCJhIjoiY2s1MnNtODFwMDE4YjNscG5oYWNydXFxYSJ9.AquTxb6AI-oo7TWt01YQ9Q"#open(".mapbox_token").read()

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
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=df.Latitude.mean(),
            lon=df.Longitude.mean()
        ),
        pitch=0,
        zoom=10
    ),
)

# https://plotly.com/python/renderers/#setting-the-default-renderer
fig.show(renderer="iframe")
# conda install -c plotly plotly-orca
# print(fig.show(renderer="png"))
# fig.show()

ht = open("./iframe_figures/figure_0.html","r")
webview.create_window('Hello world', html=ht.read())
webview.start()
ht.close()