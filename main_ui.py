import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import pickle

# Load the dataset
df = pd.read_csv('cleaned_cars.csv')

# Load the model from disk
model_filename = 'xgbr_price_predictor.pkl'
with open(model_filename, 'rb') as file:
    xgb_model = pickle.load(file)

# Load the feature names
feature_names_filename = 'feature_names.pkl'
with open(feature_names_filename, 'rb') as file:
    feature_names = pickle.load(file)

# Extract unique values for dropdown options, handling missing columns gracefully
def get_unique_values(df, column):
    return df[column].unique() if column in df.columns else []

brands = get_unique_values(df, 'brand')
models = get_unique_values(df, 'model')
fuel_types = get_unique_values(df, 'fuel_type')
gearboxes = get_unique_values(df, 'gearbox')
colors = get_unique_values(df, 'color')
sellers = get_unique_values(df, 'seller')
body_types = get_unique_values(df, 'body_type')
drivetrains = get_unique_values(df, 'drivetrain')
countries = get_unique_values(df, 'country')
conditions = get_unique_values(df, 'condition')
upholstery_colors = get_unique_values(df, 'upholstery_color')

# Default values for prediction
default_values = {
    'mileage': 50000,
    'power': 120,
    'engine_size': 1998,
    'doors': 4,
    'seats': 5,
    'brand': 'audi',
    'model': 'a4',
    'fuel_type': 'petrol',
    'gearbox': 'manual',
    'color': 'black',
    'seller': 'private',
    'body_type': 'sedan',
    'drivetrain': 'front',
    'country': 'germany',
    'condition': 'used',
    'upholstery_color': 'black',
    'emission_class': 4,
    'year': 1900
}

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H2('Car Specifications & Location'),

    html.Label('Brand'),
    dcc.Dropdown(
        id='make-dropdown',
        options=[{'label': brand, 'value': brand} for brand in brands],
        value=default_values['brand'],
        placeholder="Select a brand"
    ),
    html.Br(),

    html.Label('Model'),
    dcc.Dropdown(
        id='model-dropdown',
        options=[{'label': model, 'value': model} for model in models],
        value=default_values['model'],
        placeholder="Select a model"
    ),
    html.Br(),

    html.Label('Fuel Type'),
    dcc.Dropdown(
        id='fuel-type-dropdown',
        options=[{'label': fuel_type, 'value': fuel_type} for fuel_type in fuel_types],
        value=default_values['fuel_type'],
        placeholder="Select a fuel type"
    ),
    html.Br(),

    html.Label('Gearbox'),
    dcc.Dropdown(
        id='gearbox-dropdown',
        options=[{'label': gearbox, 'value': gearbox} for gearbox in gearboxes],
        value=default_values['gearbox'],
        placeholder="Select a gearbox type"
    ),
    html.Br(),

    html.Label('Color'),
    dcc.Dropdown(
        id='color-dropdown',
        options=[{'label': color, 'value': color} for color in colors],
        value=default_values['color'],
        placeholder="Select a color"
    ),
    html.Br(),

    html.Label('Seller'),
    dcc.Dropdown(
        id='seller-dropdown',
        options=[{'label': seller, 'value': seller} for seller in sellers],
        value=default_values['seller'],
        placeholder="Select a seller type"
    ),
    html.Br(),

    html.Label('Body Type'),
    dcc.Dropdown(
        id='body-type-dropdown',
        options=[{'label': body_type, 'value': body_type} for body_type in body_types],
        value=default_values['body_type'],
        placeholder="Select a body type"
    ),
    html.Br(),

    html.Label('Drivetrain'),
    dcc.Dropdown(
        id='drivetrain-dropdown',
        options=[{'label': drivetrain, 'value': drivetrain} for drivetrain in drivetrains],
        value=default_values['drivetrain'],
        placeholder="Select a drivetrain"
    ),
    html.Br(),

    html.Label('Country'),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in countries],
        value=default_values['country'],
        placeholder="Select a country"
    ),
    html.Br(),

    html.Label('Condition'),
    dcc.Dropdown(
        id='condition-dropdown',
        options=[{'label': condition, 'value': condition} for condition in conditions],
        value=default_values['condition'],
        placeholder="Select a condition"
    ),
    html.Br(),

    html.Label('Upholstery Color'),
    dcc.Dropdown(
        id='upholstery-color-dropdown',
        options=[{'label': upholstery_color, 'value': upholstery_color} for upholstery_color in upholstery_colors],
        value=default_values['upholstery_color'],
        placeholder="Select an upholstery color"
    ),
    html.Br(),

    html.H2('Car Specifications (Numerical)'),
    html.Label('Mileage'),
    dcc.Input(id='mileage-input', type='number', value=default_values['mileage'], placeholder="Enter mileage"),
    html.Br(),
    html.Label('Power'),
    dcc.Input(id='power-input', type='number', value=default_values['power'], placeholder="Enter power"),
    html.Br(),
    html.Label('Engine Size'),
    dcc.Input(id='engine-size-input', type='number', value=default_values['engine_size'], placeholder="Enter engine size"),
    html.Br(),
    html.Label('Doors'),
    dcc.Input(id='doors-input', type='number', value=default_values['doors'], placeholder="Enter number of doors"),
    html.Br(),
    html.Label('Seats'),
    dcc.Input(id='seats-input', type='number', value=default_values['seats'], placeholder="Enter number of seats"),
    html.Br(),
    html.Label('Emission Class'),
    dcc.Input(id='emission-class-input', type='number', value=default_values['emission_class'], placeholder="Enter emission class"),
    html.Br(),
    html.Label('Year'),
    dcc.Input(id='year-input', type='number', value=default_values['year'], placeholder="Enter year"),
    html.Br(),

    html.Button('Predict Price', id='predict-button', n_clicks=0, style={'marginTop': '20px'}),
    html.Div(id='output-container', style={'marginTop': '20px', 'padding': '20px', 'border': '1px solid #ccc', 'borderRadius': '5px', 'backgroundColor': '#f9f9f9'})
])

# Callback to handle user inputs and filter the dataset
@app.callback(
    Output('output-container', 'children'),
    Input('predict-button', 'n_clicks'),
    State('make-dropdown', 'value'),
    State('model-dropdown', 'value'),
    State('fuel-type-dropdown', 'value'),
    State('gearbox-dropdown', 'value'),
    State('color-dropdown', 'value'),
    State('seller-dropdown', 'value'),
    State('body-type-dropdown', 'value'),
    State('drivetrain-dropdown', 'value'),
    State('country-dropdown', 'value'),
    State('condition-dropdown', 'value'),
    State('upholstery-color-dropdown', 'value'),
    State('mileage-input', 'value'),
    State('power-input', 'value'),
    State('engine-size-input', 'value'),
    State('doors-input', 'value'),
    State('seats-input', 'value'),
    State('emission-class-input', 'value'),
    State('year-input', 'value')
)
def update_output(n_clicks, make, model, fuel_type, gearbox, color, seller, body_type, drivetrain, country, condition, upholstery_color,
                  mileage, power, engine_size, doors, seats, emission_class, year):
    if n_clicks == 0:
        return ''

    # Collect inputs into a dictionary, ensuring that each selection is considered
    input_data = {
        'brand': make,
        'model': model,
        'fuel_type': fuel_type,
        'gearbox': gearbox,
        'color': color,
        'seller': seller,
        'body_type': body_type,
        'drivetrain': drivetrain,
        'country': country,
        'condition': condition,
        'upholstery_color': upholstery_color,
        'mileage': mileage,
        'power': power,
        'engine_size': engine_size,
        'doors': doors,
        'seats': seats,
        'emission_class': emission_class,
        'year': year
    }

    # Convert the input data to a DataFrame
    input_df = pd.DataFrame([input_data])

    # Ensure the model's feature columns match the input DataFrame
    input_df = pd.get_dummies(input_df).reindex(columns=feature_names, fill_value=0)

    # Predict with the model
    prediction = xgb_model.predict(input_df)[0]

    # Display the prediction result
    return html.Div([
        html.H4('Predicted Value'),
        html.P(f'The predicted value is: {prediction:.2f} €')
    ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
