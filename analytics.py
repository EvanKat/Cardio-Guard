# Import packages
from dash import Dash, html, dcc, Input, Output, State, callback, no_update, clientside_callback, dash_table
from plotly_resampler import FigureResampler, FigureWidgetResampler
import dash_bootstrap_components as dbc
import logging
import numpy as np
import json
from packages.dash_package import default_values as def_val
from packages.dash_package import util_fun_dash as util_dash


import plotly.graph_objs as go

class File_name:
    def __init__(self):
        self.name = None
        self.rate = None
        self.type = None
        self.date = None
        self.time = None        

file_class = File_name()

# TODO: Impliment and plot activity and anomaly index
# TODO: Plot pioncare and Power plots
# TODO: Button to download HRV data
# TODO: Button to download all data

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Analiytics Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([ 
            html.Div([
                html.Label('Select File:'),
                html.Button('Scan', id='scan_button', n_clicks=3)
            ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between'}),
            dcc.Dropdown(id='available_devices')
        ], width=3),

        dbc.Col([
            html.Label('Type: Rate: Date: Starting Time: ', id = 'type_text_id', style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'height': '50%'}),
        ], width=3, style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}),

        dbc.Col([ html.Div([
                html.Button('Display Analitycs', id='display_analitycs_button', n_clicks=0)
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'height': '50%'})], width=3),

    ], style={ 'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between'}),
    dbc.Row([
        dbc.Col(dcc.Graph(id = "hr_graph"), width=4),
        dbc.Col(dcc.Graph(id = "rr_dist_graph"), width=4),
        # dbc.Col(dcc.Graph(id = "hr_graph"), width=4),
        dbc.Col(dcc.Graph(id = "edr_graph"), width=4)
    ], style={ 'display': 'flex', 'align-items': 'center', 'justify-items': 'center', 'margin-top': '0'}),
    html.Hr(),
    dbc.Row([
        html.H4('Arrhythmias', id='arr_text_display', style={'text-align': 'center'}),
        html.Div(id = 'arr_type_txt_fig', style = {'margin-top': '0'}),
    ], style={ 'margin-top': '0'}),
    
    html.Hr(),

    dbc.Row([
        dbc.Col([
            html.H4('HRV Characteristics', id='hrv_text_display', style={'text-align': 'center'}),
            html.Br(),
            html.Div(id = 'display_hrv')
        ], width=5)
    ],style={ 'margin-top': '0'}),

], fluid=True)


@app.callback(
    [Output('hr_graph', 'figure'),                      # 1 hr_graph 
    Output('rr_dist_graph', 'figure'),                  # 2 rr_dist_graph
    Output('edr_graph', 'figure'),                      # 3 edr_graph
    Output('arr_type_txt_fig', 'children'),             # 4 arr_Type_text_display
    Output('display_hrv', 'children')                   # 5 hrv_tables
    ],
    Input('display_analitycs_button', 'n_clicks'),
    prevent_initial_call=True
)
def calculate_analytics_and_save(n_clicks):
    if n_clicks:
        value = file_class.name
        
        # load ecg data
        file_path = f'{def_val.CLEAN_PATH}{value}'
        data_clean = util_dash.load_pickle_data(file_path)
        
        # Set time domain
        time_domain = np.arange(0, ( len(data_clean['data']) / data_clean['rate'] ), 1/ data_clean['rate'] )
        
        # Load intervals
        file_path = f'{def_val.INTERVALS_PATH}{value}'
        data_intervals = util_dash.load_pickle_data(file_path)
        
        # Get hr figure  
        fig_hr = util_dash.figure_hr(time_domain, data_intervals['hr_data'], rate = data_intervals['rate'])
        
        # Get rr density figure  
        fig_rr_dest = util_dash.figure_density_rr(data_intervals['rri_data'], data_intervals['hr_data'])

        # Load edr data
        file_path = f'{def_val.EDR_PATH}{value}'
        data_edr = util_dash.load_pickle_data(file_path)
        # print(data_edr.keys)
        # Get edr figure  
        # Resampled
        fig_edr = util_dash.figure_edr(time_domain, data_edr['edr_rate'], rate = data_edr['rate'])

        # Load hrv data
        file_path = f'{def_val.HRV_PATH}{value}'
        data_hrv = util_dash.load_pickle_data(file_path)

        # Check if data exists
        child_hrv = []
        if data_hrv['indices']:
            domains_len = len(data_hrv['indices'])
            child_width = (100 / domains_len) - 1

            for idx in range(domains_len):
                # type of hrv domain
                if data_hrv['values'][idx] == 'time_domain':
                    label_txt = 'Time Domain'
                elif data_hrv['values'][idx] == 'freq_domain':
                    label_txt = 'Frequency Domain'
                else:
                    label_txt = 'Non-linear Domain'
            
                children_hrv = html.Div([
                                    html.Label(f'{label_txt}'),
                                    html.Br(),
                                    dash_table.DataTable(
                                        data=[data_hrv['indices'][idx]],
                                        columns=[{"name": i, "id": i} for i in data_hrv['indices'][idx].keys()],
                                        style_table={'overflowX': 'auto'},
                                    ),
                                ], style={'width': f'{child_width}%', 'display': 'inline-block', 'overflowX': 'auto'}),
                
                child_hrv.append(children_hrv[0])

        else:
            msg = f'No HRV Found'
            child_hrv = [html.Div(msg, style={'text-align': 'center'})]


        # Load arrhytmias data
        file_path = f'{def_val.HRV_ARRYTHMIAS_PATH}{value}'
        data_arr = util_dash.load_pickle_data(file_path)
        # get arrhythmia_indices
        arrhythmia_indices = util_dash.adjusted_arrhythmia_indices(data_arr['predictions'],data_intervals['rpeaks_indices'])

        # calcutale no of arrythmias
        if arrhythmia_indices and len(arrhythmia_indices.values()) > 0:

            number_of_arrh = len(arrhythmia_indices.values())

            fig_arr = util_dash.figure_arrythmias(data_clean['data'], time_domain, data_intervals['rpeaks_indices'], arrhythmia_indices)
            
            msg = ', '.join([f'{key}: {len(values)}' for key, values in arrhythmia_indices.items()])
            
            # graph = dcc.Graph(figure=fig_arr)
            graph = dcc.Graph(figure=fig_arr)

            child = [html.Div(msg, style={'text-align': 'center'}), html.Br(), graph]
        else:
            msg = f'No Arrhythmias Found'
            child = [html.Div(msg, style={'text-align': 'center'})]
        
        # hrv_table
        
        return fig_hr, fig_rr_dest, fig_edr, child, child_hrv
    else:
        no_update

# To set up visual info 
@app.callback(
    Output('type_text_id', 'children'),
    Input('available_devices', 'value'),
    prevent_initial_call=True
)
def scan_for_files(value):

    data = value.split('_')
    text = f'Type: {data[0]}\t  Rate: {data[3]}\t  Date: {data[1]}\t  Starting Time: {data[2]}'
    
    file_class.name = value
    file_class.rate = data[3]
    file_class.type = data[0]
    file_class.date = data[1]
    file_class.time = data[2]
    
    return text


# To scan for row files
@app.callback(
    Output('available_devices', 'options'),
    Input('scan_button', 'n_clicks'),
    prevent_initial_call=True
)
def scan_for_files(n_clicks):
    if n_clicks:
        file_names = util_dash.scan_for_csv_files(def_val.RAW_PATH)
        return file_names
    else:
        return no_update


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)