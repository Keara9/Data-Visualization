import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc


#Create the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#load the data
df_GDP = pd.read_csv('GDP/GDP cleaned.csv')
df_InfantMortality = pd.read_csv('Infant Mortality/Infant Mortality Cleaned.csv')
df_Freshwater = pd.read_csv('Freshwater Data/NewZealand Freshwater cleaned.csv')

# define the layout of the Dash app
                    
app.layout = html.Div(
    dcc.Tabs([
        #GDP Tab
        dcc.Tab(label='GDP Visualization', children=[
            html.H1("New Zealand GDP Visualization", style={'textAlign': 'center'}),
        
            # Dropdown to select a GDP series
            html.Div([
                html.Label("Select a GDP Series:", style={'fontSize': 18}),
                dcc.Dropdown(
                    id='gdp-series-dropdown',
                    options=[{'label': series, 'value': series} for series in df_GDP['Series Name'].unique()],
                    value=df_GDP['Series Name'].unique()[0],  # Default value (first series)
                    clearable=False,
                    style={'width': '50%', 'margin': 'auto'}
                )
            ], style={'marginBottom': 20}),
        
            #graph to display the gdp data
            dcc.Graph(id='gdp-graph')
        ]),  
        #Infant Mortality Tab
        dcc.Tab(label='Infant Mortality Visualization', children=[
            html.H1("Infant Mortality in New Zealand from 1960 to 2022", style={'textAlign': 'center'}),

            #Dropdown to select an Infant Mortality series
            html.Div([
                html.Label("Select an Infant Mortality Series:", style={'fontSize': 18}),
                dcc.Dropdown(
                    id='infant-mortality-series-dropdown',
                    options=[{'label': series, 'value': series} for series in df_InfantMortality['Series Name'].unique()],
                    value=df_InfantMortality['Series Name'].unique()[0],  
                    clearable=False,
                    style={'width': '75%', 'margin': 'auto'}
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

        #Freshwater Tab
        dcc.Tab(label='Freshwater Visualization', children=[
            html.H1("Freshwater Use in New Zealand by Industry", style={'textAlign': 'center'}),
            html.Div([  
                html.Label("Select a Year:", style={'fontSize': 18}),
            dcc.Dropdown(
                id='freshwater-year-dropdown',
                options=[{'label': year, 'value': year} for year in df_Freshwater['Year'].unique()],
                value=df_Freshwater['Year'].unique()[0],  # Default value (first year)
                clearable=False,
                style={'width': '50%', 'margin': 'auto'}
            ),
            dcc.Graph(id='freshwater-graph'),  
            dash_table.DataTable(
                id='freshwater-table',
                columns=[{"name": i, "id": i} for i in df_Freshwater.columns],
                data=df_Freshwater.to_dict('records'),
                page_size=10
            )
            ])
        ])
    ])
)
# Callback to update the GDP graph
@callback(
    Output('gdp-graph', 'figure'),
    Input('gdp-series-dropdown', 'value')
)
def update_gdp_graph(selected_series):
     
    #Filter the data for the selected series
    filtered_gdp_df = df_GDP[df_GDP['Series Name'] == selected_series]
    
    # Create a line plot with Year on the x-axis and Value on the y-axis
    fig = px.line(
        filtered_gdp_df,
        x='Year',
        y='Value',
        title=f'{selected_series} Over Time',
        labels={'Value': selected_series, 'Year': 'Year'},
    )
    
    # Update layout for better readability
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
    
    # Create a line plot with Year on the x-axis and Value on the y-axis
    fig = px.bar(
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
    Input('freshwater-year-dropdown', 'value')
)
def update_freshwater_graph(selected_year):
    
    # Filter the data for the selected year
    filtered_df = df_Freshwater[df_Freshwater['Year'] == selected_year]
    
    # Filter the data for the freshwater withdrawal series
   # withdrawal_series = [
    #    'Annual freshwater withdrawals, agriculture (% of total freshwater withdrawal)',
     #   'Annual freshwater withdrawals, industry (% of total freshwater withdrawal)',
     #   'Annual freshwater withdrawals, domestic (% of total freshwater withdrawal)'
   # ]
    #filtered_df = filtered_df[filtered_df['Series Name'].isin(withdrawal_series)]
    
    fig = px.line(
        filtered_df,
        values ='Value',
        names='Series Name',
        title=f'Annual Freshwater Withdrawals ({selected_year})',
        hole=0.3
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)
