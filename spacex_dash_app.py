# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('spacex_launch_dash.csv')
min_value=df['Payload Mass (kg)'].min()
max_value=df['Payload Mass (kg)'].max()
# Initialize the app
app = Dash()

# App layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),         
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=[{'label': 'All Sites', 'value': 'ALL'},{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},{'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},{'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},{'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}], value='ALL',placeholder="place holder here",searchable=True),
                                html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(figure={},id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0,max=10000,step=1000,
                                                marks={0: '0',2500: '2500',5000:'5000',10000:'10000'},
                                                value=[min_value,max_value]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(figure={},id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    filtered_df = df
    if entered_site == 'ALL':
        fig = px.pie(df, values='class', names='Launch Site', title='Total Success launches By Site',hole=0.3)
        return fig
    else:
        filtered_df=df[df['Launch Site']==entered_site]
        success_counts = filtered_df['class'].value_counts().reset_index()
        success_counts.columns = ['class', 'count']
        fig = px.pie(success_counts, values='count', names='class', title=f'Total Success launches By Site-{entered_site}',hole=0.3)
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@callback(
        Output(component_id='success-payload-scatter-chart', component_property='figure'),
        [Input(component_id='site-dropdown', component_property='value'), 
        Input(component_id="payload-slider", component_property="value")]
)
def get_scatter_plot(entered_site,payload_range):
    low,high=payload_range
    filter_df=df[(df['Payload Mass (kg)']>=low)&(df['Payload Mass (kg)']<=high)]
    
    if entered_site=='ALL':
        fig=px.scatter(df,x='Payload Mass (kg)',y='class',title='Correlation between Payload and Success for all Sites',color="Booster Version Category",labels={'class': 'Launch Outcome'})
        return fig
    else:
        filter_df=df[df['Launch Site']==entered_site]
        fig=px.scatter(filter_df,x='Payload Mass (kg)',y='class',title=f'Correlation between Payload and Success for {entered_site}',color="Booster Version Category",labels={'class': 'Launch Outcome'})
        return fig
# Run the app
if __name__ == '__main__':
    app.run(debug=True)