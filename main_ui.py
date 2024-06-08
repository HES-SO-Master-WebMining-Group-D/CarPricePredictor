import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import pickle
import dash_bootstrap_components as dbc
from datetime import datetime

# Function to load files
def load_pickle_file(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

# Load the dataset and necessary files
df = pd.read_csv('cleaned_cars.csv')
xgb_model = load_pickle_file('xgbr_price_predictor.pkl')
feature_names = load_pickle_file('feature_names.pkl')

# Extract unique values for dropdown options and sort them alphabetically
def get_unique_values(df, column):
    return sorted(df[column].unique()) if column in df.columns else []

dropdown_options = {
    'brand': get_unique_values(df, 'brand'),
    'model': get_unique_values(df, 'model'),
    'fuel_type': get_unique_values(df, 'fuel_type'),
    'gearbox': get_unique_values(df, 'gearbox'),
    'color': get_unique_values(df, 'color'),
    'seller': get_unique_values(df, 'seller'),
    'body_type': get_unique_values(df, 'body_type'),
    'drivetrain': get_unique_values(df, 'drivetrain'),
    'country': get_unique_values(df, 'country'),
    'condition': get_unique_values(df, 'condition'),
    'upholstery_color': get_unique_values(df, 'upholstery_color')
}

# Initialize the Dash app with a custom Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.SKETCHY,
    'https://use.fontawesome.com/releases/v5.9.0/css/all.css'
])

# CSS
app.index_string = '''
<!DOCTYPE html>
<html>
<head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <style>
        .brand-logo, .country-flag, .body-type-logo {
            width: 30px;
            margin-right: 10px;
        }
        .broken-image {
            display: none;
        }
        .input-slider-container {
            margin-bottom: 15px;
        }
        .input-text {
            margin-bottom: 10px;
        }
        .slider {
            padding-left: 50px;
        }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
'''

def create_brand_options(brands):
    return [{'label': html.Span([html.Img(src=f'/assets/brand_logo/{brand.replace(" ", "")}.png', className='brand-logo'), brand]), 'value': brand} for brand in brands]

def create_country_options(countries):
    return [{'label': html.Span([html.Img(src=f'/assets/flag/{country.replace(" ", "")}.png', className='country-flag'), country]), 'value': country} for country in countries]

def create_body_type_options(body_types):
    return [{'label': html.Span([html.Img(src=f'/assets/body_type/{body_type.replace(" ", "")}.png', className='body-type-logo'), body_type]), 'value': body_type} for body_type in body_types]

# Define the layout of the app
def create_dropdown(label, id, options, placeholder, width='md-4'):
    return dbc.Col([
        html.Label(label, className='form-label'),
        dcc.Dropdown(id=id, options=options, placeholder=placeholder, persistence=True, persistence_type='local')
    ], className=width)

current_year = datetime.now().year

app.layout = dbc.Container([
    dcc.Store(id='store-dropdown-values'),
    dbc.Row([dbc.Col(html.H2('Car Specifications & Location', className='text-center mb-4'), width=12)]),
    dbc.Row([
        create_dropdown('Brand', 'make-dropdown', create_brand_options(dropdown_options['brand']), "Select a brand"),
        create_dropdown('Model', 'model-dropdown', [{'label': option, 'value': option} for option in dropdown_options['model']], "Select a model"),
        create_dropdown('Fuel Type', 'fuel-type-dropdown', [{'label': option, 'value': option} for option in dropdown_options['fuel_type']], "Select a fuel type")
    ], className='mb-3'),
    dbc.Row([
        create_dropdown('Gearbox', 'gearbox-dropdown', [{'label': option, 'value': option} for option in dropdown_options['gearbox']], "Select a gearbox type"),
        create_dropdown('Color', 'color-dropdown', [{'label': option, 'value': option} for option in dropdown_options['color']], "Select a color", width='md-2'),
        create_dropdown('Seller', 'seller-dropdown', [{'label': option, 'value': option} for option in dropdown_options['seller']], "Select a seller type")
    ], className='mb-3'),
    dbc.Row([
        create_dropdown('Body Type', 'body-type-dropdown', create_body_type_options(dropdown_options['body_type']), "Select a body type"),
        create_dropdown('Drivetrain', 'drivetrain-dropdown', [{'label': option, 'value': option} for option in dropdown_options['drivetrain']], "Select a drivetrain"),
        create_dropdown('Country', 'country-dropdown', create_country_options(dropdown_options['country']), "Select a country")
    ], className='mb-3'),
    dbc.Row([
        create_dropdown('Condition', 'condition-dropdown', [{'label': option, 'value': option} for option in dropdown_options['condition']], "Select a condition"),
        create_dropdown('Upholstery Color', 'upholstery-color-dropdown', [{'label': option, 'value': option} for option in dropdown_options['upholstery_color']], "Select an upholstery color", width='md-2')
    ], className='mb-3'),
    dbc.Row([dbc.Col(html.H2('Car Specifications (Numerical)', className='text-center mb-4'), width=12)]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Label('Mileage', className='form-label input-text'),
                dbc.Input(id='mileage-input', type='number', placeholder="Enter mileage"),
                dcc.Slider(
                    id='mileage-slider',
                    min=0,
                    max=9999999,
                    step=1000,
                    value=50000,
                    marks={i: f'{i // 1000}k' for i in range(0, 10000001, 1000000)},
                    className='slider',
                    tooltip={'always_visible': True}
                )
            ], className='input-slider-container')
        ], md=4),
        dbc.Col([
            html.Div([
                dbc.Label('Power', className='form-label input-text'),
                dbc.Input(id='power-input', type='number', placeholder="Enter power", min=0, max=2000),
                dcc.Slider(
                    id='power-slider',
                    min=0,
                    max=2000,
                    step=10,
                    value=1000,
                    marks={i: str(i) for i in range(0, 2001, 500)},
                    className='slider',
                    tooltip={'always_visible': True}
                )
            ], className='input-slider-container')
        ], md=4),
        dbc.Col([
            html.Div([
                dbc.Label('Engine Size', className='form-label input-text'),
                dbc.Input(id='engine-size-input', type='number', placeholder="Enter engine size", min=0, max=2000),
                dcc.Slider(
                    id='engine-size-slider',
                    min=0,
                    max=2000,
                    step=0.1,
                    value=1000,
                    marks={i: str(i) for i in range(0, 2001, 100)},
                    className='slider',
                    tooltip={'always_visible': True}
                )
            ], className='input-slider-container')
        ], md=4)
    ], className='mb-3'),
    dbc.Row([
        dbc.Col([
            dbc.Label('Doors', className='form-label'),
            dbc.RadioItems(
                id='doors-input',
                options=[{'label': str(i), 'value': i} for i in range(2, 8)],
                inline=True
            )
        ], md=4),
    ], className='mb-3'),
    dbc.Row([
        dbc.Col([
            dbc.Label('Seats', className='form-label'),
            dbc.RadioItems(
                id='seats-input',
                options=[{'label': str(i), 'value': i} for i in range(1, 13)],
                inline=True
            )
        ], md=4),
    ], className='mb-3'),
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Label('Year', className='form-label input-text'),
                dbc.Input(id='year-input', type='number', placeholder="Enter year", value=current_year),
                dcc.Slider(
                    id='year-slider',
                    min=1900,
                    max=current_year,
                    step=1,
                    value=current_year,
                    marks={i: str(i) for i in range(1900, current_year + 1, 10)},
                    className='slider',
                    tooltip={'always_visible': True}
                )
            ], className='input-slider-container')
        ], md=4)
    ], className='mb-3'),
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Label('Emission Class', className='form-label input-text'),
                dbc.Input(id='emission-class-input', type='number', placeholder="Enter emission class", min=0, max=2000, style={'width': '100%'}),
                dcc.Slider(
                    id='emission-class-slider',
                    min=0,
                    max=2000,
                    step=1,
                    value=1000,
                    marks={i: str(i) for i in range(0, 2001, 100)},
                    className='slider',
                    tooltip={'always_visible': True}
                )
            ], className='input-slider-container')
        ], md=4)
    ], className='mb-3'),
    dbc.Row([dbc.Col(html.Button('Predict Price', id='predict-button', n_clicks=0, className='btn btn-primary mt-3'), className='d-grid gap-2 d-md-flex justify-content-md-center')]),
    dbc.Row([dbc.Col(html.Div(id='output-container', className='mt-4 p-4 border rounded bg-light'), width=12)])
], fluid=True)

# Callback to synchronize input and slider for mileage
@app.callback(
    Output('mileage-input', 'value'),
    Output('mileage-slider', 'value'),
    Input('mileage-input', 'value'),
    Input('mileage-slider', 'value')
)
def sync_mileage(mileage_input, mileage_slider):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if input_id == 'mileage-input':
        return mileage_input, mileage_input
    else:
        return mileage_slider, mileage_slider

# Callback to synchronize input and slider for power
@app.callback(
    Output('power-input', 'value'),
    Output('power-slider', 'value'),
    Input('power-input', 'value'),
    Input('power-slider', 'value')
)
def sync_power(power_input, power_slider):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if input_id == 'power-input':
        return power_input, power_input
    else:
        return power_slider, power_slider

# Callback to synchronize input and slider for engine size
@app.callback(
    Output('engine-size-input', 'value'),
    Output('engine-size-slider', 'value'),
    Input('engine-size-input', 'value'),
    Input('engine-size-slider', 'value')
)
def sync_engine_size(engine_size_input, engine_size_slider):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if input_id == 'engine-size-input':
        return engine_size_input, engine_size_input
    else:
        return engine_size_slider, engine_size_slider

# Callback to synchronize input and slider for year
@app.callback(
    Output('year-input', 'value'),
    Output('year-slider', 'value'),
    Input('year-input', 'value'),
    Input('year-slider', 'value')
)
def sync_year(year_input, year_slider):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if input_id == 'year-input':
        return year_input, year_input
    else:
        return year_slider, year_slider

# Callback to synchronize input and slider for emission class
@app.callback(
    Output('emission-class-input', 'value'),
    Output('emission-class-slider', 'value'),
    Input('emission-class-input', 'value'),
    Input('emission-class-slider', 'value')
)
def sync_emission_class(emission_class_input, emission_class_slider):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if input_id == 'emission-class-input':
        return emission_class_input, emission_class_input
    else:
        return emission_class_slider, emission_class_slider

# Callback to save the state of dropdown values
@app.callback(
    Output('store-dropdown-values', 'data'),
    Input('make-dropdown', 'value'),
    Input('model-dropdown', 'value'),
    Input('fuel-type-dropdown', 'value'),
    Input('gearbox-dropdown', 'value'),
    Input('color-dropdown', 'value'),
    Input('seller-dropdown', 'value'),
    Input('body-type-dropdown', 'value'),
    Input('drivetrain-dropdown', 'value'),
    Input('country-dropdown', 'value'),
    Input('condition-dropdown', 'value'),
    Input('upholstery-color-dropdown', 'value'),
)
def store_dropdown_values(*values):
    return {f'dropdown-{i}': value for i, value in enumerate(values)}

# Callback to handle user inputs and predict the car price
@app.callback(
    Output('output-container', 'children'),
    Input('predict-button', 'n_clicks'),
    State('store-dropdown-values', 'data'),
    State('mileage-input', 'value'),
    State('power-input', 'value'),
    State('engine-size-input', 'value'),
    State('doors-input', 'value'),
    State('seats-input', 'value'),
    State('emission-class-input', 'value'),
    State('year-input', 'value'),
)
def update_output(n_clicks, stored_values, mileage, power, engine_size, doors, seats, emission_class, year):
    if n_clicks == 0:
        return ''

    input_data = dict(zip(
        ['brand', 'model', 'fuel_type', 'gearbox', 'color', 'seller', 'body_type', 'drivetrain', 'country', 'condition', 'upholstery_color', 'mileage', 'power', 'engine_size', 'doors', 'seats', 'emission_class', 'year'],
        [stored_values.get(f'dropdown-{i}') for i in range(11)] + [mileage, power, engine_size, doors, seats, emission_class, year]
    ))

    # Check if all required fields are filled
    required_fields = ['brand', 'model', 'fuel_type', 'gearbox', 'color', 'seller', 'body_type', 'drivetrain', 'country', 'condition', 'upholstery_color']
    missing_fields = [field for field in required_fields if input_data.get(field) is None]

    if missing_fields:
        return html.Div([
            html.H4('Missing Fields', className='text-center text-danger'),
            html.P(f'The following fields are required: {", ".join(missing_fields)}', className='text-center text-danger'),
        ])

    # Remove keys with None values (optional fields not provided by the user)
    input_data = {k: v for k, v in input_data.items() if v is not None}
    input_df = pd.DataFrame([input_data])
    input_df = pd.get_dummies(input_df).reindex(columns=feature_names, fill_value=0)

    prediction = xgb_model.predict(input_df)[0]

    return html.Div([
        html.H4('Predicted Value', className='text-center'),
        html.P(f'The predicted value is: {prediction:.2f} €', className='text-center')
    ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
