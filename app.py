# app.py
# Auto Sales Dashboard - Dash Web App
# Author: Mohit Phulwani

import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Auto Sales Dashboard"
app.config.suppress_callback_exceptions = True  # Avoid exceptions before callbacks load

# Load the automobile dataset
auto_data = pd.read_csv('automobileEDA.csv', encoding="ISO-8859-1")

# Define the layout of the app
app.layout = html.Div([
    html.H1(
        'Car Automobile Components Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 28}
    ),

    html.Div([
        # Dropdown for selecting Drive Wheels
        html.Div([
            html.H2('Drive Wheels Type:', style={'margin-right': '1em'}),
            dcc.Dropdown(
                id='drive-dropdown',
                options=[
                    {'label': 'Rear Wheel Drive', 'value': 'rwd'},
                    {'label': 'Front Wheel Drive', 'value': 'fwd'},
                    {'label': 'Four Wheel Drive', 'value': '4wd'}
                ],
                value='rwd',
                clearable=False
            )
        ], style={'width': '40%', 'margin': '20px'}),

        # Container for charts
        html.Div([
            html.Div(id='pie-chart', style={'flex': 1, 'padding': '10px'}),
            html.Div(id='bar-chart', style={'flex': 1, 'padding': '10px'})
        ], style={'display': 'flex', 'flex-wrap': 'wrap'})
    ])
])

# Callback to update charts based on dropdown selection
@app.callback(
    [Output('pie-chart', 'children'),
     Output('bar-chart', 'children')],
    [Input('drive-dropdown', 'value')]
)
def update_charts(selected_drive):
    """
    Filters the data based on selected drive wheels
    and returns updated Pie and Bar charts.
    """
    # Filter and group data
    filtered_df = auto_data[auto_data['drive-wheels'] == selected_drive].groupby(
        ['drive-wheels', 'body-style'], as_index=False
    ).mean()

    # Create Pie chart
    pie_fig = px.pie(
        filtered_df,
        values='price',
        names='body-style',
        title=f"Price Distribution by Body Style ({selected_drive.upper()})"
    )

    # Create Bar chart
    bar_fig = px.bar(
        filtered_df,
        x='body-style',
        y='price',
        title=f"Average Price by Body Style ({selected_drive.upper()})"
    )

    # Return charts as Dash Graph components
    return [dcc.Graph(figure=pie_fig), dcc.Graph(figure=bar_fig)]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
