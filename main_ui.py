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
    
def classify_emission(value):
    if value < 0 or value > 2370:
        return "Invalid emission value"
    
    if value <= 500:
        return "Euro 1"
    elif value <= 1000:
        return "Euro 2"
    elif value <= 1500:
        return "Euro 3"
    elif value <= 2000:
        return "Euro 4"
    elif value <= 2250:
        return "Euro 5"
    else:
        return "Euro 6"

# Function to generate the AutoScout24 URL
def generate_autoscout24_url(brand, model, car_type, **filters):

    # protect all value
    brand = brand.replace(' ', '-')
    model = model.replace(' ', '-')
    car_type = car_type.replace(' ', '-')
    filters = {key: str(value).replace(' ', '-') for key, value in filters.items()}

    # protect all value from /
    brand = brand.replace('/', '%2F')
    model = model.replace('/', '%2F')
    car_type = car_type.replace('/', '%2F')
    filters = {key: str(value).replace('/', '%2F') for key, value in filters.items()}

    base_url = f"https://www.autoscout24.com/lst/{brand}/{model}/ot_{car_type}"

    # Start building the URL
    url = base_url + "?"

    # Add filters to the URL
    for key, value in filters.items():
        url += f"{key}={value}&"

    # Remove the trailing '&'
    url = url.rstrip('&')

    return url

# Mapping dictionaries for filters
body_type_map = {
    'compact': '1',
    'convertible': '2',
    'coupe': '3',
    'offroad-truck': '4',
    'station-wagon': '5',
    'sedans': '6',
    'van': '12',
    'transporters': '13',
    'other': '7'
}

fuel_type_map = {
    'gazoline': 'B',
    'diesel': 'D',
    'electric': 'E',
    'ethanol': 'M',
    'hydrogen': 'H',
    'lpg': 'L',
    'cng': 'C',
    'electric/gasoline': '2',
    'other': 'O',
    'electric/diesel': '3'
}

gearbox_map = {
    'automatic': 'A',
    'manual': 'M',
    'semi-automatic': 'S'
}

seller_map = {
    'dealer': 'D',
    'private seller': 'P'
}

emission_class_map = {
    'Euro 1': '1',
    'Euro 2': '2',
    'Euro 3': '3',
    'Euro 4': '4',
    'Euro 5': '5',
    'Euro 6': '6',
    'Euro 6b': '11',
    'Euro 6c': '7',
    'Euro 6d': '8',
    'Euro 6d-temp': '9',
    'Euro 6e': '10'
}


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
    dbc.themes.YETI,
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
            margin-bottom: 5px;
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
        .slider-container {
            padding-left: 50px;
            margin-top: 20px; /* Add margin-top to increase distance between input and slider */
        }
        .predict-btn {
            font-size: 1.5em;
            padding: 0.75em 1.5em;
        }
        .price-text {
            font-size: 1.5em;
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
def create_dropdown(label, id, options, placeholder, width='md-1'):
    return dbc.Col([
        html.Label(label, className='form-label'),
        dcc.Dropdown(id=id, options=options, placeholder=placeholder, persistence=True, persistence_type='local')
    ], className=width)

current_year = datetime.now().year

app.layout = dbc.Container([
    dcc.Store(id='store-dropdown-values'),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='/assets/app_logo/logo.png', height='100px', className='mx-auto d-block mb-3'),
                html.H1('CarPricePredictor', className='text-center mb-1'),
                html.P('Use this application to predict the price of your car based on various specifications and features.', className='text-center mb-4')
            ], className='text-center')
        ], width=12)
    ]),
    dbc.Row([dbc.Col(dbc.Alert(id='alert', style={'display': 'none'}), width=12)]),
    dbc.Row([dbc.Col(html.H2('Specifications : ', className='text-left mb-4'), width=12)]),
    dbc.Row([
        create_dropdown('Brand', 'make-dropdown', create_brand_options(dropdown_options['brand']), "Select a brand"),
        create_dropdown('Model', 'model-dropdown', [], "Select a model"),
        create_dropdown('Fuel Type', 'fuel-type-dropdown', [{'label': option, 'value': option} for option in dropdown_options['fuel_type']], "Select a fuel type"),
        create_dropdown('Gearbox', 'gearbox-dropdown', [{'label': option, 'value': option} for option in dropdown_options['gearbox']], "Select a gearbox type"),
    ], className='mb-1'),
    dbc.Row([
        create_dropdown('Body Type', 'body-type-dropdown', create_body_type_options(dropdown_options['body_type']), "Select a body type"),
        create_dropdown('Color', 'color-dropdown', [{'label': option, 'value': option} for option in dropdown_options['color']], "Select a color", width='md-2'),
        create_dropdown('Seller', 'seller-dropdown', [{'label': option, 'value': option} for option in dropdown_options['seller']], "Select a seller type"),
        create_dropdown('Drivetrain', 'drivetrain-dropdown', [{'label': option, 'value': option} for option in dropdown_options['drivetrain']], "Select a drivetrain"),
    ], className='mb-1'),
    dbc.Row([
        create_dropdown('Country', 'country-dropdown', create_country_options(dropdown_options['country']), "Select a country"),
        create_dropdown('Condition', 'condition-dropdown', [{'label': option, 'value': option} for option in dropdown_options['condition']], "Select a condition"),
        create_dropdown('Upholstery Color', 'upholstery-color-dropdown', [{'label': option, 'value': option} for option in dropdown_options['upholstery_color']], "Select an upholstery color", width='md-2')
    ], className='mb-1'),
    dbc.Row([dbc.Col(html.H2('Specifications (Numerical) :', className='text-left mb-4'), width=12)]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Label('Mileage (km)', className='form-label input-text'),
                dbc.Input(id='mileage-input-hidden', type='number', value=0, style={'display': 'none'}),
                dbc.Input(id='mileage-input-visible', type='text', value='0 km', style={'margin-bottom': '20px'}),

                html.Div([
                    dcc.Slider(
                        id='mileage-slider',
                        min=0,
                        max=500000,
                        step=0,
                        value=0,
                        marks={i: f'{i // 1000} km' for i in range(0, 500001, 50000)},
                        className='slider',
                        tooltip={'always_visible': True}
                    )
                ], style={'margin-top': '40px'})
            ], className='input-slider-container')
        ], md=4),
        dbc.Col([
            html.Div([
                dbc.Label('Power (kw)', className='form-label input-text'),
                dbc.Input(id='power-input', type='number', placeholder="Enter power", value=0,min=0, max=2000, style={'margin-bottom': '20px'}),
                html.Div([
                    dcc.Slider(
                        id='power-slider',
                        min=0,
                        max=2000,
                        step=10,
                        value=0,
                        marks={i: str(i) for i in range(0, 2001, 500)},
                        className='slider',
                        tooltip={'always_visible': True}
                    )
                ], style={'margin-top': '40px'})
            ], className='input-slider-container')
        ], md=4),
        dbc.Col([
            html.Div([
                dbc.Label('Engine Size', className='form-label input-text'),
                dbc.Input(id='engine-size-input', type='number', placeholder="Enter engine size", value=0, min=0, max=2000, style={'margin-bottom': '20px'}),
                html.Div([
                    dcc.Slider(
                        id='engine-size-slider',
                        min=0,
                        max=2000,
                        step=10,
                        value=0,
                        marks={i: str(i) for i in range(0, 2001, 400)},
                        className='slider',
                        tooltip={'always_visible': True}
                    )
                ], style={'margin-top': '40px'})
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
        ], md=3),
        dbc.Col([
            dbc.Label('Seats', className='form-label'),
            dbc.RadioItems(
                id='seats-input',
                options=[{'label': str(i), 'value': i} for i in range(1, 13)],
                inline=True
            )
        ], md=3),
        dbc.Col([
            html.Div([
                dbc.Label('Year', className='form-label input-text'),
                dbc.Input(id='year-input', type='number', placeholder="Enter year", value=current_year, style={'margin-bottom': '20px'}),
                html.Div([
                    dcc.Slider(
                        id='year-slider',
                        min=1800,
                        max=current_year,
                        step=1,
                        value=current_year,
                        marks={i: str(i) for i in range(1800, current_year + 1, 50)},
                        className='slider',
                        tooltip={'always_visible': True}
                    )
                ], style={'margin-top': '40px'})
            ], className='input-slider-container')
        ], md=3),
        dbc.Col([
            html.Div([
                html.Div([
                    dbc.Label('Emission Class', id='emission-class-label', className='form-label input-text'),
                ], className='d-flex align-items-center'),
                html.Div([
                    dbc.Input(id='emission-class-input', type='number', placeholder="Enter emission class", min=0, value=0, max=2370),
                ], className='d-flex align-items-center'),
                html.Div([
                    dcc.Slider(
                        id='emission-class-slider',
                        min=0,
                        max=2370,
                        step=1,
                        value=0,
                        marks={i: str(i) for i in range(0, 2371, 500)},
                        className='slider',
                        tooltip={'always_visible': True}
                    )
                ], style={'margin-top': '40px'}),
            ], className='input-slider-container')
        ], md=3)
    ], className='mb-3'),
    dbc.Row([dbc.Col(html.Button('Predict Price', id='predict-button', n_clicks=0, className='btn btn-primary mt-3 predict-btn'), className='d-grid gap-2 d-md-flex justify-content-md-center')]),
    dbc.Row([dbc.Col(html.Div(id='output-container', className='mt-4 p-4 border rounded bg-light'), width=12)])
], fluid=True)

# Callback to update model dropdown based on selected brand
@app.callback(
    Output('model-dropdown', 'options'),
    [Input('make-dropdown', 'value')]
)
def set_model_options(selected_brand):
    if selected_brand is None:
        return []
    filtered_models = df[df['brand'] == selected_brand]['model'].unique()
    return [{'label': model, 'value': model} for model in filtered_models]

# Callback to synchronize input and slider for mileage
@app.callback(
    Output('mileage-input-hidden', 'value'),
    Output('mileage-slider', 'value'),
    Output('mileage-input-visible', 'value'),
    Input('mileage-input-hidden', 'value'),
    Input('mileage-slider', 'value')
)
def sync_mileage(mileage_input, mileage_slider):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if input_id == 'mileage-input-hidden':
        formatted_value = f"{mileage_input:,} km"
        return mileage_input, mileage_input, formatted_value
    else:
        formatted_value = f"{mileage_slider:,} km"
        return mileage_slider, mileage_slider, formatted_value

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
    Output('emission-class-label', 'children'),
    Input('emission-class-input', 'value'),
    Input('emission-class-slider', 'value')
)
def sync_emission_class(emission_class_input, emission_class_slider):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if input_id == 'emission-class-input':
        emission_class = classify_emission(emission_class_input)
        label_text = f"Emission Class - {emission_class}"
        return emission_class_input, emission_class_input, label_text
    else:
        emission_class = classify_emission(emission_class_slider)
        label_text = f"Emission Class - {emission_class}"
        return emission_class_slider, emission_class_slider, label_text

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
    Output('alert', 'style'),
    Output('alert', 'color'),
    Output('alert', 'children'),
    Output('output-container', 'children'),
    Input('predict-button', 'n_clicks'),
    State('store-dropdown-values', 'data'),
    State('mileage-input-hidden', 'value'),
    State('power-input', 'value'),
    State('engine-size-input', 'value'),
    State('doors-input', 'value'),
    State('seats-input', 'value'),
    State('emission-class-input', 'value'),
    State('year-input', 'value'),
)
def update_output(n_clicks, stored_values, mileage, power, engine_size, doors, seats, emission_class, year):
    if n_clicks == 0:
        return {'display': 'none'}, '', '', ''  # Added an extra '' for alert.color

    input_data = dict(zip(
        ['brand', 'model', 'fuel_type', 'gearbox', 'color', 'seller', 'body_type', 'drivetrain', 'country', 'condition', 'upholstery_color', 'mileage', 'power', 'engine_size', 'doors', 'seats', 'emission_class', 'year'],
        [stored_values.get(f'dropdown-{i}') for i in range(11)] + [mileage, power, engine_size, doors, seats, emission_class, year]
    ))

    # Check if all required fields are filled
    required_fields = ['brand', 'model', 'fuel_type', 'gearbox', 'color', 'seller', 'body_type', 'drivetrain', 'country', 'condition', 'upholstery_color']
    missing_fields = [field for field in required_fields if input_data.get(field) is None]

    if missing_fields:
        return {'display': 'block'}, 'danger', html.Div([
            html.H4('Missing Fields', className='alert-heading text-center'),
            html.P(f'The following fields are required: {", ".join(missing_fields)}', className='text-center'),
        ]), ''

    
    # doors
    # 2/3 &doorfrom=2&doorto=3
    # 4/5 &doorfrom=4&doorto=5
    # 6/7 &doorfrom=6&doorto=7
    # doors can be just like that so do class
    if doors == 2 or doors == 3:
        doorform = 2
        doorto = 3
    elif doors == 4 or doors == 5:
        doorform = 4
        doorto = 5
    else:
        doorform = 6
        doorto = 7

    # Remove keys with None values (optional fields not provided by the user)
    input_data = {k: v for k, v in input_data.items() if v is not None}

    # Map the input data to the corresponding URL parameters
    filters = {
        'body': body_type_map.get(input_data.get('body_type')),
        'fuel': fuel_type_map.get(input_data.get('fuel_type')),
        'gear': gearbox_map.get(input_data.get('gearbox')),
        'custtype': seller_map.get(input_data.get('seller')),
        'emclass': emission_class_map.get(classify_emission(input_data.get('emission_class'))),
        'kmfrom': input_data.get('mileage'),
        'kmto': input_data.get('mileage'),
        'powerfrom': input_data.get('power'),
        'powertype': 'kw',
        'doorfrom': doorform,
        'doorto': doorto,
        'seatsfrom': input_data.get('seats'),
        'fregfrom': input_data.get('year'),
        'fregto': input_data.get('year'),
        'cy': input_data.get('country'),
    }

    # Clean filters from None values
    filters = {k: v for k, v in filters.items() if v is not None}
    print(fuel_type_map.get(input_data.get('fuel_type')))
    #print(filters)

    # Generate the AutoScout24 URL
    try:
        search_url = generate_autoscout24_url(
            brand=input_data.get('brand'),
            model=input_data.get('model'),
            car_type=input_data.get('condition'),
            **filters
        )
    except ValueError as e:
        return {'display': 'block'}, html.Div([
            html.H4('Error', className='text-center text-danger'),
            html.P(str(e), className='text-center text-danger'),
        ]), ''

    input_df = pd.DataFrame([input_data])
    input_df = pd.get_dummies(input_df).reindex(columns=feature_names, fill_value=0)

    prediction = xgb_model.predict(input_df)[0]
    prediction_text = f'The predicted value is: {prediction:.2f} €'
        

    return {'display': 'block'}, 'success', html.Div([
        html.H4('Predicted Value', className='text-center mb-3'),
        html.P(html.B(prediction_text), className='text-center price-text mb-3'),
        html.P('Url to find the cars available with these specifications on the AutoScout24 website:', className='text-center price-text mb-3'),
        html.A(html.B('Click here to go to Autoscout24.com'), href=search_url, target='_blank', className='d-block text-center alert-link mb-3'),
    ]), html.Div([
        html.H4('Predicted Value', className='text-center mb-3'),
        html.P(html.B(prediction_text), className='text-center price-text mb-3')
    ])


# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
