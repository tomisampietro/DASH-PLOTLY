#Seguimiento --> https://www.youtube.com/watch?v=hBSZQBpYi5M&ab_channel=PabloPaniagua

#Coronavirus dashboard
import pandas as pd
import numpy as np
import dash
import requests
from dash import dcc # DCC: Son widgets de la interfaz grafica... Todo lo que son graficos, sliders, menu de dropdown, etc. 
from dash import html # HTML: Son los elementos de estructura HTML. Por ejemplo, titulos, parrafos, etc. 
import plotly.graph_objs as go # Para hacer graficos en PLOTLY. GO: Graph Objects
from dash.dependencies import Input, Output #Permitira hacer selecciones y que el grafico se actualice. 
import dash_auth #Autenticacion: Una capa de seguridad. Para que no entre gente que no queremos que entre a la pagina web.

#1. Get data

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'



#2.Format and templates
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
tickFont = {'size':9, 'color': 'rgb(30,30,30)'}


#2 Function to get data
# def loadData(filename):
#    data = pd.read_csv(url)
#    return data

#Read data and format the data
data = pd.read_csv(url)

#Elimino algunos columnas que no son de interes
data = data.drop(['Lat', 'Long', 'Province/State'], axis=1)
data = data.melt(id_vars = ['Country/Region'], var_name= 'date', value_name='confirmed')

#Formato estandarizado para fechas:
data= data.astype({'date':'datetime64[ns]', 'confirmed':'Int64'}, errors = 'ignore')
data['dateStr'] = data['date'].dt.strftime('%d-%b-%Y') # https://strftime.org/


#3. CPrepare a list of countries
countries = data['Country/Region'].unique()
countries.sort()

#Menu de dropdown
options = [{'label': c, 'value': c} for c in countries]

#4. Create a Dash application LAYOUT
app = dash.Dash()
app.title = 'Coronavirus Dashboard'

#Autenticacion: Una capa de seguridad. Para que no entre gente que no queremos que entre a la pagina web.
USERNAME_PASSWORD_PAIRS = [
    ['tomis', '1234']

]
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)


#En este espacio de HTML hay que meter todos los componentes. 
#Todo va dentro de una lista.
app.layout = html.Div([

    #Header
    html.H1('Coronavirus Dashboard: Casos Confirmados'),
    #Dropdown menu
    html.Div(
        dcc.Dropdown(
            id = 'country_picker',
            options= options,
            value= 'Argentina'
        ),
        style = {'width': '20%'}
    ),
    #Plot
    dcc.Graph(
        id='confirmed_cases',
        config={'displayModeBar': True}
    )

]) # End Layout

# Add callback to support the interactive components (Python decorators):
# Un decorador, extiende la funcionaldiad de una funcion. Empieza con un @

@app.callback(Output(component_id='confirmed_cases', component_property = 'figure'), 
            [Input(component_id='country_picker', component_property='value')])

def update_bar_chart(selected_country):
    filtered_df = data[data['Country/Region'] == selected_country]
    fig = go.Figure(data = [go.Bar(name = 'Confirmados', x= filtered_df['dateStr'], y= filtered_df['confirmed'], marker_color='firebrick')])
    
    fig.update_layout(
                    title= 'Casos confirmados para {}'.format(selected_country),
                    xaxis=dict(tickangle= -90, ticktext = data.dateStr, tickfont = tickFont, type = 'category'))

    return fig


app.run_server(debug=True)

""" CALLBACKS: Cuando modificado algo en una parte, me lo actualice en otra parte. 
Por ejemplo, si selecciono un pais en un menu desplegable, que me muestre los datos de ese pais.
"""
