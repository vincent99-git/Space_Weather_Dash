import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import sqlite3
import ipdb
from datetime import datetime as dt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

conn = sqlite3.connect("space.db", isolation_level=None)
cur = conn.cursor()

# cur.execute("SELECT strftime('%Y',date) AS yr, strftime('%m',date) AS mo, sum(sunspot_count) AS cnt FROM sunspots WHERE yr >= 1950 GROUP BY yr, mo;")
# df_ss = pd.DataFrame(columns = ["Date", "Sunspot_count", "Sunspot_sd", "Observ_No"])
#  
#  
# sunspots = cur.fetchall()
# df_ss = df_ss.append([pd.Series(row[1:], index = df_ss.columns) for row in sunspots])

cur.execute("SELECT * FROM sunspots WHERE CAST(strftime('%Y', date) AS INTEGER) > 1900")
df_ss = pd.DataFrame(columns = ["Date", "Sunspot_count", "Sunspot_sd", "Observ_No"])
 
 
sunspots = cur.fetchall()
df_ss = df_ss.append([pd.Series(row[1:], index = df_ss.columns) for row in sunspots])

# cur.execute("SELECT station, date_time, lat, long, bf FROM geo_mag WHERE strftime('%M:%S',date_time)='00:00' AND bf != 99999 AND bf != 88888")
cur.execute("SELECT station, strftime('%H',date_time) AS hour, avg(lat), avg(long), max(bf)-min(bf) AS bf_range FROM geo_mag WHERE bf != 99999 AND bf != 88888 GROUP BY station, hour")
df_gm = pd.DataFrame(columns = ["Station","Time", "Lat", "Long", "Bf"])

geo_mag = cur.fetchall()

df_gm = df_gm.append([pd.Series(row, index = df_gm.columns) for row in geo_mag])

df_gm['Log_Bf'] = np.log(df_gm['Bf']) 


cur.execute("SELECT * FROM mag")
df_mg = pd.DataFrame(columns = ["Datetime", "Bx", "By", "Bz", "Bt"])


mag = cur.fetchall()

df_mg = df_mg.append([pd.Series(row[1:], index = df_mg.columns) for row in mag])

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [40, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig1 = go.Figure()
 
fig1.add_trace(
    go.Scatter(
        x=df_mg.Datetime,
        y=df_mg.Bx,
        name="Bx"
    ))
 
fig1.add_trace(
    go.Scatter(
        x=df_mg.Datetime,
        y=df_mg.By,
        name="By"
    ))

fig1.add_trace(
    go.Scatter(
        x=df_mg.Datetime,
        y=df_mg.Bz,
        name="Bz"
    ))

fig1.add_trace(
    go.Scatter(
        x=df_mg.Datetime,
        y=df_mg.Bt,
        name="Bt"
    ))

fig1.update_layout(
    height=200,
    margin=dict(t=10, b=10, l=20, r=20)
)

cur.execute("SELECT * FROM plasma")
df_pl = pd.DataFrame(columns = ["Datetime", "density", "speed", "temp"])


plasma = cur.fetchall()

df_pl = df_pl.append([pd.Series(row[1:], index = df_pl.columns) for row in plasma])

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_pl.Datetime,
    y=df_pl.density,
    name="D"
))

fig.add_trace(go.Scatter(
    x=df_pl.Datetime,
    y=df_pl.speed,
    name="S",
    yaxis="y2"
))

fig.add_trace(go.Scatter(
    x=df_pl.Datetime,
    y=df_pl.temp,
    name="T",
    yaxis="y3"
))

# Create axis objects
fig.update_layout(
  
    yaxis=dict(
        tickfont=dict(
            color="#1f77b4"
        ),
        side="left"
    ),
    yaxis2=dict(
        tickfont=dict(
            color="#ff7f0e"
        ),
        anchor="free",
        overlaying="y",
        side="left",
        position=0.3
    ),
    yaxis3=dict(
        tickfont=dict(
            color="#d62728"
        ),
        anchor="x",
        overlaying="y",
        side="right"
    )
)

# Update layout properties
fig.update_layout(
#     title_text="multiple y-axes example",
    height=200,
    margin=dict(t=10, b=10, l=20, r=20)
)

fig4 = fig

# fig1 = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
# fig2 = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])



fig2 = go.Figure(data=[go.Scatter(x=df_ss.Date, y=df_ss.Sunspot_count)])

fig2.update_layout(
    height=380,
    margin=dict(t=20, b=20, l=20, r=20)
)

fig2.update_layout(
  
    yaxis=dict(
        title="# of Sunspots (raw count)",
#         titlefont=dict(
#             color="#1f77b4"
#         ),
#         tickfont=dict(
#             color="#1f77b4"
#         ),
        side="right"
    )
)

fig2.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(count=5,
                     label="5y",
                     step="year",
                     stepmode="backward"),
                dict(count=10,
                     label="10y",
                     step="year",
                     stepmode="backward"),
                dict(count=20,
                     label="20y",
                     step="year",
                     stepmode="backward"),
                dict(count=50,
                     label="50y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")


import plotly.express as px

# fig3 = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
#                         color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig3 = px.scatter_mapbox(df_gm, lat="Lat", lon="Long", hover_name="Station", hover_data=["Time","Bf"], color="Log_Bf", 
                  color_continuous_scale=px.colors.sequential.Viridis, zoom = 0.65, center=dict(lat=17.41, lon=9.33), height=780)
fig3.update_layout(mapbox_style="open-street-map")
fig3.update_layout(margin=dict(t=20, b=20, l=20, r=20))
# fig.update_layout(legend=dict(
#     yanchor="top",
#     y=0.99,
#     xanchor="left",
#     x=0.01
# ))

# ipdb.set_trace()

# app.layout = html.Div(children=[
#     html.H4(children='Space Weather Dashboard'),
#     
#     html.Div([
#         html.Div([
#             html.H6('Sunspot Count'),
#             dcc.Graph(id='sunspots', figure=fig2),
#             
#             html.H6('Solar Wind Magnetic Field and Plasma'),
#             dcc.Graph(id='mag', figure=fig1),
#             dcc.Graph(id='plasma', figure=fig4)
#         ], className="six columns"),
# 
#         html.Div([
#             html.H6('Earth Magnetic Field Map'),
#             dcc.Slider(
#                 id='time-slider',
#                 min=0,
#                 max=len(df_gm.Time.unique())-1,
#                 value=0,
#                 marks={int(i):(str(j)+":00") for i,j in zip(range(len(df_gm.Time.unique())), df_gm.Time.unique())}
#             ),
#             dcc.Graph(id='geo_mag_map', figure=fig3)   
#         ], className="six columns pretty_container"),
#     ], className="row")
# ])
# 
# 
@app.callback(
    Output('geo_mag_map', 'figure'),
    [Input('time-slider', 'value')])
def update_figure(selected_time):
#     ipdb.set_trace()
       
    actual_selected_time={int(i):str(j) for i,j in zip(range(len(df_gm.Time.unique())), df_gm.Time.unique())}[selected_time]
     
    filtered_df = df_gm[df_gm.Time == actual_selected_time]
 
#     fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp", 
#                      size="pop", color="continent", hover_name="country", 
#                      log_x=True, size_max=55)
# 
#     fig.update_layout(transition_duration=500)
 
    fig_new = px.scatter_mapbox(filtered_df, lat="Lat", lon="Long", hover_name="Station", hover_data=["Time","Bf"], color="Log_Bf", 
                      color_continuous_scale=px.colors.sequential.Viridis, zoom = 0.65, center=dict(lat=17.41, lon=9.33), height=780)
    fig_new.update_layout(mapbox_style="open-street-map")
    fig_new.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
 
    return fig_new

app.layout = html.Div([
    html.Div([html.H3(children='Space Weather Dashboard')], id="title"),
    
    html.Div([
        html.Div([
            html.H6('Sunspot Count'),
            dcc.Graph(id='sunspots', figure=fig2),
        ], className="row pretty_container"),
                    
        html.Div([     
            html.H6('Solar Wind Magnetic Field and Plasma'),
            dcc.Graph(id='mag', figure=fig1),
            dcc.Graph(id='plasma', figure=fig4)
        ], className="row pretty_container"),
    ], className="six columns"),
    
    html.Div([
        html.H6('Earth Magnetic Field Map'),
        dcc.Slider(
            id='time-slider',
            min=0,
            max=len(df_gm.Time.unique())-1,
            value=0,
            marks={int(i):(str(j)+":00") for i,j in zip(range(len(df_gm.Time.unique())), df_gm.Time.unique())}
        ),
        dcc.Graph(id='geo_mag_map', figure=fig3)   
    ], className="six columns pretty_container")
])

if __name__ == '__main__':
    app.run_server(debug=True)