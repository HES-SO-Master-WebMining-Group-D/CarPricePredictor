from dash import Dash, html, dcc, Input, Output
import dash

from dash.dependencies import Input, Output
import pandas as pd


# Load the dataset
df = pd.read_csv('cleaned_cars.csv')

# Extract unique values for dropdown options
brands = df['brand'].unique()
models = df['model'].unique()
body_types = df['body_type'].unique()
fuel_types = df['fuel_type'].unique()
colors = df['color'].unique()
gearboxes = df['gearbox'].unique()
sellers = df['seller'].unique()
drivetrains = df['drivetrain'].unique()
emission_classes = df['emission_class'].unique()
conditions = df['condition'].unique()
upholsteries = df['upholstery'].unique()
upholstery_colors = df['upholstery_color'].unique()
countries = df['country'].unique()

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

    html.Label('Model'),
    dcc.Dropdown(
        id='model-dropdown',
        options=[{'label': model, 'value': model} for model in models],
        placeholder="Select a model"
    ),
    html.Br(),

    html.Label('Variant'),
    dcc.Input(id='variant-input', type='text', placeholder='e.g. Plus, GTI, etc.'),
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

    html.Label('Color'),
    dcc.Dropdown(
        id='color-dropdown',
        options=[{'label': color, 'value': color} for color in colors],
        placeholder="Select a color"
    ),
    html.Br(),

    html.Label('Gearbox'),
    dcc.Dropdown(
        id='gearbox-dropdown',
        options=[{'label': gearbox, 'value': gearbox} for gearbox in gearboxes],
        placeholder="Select a gearbox type"
    ),
    html.Br(),

    html.Label('Seller'),
    dcc.Dropdown(
        id='seller-dropdown',
        options=[{'label': seller, 'value': seller} for seller in sellers],
        placeholder="Select a seller type"
    ),
    html.Br(),

    html.Label('Drivetrain'),
    dcc.Dropdown(
        id='drivetrain-dropdown',
        options=[{'label': drivetrain, 'value': drivetrain} for drivetrain in drivetrains],
        placeholder="Select a drivetrain"
    ),
    html.Br(),

    html.Label('Emission Class'),
    dcc.Dropdown(
        id='emission-class-dropdown',
        options=[{'label': emission_class, 'value': emission_class} for emission_class in emission_classes],
        placeholder="Select an emission class"
    ),
    html.Br(),

    html.Label('Condition'),
    dcc.Dropdown(
        id='condition-dropdown',
        options=[{'label': condition, 'value': condition} for condition in conditions],
        placeholder="Select a condition"
    ),
    html.Br(),

    html.Label('Upholstery'),
    dcc.Dropdown(
        id='upholstery-dropdown',
        options=[{'label': upholstery, 'value': upholstery} for upholstery in upholsteries],
        placeholder="Select an upholstery type"
    ),
    html.Br(),

    html.Label('Upholstery Color'),
    dcc.Dropdown(
        id='upholstery-color-dropdown',
        options=[{'label': upholstery_color, 'value': upholstery_color} for upholstery_color in upholstery_colors],
        placeholder="Select an upholstery color"
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

    html.Label('Countries'),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in countries],
        placeholder="Select a country"
    ),
    html.Br(),

    html.Label('Mileage (km)'),
    html.Div([
        dcc.Input(id='mileage-from', type='number', placeholder='From', min=0),
        dcc.Input(id='mileage-to', type='number', placeholder='To', min=0)
    ]),
    html.Br(),

    html.Label('Power (kW)'),
    html.Div([
        dcc.Input(id='power-from', type='number', placeholder='From', min=0),
        dcc.Input(id='power-to', type='number', placeholder='To', min=0)
    ]),
    html.Br(),

    html.Label('Engine Size (cc)'),
    html.Div([
        dcc.Input(id='engine-size-from', type='number', placeholder='From', min=0),
        dcc.Input(id='engine-size-to', type='number', placeholder='To', min=0)
    ]),
    html.Br(),

    html.Label('Doors'),
    html.Div([
        dcc.Input(id='doors-from', type='number', placeholder='From', min=0),
        dcc.Input(id='doors-to', type='number', placeholder='To', min=0)
    ]),
    html.Br(),

    html.Label('Seats'),
    html.Div([
        dcc.Input(id='seats-from', type='number', placeholder='From', min=0),
        dcc.Input(id='seats-to', type='number', placeholder='To', min=0)
    ]),
    html.Br(),

    html.Div(id='output-container')
])

# Callback to handle user inputs and filter the dataset
@app.callback(
    Output('output-container', 'children'),
    Input('make-dropdown', 'value'),
    Input('model-dropdown', 'value'),
    Input('variant-input', 'value'),
    Input('body-type-dropdown', 'value'),
    Input('fuel-type-dropdown', 'value'),
    Input('color-dropdown', 'value'),
    Input('gearbox-dropdown', 'value'),
    Input('seller-dropdown', 'value'),
    Input('drivetrain-dropdown', 'value'),
    Input('emission-class-dropdown', 'value'),
    Input('condition-dropdown', 'value'),
    Input('upholstery-dropdown', 'value'),
    Input('upholstery-color-dropdown', 'value'),
    Input('first-registration-from', 'value'),
    Input('first-registration-to', 'value'),
    Input('price-from', 'value'),
    Input('price-to', 'value'),
    Input('country-dropdown', 'value'),
    Input('mileage-from', 'value'),
    Input('mileage-to', 'value'),
    Input('power-from', 'value'),
    Input('power-to', 'value'),
    Input('engine-size-from', 'value'),
    Input('engine-size-to', 'value'),
    Input('doors-from', 'value'),
    Input('doors-to', 'value'),
    Input('seats-from', 'value'),
    Input('seats-to', 'value')
)
def update_output(make, model, variant, body_type, fuel_type, color, gearbox, seller, drivetrain, emission_class, condition, upholstery, upholstery_color, first_reg_from, first_reg_to, price_from, price_to, country, mileage_from, mileage_to, power_from, power_to, engine_size_from, engine_size_to, doors_from, doors_to, seats_from, seats_to):
    filtered_df = df.copy()

    if make:
        filtered_df = filtered_df[filtered_df['brand'] == make]
    if model:
        filtered_df = filtered_df[filtered_df['model'] == model]
    if variant:
        filtered_df = filtered_df[filtered_df['variant'].str.contains(variant, case=False, na=False)]
    if body_type:
        filtered_df = filtered_df[filtered_df['body_type'] == body_type]
    if fuel_type:
        filtered_df = filtered_df[filtered_df['fuel_type'] == fuel_type]
    if color:
        filtered_df = filtered_df[filtered_df['color'] == color]
    if gearbox:
        filtered_df = filtered_df[filtered_df['gearbox'] == gearbox]
    if seller:
        filtered_df = filtered_df[filtered_df['seller'] == seller]
    if drivetrain:
        filtered_df = filtered_df[filtered_df['drivetrain'] == drivetrain]
    if emission_class:
        filtered_df = filtered_df[filtered_df['emission_class'] == emission_class]
    if condition:
        filtered_df = filtered_df[filtered_df['condition'] == condition]
    if upholstery:
        filtered_df = filtered_df[filtered_df['upholstery'] == upholstery]
    if upholstery_color:
        filtered_df = filtered_df[filtered_df['upholstery_color'] == upholstery_color]
    if first_reg_from:
        filtered_df = filtered_df[filtered_df['year'] >= first_reg_from]
    if first_reg_to:
        filtered_df = filtered_df[filtered_df['year'] <= first_reg_to]
    if price_from:
        filtered_df = filtered_df[filtered_df['price'] >= price_from]
    if price_to:
        filtered_df = filtered_df[filtered_df['price'] <= price_to]
    if country:
        filtered_df = filtered_df[filtered_df['country'] == country]
    if mileage_from:
        filtered_df = filtered_df[filtered_df['mileage'] >= mileage_from]
    if mileage_to:
        filtered_df = filtered_df[filtered_df['mileage'] <= mileage_to]
    if power_from:
        filtered_df = filtered_df[filtered_df['power'] >= power_from]
    if power_to:
        filtered_df = filtered_df[filtered_df['power'] <= power_to]
    if engine_size_from:
        filtered_df = filtered_df[filtered_df['engine_size'] >= engine_size_from]
    if engine_size_to:
        filtered_df = filtered_df[filtered_df['engine_size'] <= engine_size_to]
    if doors_from:
        filtered_df = filtered_df[filtered_df['doors'] >= doors_from]
    if doors_to:
        filtered_df = filtered_df[filtered_df['doors'] <= doors_to]
    if seats_from:
        filtered_df = filtered_df[filtered_df['seats'] >= seats_from]
    if seats_to:
        filtered_df = filtered_df[filtered_df['seats'] <= seats_to]

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

