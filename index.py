from dash import Dash, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from numerize import numerize 
import plotly
import plotly.express as px
from dash import dcc
import plotly.express as px
import math
import plotly.graph_objects as go
from dotenv import load_dotenv
import os

stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP])
server = app.server

TotalCrashes = pd.read_excel('USA_Crashes.xlsx')
TotalCrashes = TotalCrashes.convert_dtypes()
Fatalities = pd.read_excel('GenderTypeUpdated.xlsx')
Fatalities = Fatalities.convert_dtypes()
AgeGroup = pd.read_excel('AgeType_Updated.xlsx')
AgeGroup = AgeGroup.convert_dtypes()
PersonGroup = pd.read_excel('PersonType_Updated.xlsx')
PersonGroup = PersonGroup.dropna()
PersonGroup['PersonKilled'] = PersonGroup['PersonKilled'].astype('int')
US_Crashes = pd.read_excel('US_Crashes_Updated.xlsx')
US_Crashes = US_Crashes.convert_dtypes()

WCrashes = pd.read_excel('WeeklyCrashes_Updated.xlsx')
Weeks = WCrashes.columns
Weeks = Weeks[1:8]
Alcohol = pd.read_excel('Alcohol_CrashesUp.xlsx')
Alcohol['State'] = Alcohol['State'].astype('str')

Years = TotalCrashes['Year'].unique()
Years = [y for y in Years if y>2010]
States = list(TotalCrashes['State'].unique())
States.insert(0,'All')

app.layout = html.Div(
    [
        html.Div([
            html.H1("Data Visualization For Traffic Accidents - USA (2011-2020)")
        ]),
        
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='my_dropdown',
                    multi=False,
                    options=[
                        {"label": x, "value": x}
                        for x in Years
                        ],
                    value=2020,
                    clearable = False,
                    placeholder = 'Select The Year:',
                    #style={'background':'#1f2c56',
                    style={'margin':'10px',
                        'background':'black',
                        'color':'white',
                        'font-weight':'bold',
                        'width':'100%'}
                )                
            ],className="four Columns"),
            
            dbc.Col([
                dcc.Dropdown(id='Selected_value', 
                             placeholder='Please Click the State (On Map) Or Select All...', 
                             #type='text',
                             value='All',
                             options=[
                                 {"label": x, "value": x}
                                 for x in States
                             ],
                             clearable = False,
                             searchable = False,
                             style={'margin':'10px',
                                'background':'black',
                                'color':'white',
                                'font-weight':'bold',
                                'width':'100%'}
                )   
            ],className="eight Columns"),     
        
        ], className='twelve columns'),       
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.H2("Total Crashes"),id='m-header-color'
                    ),
                    dbc.CardBody([
                        html.H1(id='Crash_Card'),
                        html.Div(id='Total_Crashes')
                        ],)
                    ],className="card_container1 text-center")
            ],className="three columns"),                                     

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.H2("Total Fatalities"),id='n-header-color'
                    ),
                    dbc.CardBody([
                        html.H1(id='Fatality_Card'),
                        html.Div(id='Total_Fatalities')
                        ],)
                    ],className="card_container2 text-center")
            ],className="three columns") ,

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.H2("Pedestrian Fatalities"),id='o-header-color'
                    ),
                    dbc.CardBody([
                        html.H1(id='Ped_Card'),
                        html.Div(id='Pedestrian_Crahes')
                        ],)
                    ],className="card_container3 text-center")
            ],className="three columns") ,
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.H2("Alc-Impaired Driving"),id='p-header-color'
                    ),
                    dbc.CardBody([
                        html.H1(id='Alc_Card'),
                        html.Div(id='Alcohol_Crashes')
                        ],)
                    ],className="card_container4 text-center")
            ],className="three columns")            
        ]),
        
        dbc.Row([
           dbc.Col([
               html.Div([
                   dcc.Graph(id='line_chart', config={'displayModeBar': 'hover',
                                                    'scrollZoom': False}, 
                            style={'background':'#00FC87','padding-bottom':'0px','padding-left':'0px','height':'60vh',
                                   'width':'100vh'})
                ]),                             
           ],className="seven columns"),
           
           dbc.Col([
                html.Div([
                    dcc.Graph(id = 'pie_chart', config={'displayModeBar': 'hover',
                                                    'scrollZoom': False}, 
                            style={'background':'#00FC87','padding-bottom':'0px','padding-left':'0px','height':'60vh'})
                ]),
           ],className="five columns")
        ],className='PieMap'),
        
        html.Br(),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(id='bar_chart', config={'displayModeBar': 'hover',
                                                    'scrollZoom': False}, 
                            style={'background':'#00FC87','padding-bottom':'0px','padding-left':'0px','height':'100vh',
                                   })
                ])
            ],className="six columns"),
            
            dbc.Col([

                dcc.RadioItems(
                    id='radio_items',
                    options=[
                        {"label": x, "value": x}
                        for x in Weeks
                        ],
                    value = "Sunday",
                    inline=True,
                    #labelStyle={'display': 'inline-block'},
                    style={'margin':'10px',
                           'background':'black',
                            'color':'white',
                            #'font-weight':'bold',
                            'width':'100%'}
                ),
                
                
                html.Div([
                    dcc.Graph(id='bar_chart1', config={'displayModeBar': 'hover',
                                                    'scrollZoom': False}, 
                            style={'background':'#00FC87','padding-bottom':'0px','padding-left':'0px','height':'100vh'})
                ])
            ],className="six columns")
        ],className='PieMap')
    ]
)

@app.callback(Output('bar_chart1', 'figure'),
              [Input('my_dropdown','value'),
               Input('Selected_value','value'),
               Input('radio_items','value')])
def updatecard(my_dropdown,Selected_value, radio_items):
    if (Selected_value == '' or Selected_value == 'All'):
        Weekly_Crashes = WCrashes[(WCrashes['State']=='USA') & (WCrashes['Year']== my_dropdown) & 
                                  (WCrashes['Timings'] != 'TOTAL')][[radio_items,'Timings']]
    else:
        Weekly_Crashes = WCrashes[(WCrashes['State']== Selected_value) & (WCrashes['Year']== my_dropdown) & 
                                  (WCrashes['Timings'] != 'TOTAL')][[radio_items,'Timings']] 
        Selected_value = ' / ' + Selected_value
    x = Weekly_Crashes['Timings']
    y = Weekly_Crashes[radio_items]

    fig = go.Figure(data=go.Scatter(x=x, y=y,line=dict(color='black')))
    fig.update_layout(
        paper_bgcolor='black',
        # plot_bgcolor='black',
        margin=dict(t=110,b=0,l=0,r=0),
        title={'text': 'Frequency Of Crashes On ' + radio_items + ' ' + ' For Year ' +str(my_dropdown) + Selected_value,
               'y': 0.93,
               'x': 0.5,
               'xanchor': 'center',
               'yanchor': 'top'},
        titlefont={'color': 'white',
                   'size': 20},
        font=dict(family='sans-serif',
                  color='white',
                  size=12),
        xaxis_tickfont_size=20,
        xaxis=dict(color='white'),
        yaxis=dict(
            color='white',
            title='Crashes',
            titlefont_size=16,
            tickfont_size=20,
            ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
            ),
    )
        
    return fig

@app.callback(Output('bar_chart', 'figure'),
              [Input('my_dropdown','value'),
               Input('Selected_value','value')])
def updatecard(my_dropdown,Selected_value):
    if (Selected_value == '' or Selected_value == 'All'):
        MonthDf = US_Crashes[(US_Crashes['Year'] == 2020) & (US_Crashes['Months'] != 'TOTAL') & (US_Crashes['State'] == 'USA')]
        years = MonthDf['Months']
        Month_Fatalities = MonthDf['Crashes']
    else:
        MonthDf = US_Crashes[(US_Crashes['Year'] == 2020) & (US_Crashes['Months'] != 'TOTAL') & (US_Crashes['State'] == Selected_value)]
        years = MonthDf['Months']
        Month_Fatalities = MonthDf['Crashes']
        Selected_value = '- ' + Selected_value + ' '

    fig = go.Figure()
    fig.add_trace(go.Bar(x=years,
                         y=Month_Fatalities,
                        #  marker_color='rgb(55, 83, 109)'
                        #marker_color='black'
                        marker={'color': Month_Fatalities,
                                'colorscale':'Reds'}

    ))

    fig.update_layout(
        paper_bgcolor='black',
        # plot_bgcolor='black',
        margin=dict(t=180,b=0,l=0,r=0),
        title={'text': 'Fatalities By Month ' + (Selected_value) + ' For Year ' +str(my_dropdown),
               'y': 0.93,
               'x': 0.5,
               'xanchor': 'center',
               'yanchor': 'top'},
        titlefont={'color': 'white',
                   'size': 20},
        font=dict(family='sans-serif',
                  color='white',
                  size=12),
        xaxis_tickfont_size=14,
        xaxis=dict(color='white'),
        yaxis=dict(
            color='white',
            title='Fatalities',
            titlefont_size=16,
            tickfont_size=14,
            ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
            ),
        barmode='group',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
    )
        
    return fig

@app.callback(Output('pie_chart', 'figure'),
              [Input('my_dropdown','value'),
               Input('Selected_value','value')])
def updatecard(my_dropdown,Selected_value):
    if (Selected_value == '' or Selected_value == 'All'):
        AgeGroupDf = AgeGroup[(AgeGroup['Year'] == my_dropdown) & (AgeGroup['Age Type'] != 'TOTAL')]
        AgeGroupDf_1 = AgeGroupDf.groupby(['Age Type'])['Age Fatalities'].sum().reset_index()
        Age_labels = AgeGroupDf_1['Age Type']
        Age_values = AgeGroupDf_1['Age Fatalities']

    else:
        AgeGroupDf = AgeGroup[(AgeGroup['Year'] == my_dropdown) & (AgeGroup['Age Type'] != 'TOTAL') &
                              (AgeGroup['State'] == Selected_value)]
        Age_labels = AgeGroupDf['Age Type']
        Age_values = AgeGroupDf['Age Fatalities']
        Selected_value = '- ' + Selected_value
        
    return {
        'data': [go.Pie(
            labels=Age_labels,
            values=Age_values,
            #marker=dict(colors=colors),
            hoverinfo='label+value+percent',
            textinfo='label',
            hole=.7,
            rotation=45,
            # insidetextorientation= 'radial'
        )],

        'layout': go.Layout(
            margin=dict(t=110,b=0,l=0,r=0),
            title={'text': 'Fatalities By Age Group ' + (Selected_value),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            #paper_bgcolor='rgb(51, 51, 45)',
            paper_bgcolor='black',
            #plot_bgcolor='rgb(51, 51, 45)',
            plot_bgcolor='black',
            legend={'orientation': 'h',
                    'bgcolor': 'black',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7}
        )
    }

@app.callback([Output('Crash_Card', 'children'),
               Output('Total_Crashes', 'children')],
              [Input('my_dropdown','value'),
               Input('Selected_value','value')])
def updatecard(my_dropdown,Selected_value):
    if (Selected_value == '' or Selected_value == 'All'):
        Previous_Year = my_dropdown - 1
        Total_Current = US_Crashes[(US_Crashes['Year']==my_dropdown) & 
                                   (US_Crashes['Months']=='TOTAL') &
                                   (US_Crashes['State']=='USA')]['Crashes']
        Total_Current = int(Total_Current.to_string(index=False))
        Total_Previous = US_Crashes[(US_Crashes['Year']==Previous_Year) & 
                                   (US_Crashes['Months']=='TOTAL') &
                                   (US_Crashes['State']=='USA')]['Crashes']
        Total_Previous = int(Total_Previous.to_string(index=False))
        percentage_Change = ((Total_Current-Total_Previous)/Total_Previous) * 100.0
        if percentage_Change > 0:
            percentage_Change = "{:.2f}".format(percentage_Change)
            return "{:,}".format(Total_Current),html.H4(percentage_Change + "% vs PreviousYear",className="bi bi-caret-up-fill text-danger")
        else:
            percentage_Change = "{:.2f}".format(percentage_Change)
            return "{:,}".format(Total_Current),html.H4(percentage_Change + "% vs PreviousYear",className="bi bi-caret-down-fill text-success")
    else:
        Previous_Year = my_dropdown - 1
        Total_Current = US_Crashes[(US_Crashes['Year']==my_dropdown) & 
                                   (US_Crashes['Months']=='TOTAL') &
                                   (US_Crashes['State']== Selected_value)]['Crashes']
        Total_Current = int(Total_Current.to_string(index=False))
        Total_Previous = US_Crashes[(US_Crashes['Year']==Previous_Year) & 
                                   (US_Crashes['Months']=='TOTAL') &
                                   (US_Crashes['State']== Selected_value)]['Crashes']
        Total_Previous = int(Total_Previous.to_string(index=False))
        percentage_Change = ((Total_Current-Total_Previous)/Total_Previous) * 100.0
        if percentage_Change > 0:
            percentage_Change = "{:.2f}".format(percentage_Change)
            return "{:,}".format(Total_Current),html.H4(percentage_Change + "% vs PreviousYear",className="bi bi-caret-up-fill text-danger")
        else:
            percentage_Change = "{:.2f}".format(percentage_Change)
            return "{:,}".format(Total_Current),html.H4(percentage_Change + "% vs PreviousYear",className="bi bi-caret-down-fill text-success")

@app.callback([Output('Fatality_Card', 'children'),
               Output('Total_Fatalities', 'children')],
              [Input('my_dropdown','value'),
               Input('Selected_value','value')])
def updatecard(my_dropdown,Selected_value):
    if (Selected_value == '' or Selected_value == 'All'):
        Previous_Year = my_dropdown - 1
        Total_Current = Fatalities[(Fatalities['Year']==my_dropdown) & 
                                   (Fatalities['GenderTypes']=='TOTAL')]['GenderFatalities'].sum()
        Total_Previous = Fatalities[(Fatalities['Year']==Previous_Year) &
                                   (Fatalities['GenderTypes']=='TOTAL')]['GenderFatalities'].sum()
        percentage_Change = ((Total_Current-Total_Previous)/Total_Previous) * 100.0
        if percentage_Change > 0:
            percentage_Change = "{:.2f}".format(percentage_Change)
            return "{:,}".format(Total_Current),html.H4(percentage_Change + "% vs PreviousYear",className="bi bi-caret-up-fill text-danger")
        else:
            percentage_Change = "{:.2f}".format(percentage_Change)
            return "{:,}".format(Total_Current),html.H4(percentage_Change + "% vs PreviousYear",className="bi bi-caret-down-fill text-success")
    else:
        Previous_Year = my_dropdown - 1
        Total_Current = Fatalities[(Fatalities['Year']==my_dropdown) & 
                                   (Fatalities['GenderTypes']=='TOTAL') &
                                   (Fatalities['State']== Selected_value)]['GenderFatalities']
        Total_Current = int(Total_Current.to_string(index=False))
        Total_Previous = Fatalities[(Fatalities['Year']==Previous_Year) &
                                   (Fatalities['GenderTypes']=='TOTAL') &
                                   (Fatalities['State']== Selected_value)]['GenderFatalities']
        Total_Previous = int(Total_Previous.to_string(index=False))
        
        percentage_Change = ((Total_Current-Total_Previous)/Total_Previous) * 100.0
        if percentage_Change > 0:
            percentage_Change = "{:.2f}".format(percentage_Change)
            return "{:,}".format(Total_Current),html.H4(percentage_Change + "% vs PreviousYear",className="bi bi-caret-up-fill text-danger")
        else:
            percentage_Change = "{:.2f}".format(percentage_Change)
            return "{:,}".format(Total_Current),html.H4(percentage_Change + "% vs PreviousYear",className="bi bi-caret-down-fill text-success")


@app.callback([Output('Ped_Card', 'children'),
               Output('Pedestrian_Crahes', 'children')],
              [Input('my_dropdown','value'),
               Input('Selected_value','value')])
def updatecard(my_dropdown,Selected_value):
    if (Selected_value == '' or Selected_value == 'All'):
        Previous_Year = my_dropdown - 1
        Total_Current = PersonGroup[(PersonGroup['Year']==my_dropdown) & 
                                     (PersonGroup['PersonType']=='Pedestrian')][['PersonKilled']].sum()
        Total_Current = int(Total_Current.to_string(index=False))
        Total_Previous = PersonGroup[(PersonGroup['Year']==Previous_Year) & 
                                     (PersonGroup['PersonType']=='Pedestrian')][['PersonKilled']].sum()
        Total_Previous = int(Total_Previous.to_string(index=False))
        percentage_Change = ((Total_Current-Total_Previous)/Total_Previous) * 100.0
        if percentage_Change > 0:
            percentage_Change = "{:.2f}".format(percentage_Change)
            return "{:,}".format(Total_Current),html.H4(percentage_Change + "% vs PreviousYear",className="bi bi-caret-up-fill text-danger")
        else:
            percentage_Change = "{:.2f}".format(percentage_Change)
            return "{:,}".format(Total_Current),html.H4(percentage_Change + "% vs PreviousYear",className="bi bi-caret-down-fill text-success")
    else:
        Previous_Year = my_dropdown - 1
        Total_Current = PersonGroup[(PersonGroup['Year']==my_dropdown) & 
                                     (PersonGroup['PersonType']=='Pedestrian') &
                                     (PersonGroup['State']== Selected_value)]['PersonKilled']
        Total_Current = int(Total_Current.to_string(index=False))
        Total_Previous = PersonGroup[(PersonGroup['Year']==Previous_Year) & 
                                     (PersonGroup['PersonType']=='Pedestrian') &
                                     (PersonGroup['State']== Selected_value)]['PersonKilled']
        Total_Previous = int(Total_Previous.to_string(index=False))
        percentage_Change = ((Total_Current-Total_Previous)/Total_Previous) * 100.0
        
        if percentage_Change > 0:
            percentage_Change = "{:.2f}".format(percentage_Change)
            return "{:,}".format(Total_Current),html.H4(percentage_Change + "% vs PreviousYear",className="bi bi-caret-up-fill text-danger")
        else:
            percentage_Change = "{:.2f}".format(percentage_Change)
            return "{:,}".format(Total_Current),html.H4(percentage_Change + "% vs PreviousYear",className="bi bi-caret-down-fill text-success")

@app.callback([Output('Alc_Card', 'children'),
               Output('Alcohol_Crashes', 'children')],
              [Input('my_dropdown','value'),
               Input('Selected_value','value')])
def updatecard(my_dropdown,Selected_value):
    if Selected_value == '' or Selected_value == 'All':
        Previous_Year = my_dropdown - 1
        Alcohol_Current = Alcohol
        Alcohol_Previous = Alcohol
        #Current Year
        AlcoholDf = Alcohol_Current[(Alcohol_Current['Year']==my_dropdown) & (Alcohol_Current['Timings'] == 'TOTAL')].index
        Alcohol_Current.drop(AlcoholDf, inplace=True)
        AlcoholData = Alcohol_Current[(Alcohol_Current['State'] != 'USA') & (Alcohol_Current['Year']==my_dropdown)][['Total_Alcohol_Impaired_Driving','State']]
        AlcoholData = AlcoholData.groupby('State').sum()
        Total_Current = AlcoholData['Total_Alcohol_Impaired_Driving'].sum()
        
        #Previous Year
        AlcoholDf = Alcohol_Previous[(Alcohol_Current['Year']==Previous_Year) & (Alcohol_Previous['Timings'] == 'TOTAL')].index
        Alcohol_Previous.drop(AlcoholDf, inplace=True)
        AlcoholDataP = Alcohol_Previous[(Alcohol_Current['State'] != 'USA') & (Alcohol_Previous['Year']==Previous_Year)][['Total_Alcohol_Impaired_Driving','State']]
        AlcoholDataP = AlcoholDataP.groupby('State').sum()
        Total_Previous = AlcoholDataP['Total_Alcohol_Impaired_Driving'].sum()

        percentage_Change = ((Total_Current-Total_Previous)/Total_Previous) * 100.0
        if percentage_Change > 0:
            percentage_Change = "{:.2f}".format(percentage_Change)
            return "{:,}".format(Total_Current),html.H4(percentage_Change + "% vs PreviousYear",className="bi bi-caret-up-fill text-danger")
        else:
            percentage_Change = "{:.2f}".format(percentage_Change)
            return "{:,}".format(Total_Current),html.H4(percentage_Change + "% vs PreviousYear",className="bi bi-caret-down-fill text-success")
    else:
        Previous_Year = my_dropdown - 1
        Alcohol_Current = Alcohol
        Alcohol_Previous = Alcohol
        #Current Year
        AlcoholDf = Alcohol_Current[(Alcohol_Current['Year']==my_dropdown) & (Alcohol_Current['Timings'] == 'TOTAL')].index
        Alcohol_Current.drop(AlcoholDf, inplace=True)
        AlcoholData = Alcohol_Current[(Alcohol_Current['State'] == Selected_value) & (Alcohol_Current['Year']==my_dropdown)][['Total_Alcohol_Impaired_Driving','State']]
        AlcoholData = AlcoholData.groupby('State').sum()
        Total_Current = AlcoholData['Total_Alcohol_Impaired_Driving'].sum()
        
        #Previous Year
        AlcoholDf = Alcohol_Previous[(Alcohol_Current['Year']==Previous_Year) & (Alcohol_Previous['Timings'] == 'TOTAL')].index
        Alcohol_Previous.drop(AlcoholDf, inplace=True)
        AlcoholDataP = Alcohol_Previous[(Alcohol_Current['State'] == Selected_value) & (Alcohol_Previous['Year']==Previous_Year)][['Total_Alcohol_Impaired_Driving','State']]
        AlcoholDataP = AlcoholDataP.groupby('State').sum()
        Total_Previous = AlcoholDataP['Total_Alcohol_Impaired_Driving'].sum()

        percentage_Change = ((Total_Current-Total_Previous)/Total_Previous) * 100.0
        if percentage_Change > 0:
            percentage_Change = "{:.2f}".format(percentage_Change)
            return "{:,}".format(Total_Current),html.H4(percentage_Change + "% vs PreviousYear",className="bi bi-caret-up-fill text-danger")
        else:
            percentage_Change = "{:.2f}".format(percentage_Change)
            return "{:,}".format(Total_Current),html.H4(percentage_Change + "% vs PreviousYear",className="bi bi-caret-down-fill text-success")

@app.callback(Output('Selected_value', 'value'),
              [Input('line_chart', 'clickData')])
def updatecard(clickData):
    if clickData is not None:
        StateName = TotalCrashes[TotalCrashes['State_Code'] == clickData['points'][0]['location']]
        return ''.join(StateName['State'].unique())
    else:
        value = ''
        return value

@app.callback(Output('line_chart', 'figure'),
               Input('my_dropdown','value'))
def updatecard(my_dropdown):  
    TotalCrashes_Updated = TotalCrashes[TotalCrashes['Year']==my_dropdown]   
    fig = go.Figure(
        data=go.Choropleth(
        locations=TotalCrashes_Updated['State_Code'], # Spatial coordinates
        z = TotalCrashes_Updated['GenderFatalities'].astype(float), # Data to be color-coded
            locationmode = 'USA-states'  ,
            colorscale = 'Reds',
            colorbar_title = "USD",     
        ),layout = go.Layout(
            geo=dict(
                bgcolor='black',lakecolor='rgb(51, 51, 45)',
                landcolor = 'rgba(51,17,0,0.2)',
                subunitcolor='black'),
            title={'text': 'Total Crashes Across USA for ' + str(my_dropdown),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            geo_scope='usa',
            margin={"r":0,"t":40,"l":0,"b":0},
            # paper_bgcolor='rgb(51, 51, 45)',
            # plot_bgcolor='rgb(51, 51, 45)',
            paper_bgcolor='black',
            plot_bgcolor='black',
        )
    )
    
    return fig

if __name__ == "__main__":
    app.run(debug=True, port=8050)
