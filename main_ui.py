import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import pickle

# Load the dataset
df = pd.read_csv('cleaned_cars.csv')

# Load the model from disk
filename = 'xgbr_price_predictor.pkl'
with open(filename, 'rb') as file:
    xgb_model = pickle.load(file)

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

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H2('Car Specifications & Location'),

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

    html.Label('Fuel Type'),
    dcc.Dropdown(
        id='fuel-type-dropdown',
        options=[{'label': fuel_type, 'value': fuel_type} for fuel_type in fuel_types],
        placeholder="Select a fuel type"
    ),
    html.Br(),

    html.Label('Gearbox'),
    dcc.Dropdown(
        id='gearbox-dropdown',
        options=[{'label': gearbox, 'value': gearbox} for gearbox in gearboxes],
        placeholder="Select a gearbox type"
    ),
    html.Br(),

    html.Label('Color'),
    dcc.Dropdown(
        id='color-dropdown',
        options=[{'label': color, 'value': color} for color in colors],
        placeholder="Select a color"
    ),
    html.Br(),

    html.Label('Seller'),
    dcc.Dropdown(
        id='seller-dropdown',
        options=[{'label': seller, 'value': seller} for seller in sellers],
        placeholder="Select a seller type"
    ),
    html.Br(),

    html.Label('Body Type'),
    dcc.Dropdown(
        id='body-type-dropdown',
        options=[{'label': body_type, 'value': body_type} for body_type in body_types],
        placeholder="Select a body type"
    ),
    html.Br(),

    html.Label('Drivetrain'),
    dcc.Dropdown(
        id='drivetrain-dropdown',
        options=[{'label': drivetrain, 'value': drivetrain} for drivetrain in drivetrains],
        placeholder="Select a drivetrain"
    ),
    html.Br(),

    html.Label('Country'),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in countries],
        placeholder="Select a country"
    ),
    html.Br(),

    html.Label('Condition'),
    dcc.Dropdown(
        id='condition-dropdown',
        options=[{'label': condition, 'value': condition} for condition in conditions],
        placeholder="Select a condition"
    ),
    html.Br(),

    html.Label('Upholstery Color'),
    dcc.Dropdown(
        id='upholstery-color-dropdown',
        options=[{'label': upholstery_color, 'value': upholstery_color} for upholstery_color in upholstery_colors],
        placeholder="Select an upholstery color"
    ),
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
    State('upholstery-color-dropdown', 'value')
)
def update_output(n_clicks, make, model, fuel_type, gearbox, color, seller, body_type, drivetrain, country, condition, upholstery_color):
    if n_clicks == 0:
        return ''

    # Collect inputs into a dictionary
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
        'upholstery_color': upholstery_color
    }

    # Convert the input data to a DataFrame
    input_df = pd.DataFrame([input_data])

    # Ensure the model's feature columns match the input DataFrame
    feature_columns = xgb_model.get_booster().feature_names
    input_df = input_df.reindex(columns=feature_columns)

    # One-hot encode categorical columns
    input_df = pd.get_dummies(input_df).reindex(columns=feature_columns, fill_value=0)

    # Predict with the model
    prediction = xgb_model.predict(input_df)[0]

    # Display the input data and the prediction result
    return html.Div([
        html.H4('Model Prediction'),
        html.Table([
            html.Tr([html.Th('Field'), html.Th('Value')])] +
            [html.Tr([html.Td(k), html.Td(v if v is not None else '-')]) for k, v in input_data.items()]
        ),
        html.Br(),
        html.Div([
            html.H4('Predicted Value'),
            html.P(f'The predicted value is: {prediction:.2f} €')
        ], style={'backgroundColor': '#e8f4f8', 'padding': '10px', 'borderRadius': '5px', 'textAlign': 'center'})
    ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
