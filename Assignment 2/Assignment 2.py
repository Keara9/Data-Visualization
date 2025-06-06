import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import base64


#Create the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "New Zealand"

#load the data
df_GDP = pd.read_csv('GDP/GDP cleaned.csv')
df_InfantMortality = pd.read_csv('Infant Mortality/Infant Mortality Cleaned.csv')
df_Freshwater = pd.read_csv('Freshwater Data/NewZealand Freshwater cleaned.csv')

NZFlag = "data:image/png;base64," + base64.b64encode(open("NZ Flag.png", 'rb').read()).decode('utf-8')

 # water stress level over time graph
water_stress_series = 'Level of water stress: freshwater withdrawal as a proportion of available freshwater resources'

fig_water_stress = px.bar(
    df_Freshwater[df_Freshwater['Series Name'] == water_stress_series],
    x='Year',
    y='Value',
    title='New Zealand Water Stress Trends (1985-2021)',
    labels={'Value': 'Water Stress', 'Year': 'Year'},
    color_discrete_sequence=['#1f77b4']
)
fig_water_stress.update_layout(
        xaxis_title='Year',
        yaxis_title='Water Stress (%)',
        template='plotly_white'
    )

# water resources graph
water_resources = df_Freshwater[
    (df_Freshwater['Series Name'] == 'Renewable internal freshwater resources, total (billion cubic meters)') |
    (df_Freshwater['Series Name'] == 'Annual freshwater withdrawals, total (billion cubic meters)')
]

fig_water_resources = px.line(
    water_resources,
    x='Year',
    y='Value',
    color='Series Name',
    title='New Zealand Water Resources and Freshwater Withdrawals (1985-2021)',
    labels={'Value': 'Water Resources (billion cubic meters)', 'Year': 'Year', 'Series Name': 'Series'},
    color_discrete_sequence=px.colors.qualitative.Set1
)

# define the layout of the Dash app
app.layout = html.Div([
    html.H1(),
    html.Div([
        html.Img(src=NZFlag, style={'width': '15%', 'height': '15%', 'float': 'left'}),
        html.H1("New Zealand Data Analysis", style={'textAlign': 'center'}),
        html.Img(src=NZFlag, style={'width': '15%', 'height': '15%', 'float': 'right'})
    ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'}),

    dcc.Tabs([
        # GDP Tab
        dcc.Tab(label='GDP Visualization', children=[
            html.H1("New Zealand GDP 1960 to 2023", style={'textAlign': 'center'}),
        
            # Dropdown to select a GDP series
            html.Div([
                html.Label("Select a GDP Series:", style={'fontSize': 18}),
                dcc.Dropdown(
                    id='gdp-series-dropdown',
                    options=[{'label': series, 'value': series} for series in df_GDP['Series Name'].unique()],
                    value=df_GDP['Series Name'].unique()[0], 
                    clearable=False,
                    style={'width': '50%', 'margin': 'auto'}
                )
            ]),

            # Graph to display the GDP data
            dcc.Graph(id='gdp-graph')
        ]),
        # Infant Mortality Tab
        dcc.Tab(label='Infant Mortality Visualization', children=[
            html.H1("Infant Mortality in New Zealand from 1960 to 2022", style={'textAlign': 'center'}),

            # Dropdown to select an Infant Mortality series
            html.Div([
                html.Label("Select an Infant Mortality Series:", style={'fontSize': 18}),
                dcc.Dropdown(
                    id='infant-mortality-series-dropdown',
                    options=[{'label': series, 'value': series} for series in df_InfantMortality['Series Name'].unique()],
                    value=df_InfantMortality['Series Name'].unique()[0],  # Default value (first series)
                    clearable=False,
                    style={'width': '50%', 'margin': 'auto'}
                )
            ]),

            # Graph to display the infant mortality data
            dcc.Graph(id='infant-mortality-graph'),

            # Data table to show the raw data
            dash_table.DataTable(
                id='infant-mortality-table',
                columns=[{"name": i, "id": i} for i in df_InfantMortality.columns],
                data=df_InfantMortality.to_dict('records'),
                page_size=10
            )
        ]),

        # Freshwater Tab
        dcc.Tab(label='New Zealand Freshwater Visualizations', children=[
            html.H1("Freshwater Withdrawals by Sector", style={'textAlign': 'center'}),
            html.Div([  
                html.Label("Select a Year:", style={'fontSize': 18}),
                dcc.Slider(
                    id='freshwater-year-slider',
                    min=int(df_Freshwater['Year'].min()),
                    max=int(df_Freshwater['Year'].max()),
                    step=1,
                    marks={int(year): str(year) for year in df_Freshwater['Year'].unique()},
                    value=int(df_Freshwater['Year'].min()), 
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ]),
            dcc.Graph(id='freshwater-graph'), 
            dcc.Graph(figure=fig_water_stress, id='freshwater-graph2'), 
            dcc.Graph(figure=fig_water_resources, id='freshwater-graph3'),

            dash_table.DataTable(
                id='freshwater-table',
                columns=[{"name": i, "id": i} for i in df_Freshwater.columns],
                data=df_Freshwater.to_dict('records'),
                page_size=10
            )
        ])
    ])
])
# Callback to update the GDP graph
@callback(
    Output('gdp-graph', 'figure'),
    Input('gdp-series-dropdown', 'value')
)
def update_gdp_graph(selected_series):
     
    # Filter the data for the selected series
    filtered_gdp_df = df_GDP[df_GDP['Series Name'] == selected_series]
    
    # Scatter plot to compare selected series
    fig = px.area(
        filtered_gdp_df,
        x='Year',
        y='Value',
        title=f'{selected_series} Over Time in New Zealand',
        color='Series Name'
    )
    
    # Update the layout
    fig.update_layout(
        colorway=['#FFA07A'],
        xaxis_title='Year',
        yaxis_title='Value',
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig


# Callback to update the Infant Mortality graph
@callback(
    Output('infant-mortality-graph', 'figure'),
    Input('infant-mortality-series-dropdown', 'value')
)
def update_graph(selected_series):
    # Filter the data for the selected series
    filtered_df = df_InfantMortality[df_InfantMortality['Series Name'] == selected_series]
    
    # Create a line plot for Infant Mortality
    fig = px.line(
        filtered_df,
        x='Year',  
        y='Value',  
        title=f'{selected_series} Over Time in New Zealand',
        color_discrete_sequence=['green'],
        )
    
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Value',
        hovermode='x unified'
    )
    
    return fig

@callback(
    Output('freshwater-graph', 'figure'),
    Input('freshwater-year-slider', 'value')
)
def update_freshwater_graph(selected_year):
    
    # Filter the data for the selected year
    filtered_df = df_Freshwater[df_Freshwater['Year'] == selected_year]
    
    # Filter the data for the freshwater withdrawal series
    withdrawal_series = [
        'Annual freshwater withdrawals, agriculture (% of total freshwater withdrawal)',
        'Annual freshwater withdrawals, industry (% of total freshwater withdrawal)',
        'Annual freshwater withdrawals, domestic (% of total freshwater withdrawal)'
    ]
    filtered_df = filtered_df[filtered_df['Series Name'].isin(withdrawal_series)]
    
    # Create a pie chart for freshwatee withdrawals
    fig = px.pie(
        filtered_df,
        values='Value',
        names='Series Name',
        title=f'Annual Freshwater Withdrawals by Industry ({selected_year})',
        hole=0.3
    )
    
    return fig 



if __name__ == '__main__':
    app.run(debug=True)
