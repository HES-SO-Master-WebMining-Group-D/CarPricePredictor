from dash import Dash, html, dcc, Input, Output
import dash

from dash.dependencies import Input, Output
import pandas as pd

# Load the dataset
df = pd.read_csv('cleaned_cars.csv')

# Extract unique values for dropdown options
brands = df['brand'].unique()
body_types = df['body_type'].unique()
fuel_types = df['fuel_type'].unique()

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H2('Basic specifications & Location'),
    html.Label('Brand'),
    dcc.Dropdown(
        id='make-dropdown',
        options=[{'label': brand, 'value': brand} for brand in brands],
        placeholder="Select a brand"
    ),
    html.Br(),
    html.Label('Body type'),
    dcc.Dropdown(
        id='body-type-dropdown',
        options=[{'label': body_type, 'value': body_type} for body_type in body_types],
        placeholder="Select a body type"
    ),
    html.Br(),
    html.Label('Fuel type'),
    dcc.Dropdown(
        id='fuel-type-dropdown',
        options=[{'label': fuel_type, 'value': fuel_type} for fuel_type in fuel_types],
        placeholder="Select a fuel type"
    ),
    html.Br(),
    html.Label('First registration'),
    html.Div([
        dcc.Input(id='first-registration-from', type='number', placeholder='From', min=1900, max=2024),
        dcc.Input(id='first-registration-to', type='number', placeholder='To', min=1900, max=2024)
    ]),
    html.Br(),
    html.Label('Price'),
    html.Div([
        dcc.Input(id='price-from', type='number', placeholder='From', min=0),
        dcc.Input(id='price-to', type='number', placeholder='To', min=0)
    ]),
    html.Br(),
    html.Div(id='output-container')
])

# Callback to handle user inputs and filter the dataset
@app.callback(
    Output('output-container', 'children'),
    Input('make-dropdown', 'value'),
    Input('body-type-dropdown', 'value'),
    Input('fuel-type-dropdown', 'value'),
    Input('first-registration-from', 'value'),
    Input('first-registration-to', 'value'),
    Input('price-from', 'value'),
    Input('price-to', 'value')
)
def update_output(make, body_type, fuel_type, first_reg_from, first_reg_to, price_from, price_to):
    filtered_df = df

    if make:
        filtered_df = filtered_df[filtered_df['brand'] == make]
    if body_type:
        filtered_df = filtered_df[filtered_df['body_type'] == body_type]
    if fuel_type:
        filtered_df = filtered_df[filtered_df['fuel_type'] == fuel_type]
    if first_reg_from:
        filtered_df = filtered_df[filtered_df['year'] >= first_reg_from]
    if first_reg_to:
        filtered_df = filtered_df[filtered_df['year'] <= first_reg_to]
    if price_from:
        filtered_df = filtered_df[filtered_df['price'] >= price_from]
    if price_to:
        filtered_df = filtered_df[filtered_df['price'] <= price_to]

    return html.Div([
        html.H4('Filtered Cars'),
        html.Table(
            # Header
            [html.Tr([html.Th(col) for col in filtered_df.columns])] +

            # Body
            [html.Tr([
                html.Td(filtered_df.iloc[i][col]) for col in filtered_df.columns
            ]) for i in range(min(len(filtered_df), 10))]  # Show up to 10 results
        )
    ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
