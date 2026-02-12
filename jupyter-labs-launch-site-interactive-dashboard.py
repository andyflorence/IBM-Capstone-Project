# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import webbrowser
from pathlib import Path

in_file = 'spacex_launch_dash.csv'

if Path(in_file).exists():
   spacex_df = pd.read_csv("spacex_launch_dash.csv")
   max_payload = spacex_df['Payload Mass (kg)'].max()
   min_payload = spacex_df['Payload Mass (kg)'].min()
else:
    print(f" {in_file} File does not exist")


# Confirm data loaded
print(spacex_df.shape)
print(spacex_df.columns)
spacex_df.head()

# Create a dash application
#app = dash.Dash(__name__)
app = dash.Dash(__name__, title="IBM - SpaceX Launch Dashboard")

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1: Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'Cape Canaveral - Launch Complex 40', 'value': 'CCAFS LC-40'},
            {'label': 'Vandenberg - Launch Complex 4 East', 'value': 'VAFB SLC-4E'},
            {'label': 'Kennedy Space Center - Launch Complex 39A', 'value': 'KSC LC-39A'},
            {'label': 'Cape Canaveral - Space Launch Complex 40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder="Select a Launch Site",
        searchable=True
    ),
    html.Br(),

    # TASK 2: Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: RangeSlider
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
        value=[min_payload, max_payload]
    ),
    html.Br(),

    # TASK 4: Scatter chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2 callback: Pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Sum of successes per launch site (class is 0/1)
        fig = px.pie(
            spacex_df,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Site (All Sites)'
        )
        return fig
    else:
        # Success vs Failure for a specific site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        outcome_counts = (
            filtered_df['class']
            .value_counts()
            .rename(index={1: 'Success', 0: 'Failure'})
            .reset_index()
        )
        outcome_counts.columns = ['Outcome', 'Count']

        fig = px.pie(
            outcome_counts,
            values='Count',
            names='Outcome',
            title=f'Success vs Failure for site {entered_site}'
        )
        return fig

# TASK 4 callback: Scatter chart (site + payload range)
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')
)
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range

    # Filter by payload range first
    df_filtered = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    # Then filter by site if needed
    if entered_site != 'ALL':
        df_filtered = df_filtered[df_filtered['Launch Site'] == entered_site]
        title = f'Payload vs. Launch Outcome for site {entered_site}'
    else:
        title = 'Payload vs. Launch Outcome for All Sites'

    fig = px.scatter(
        df_filtered,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=title
    )
    return fig

# Run the app and the open browser 
if __name__ == '__main__':
    #app.run_server()
    webbrowser.open("http://127.0.0.1:8050")
    app.run()

