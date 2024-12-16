import numpy as np
import plotly.graph_objs as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import scipy.signal


def harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    t = np.linspace(0, 2 * np.pi, 1000)
    harmonic_signal = amplitude * np.sin(frequency * t + phase)
    noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), len(t))

    if show_noise:
        signal_with_noise = harmonic_signal + noise
    else:
        signal_with_noise = harmonic_signal

    return t, harmonic_signal, signal_with_noise


def filter(sig, fs, wn):
    b, a = scipy.signal.iirfilter(2, Wn=wn, fs=fs, btype="low", ftype="butter")
    return scipy.signal.filtfilt(b, a, sig)


app = Dash(__name__)


param_tooltip = {"placement": "bottom", "always_visible": True}

initial_params = {
    'amplitude': 1.0,
    'frequency': 5.0,
    'phase': 0.0,
    'noise_mean': 0.0,
    'noise_covariance': 0.1,
    'show_noise': True,
    'fs': 50,
    'wn': 2.5
}

app.layout = html.Div([
    html.H1('Harmonic signal with noise',
            style={'textAlign': 'center', 'fontSize': '18px', 'marginBottom': '0px'}),

    dcc.Graph(id='harmonic-plot', style={'height': '50vh', 'marginTop': '0px'}),

    html.Div([
        html.Label('Amplitude:'),
        dcc.Slider(id='amplitude-slider', min=0, max=10, marks=None, value=initial_params['amplitude'],
                   tooltip=param_tooltip),
        html.Label('Frequency:'),
        dcc.Slider(id='frequency-slider', min=0.1, max=10, marks=None, value=initial_params['frequency'],
                   tooltip=param_tooltip),
        html.Label('Phase:'),
        dcc.Slider(id='phase-slider', min=0, max=2 * np.pi, marks=None, value=initial_params['phase'],
                   tooltip=param_tooltip),
        html.Label('Noise mean:'),
        dcc.Slider(id='noise-mean-slider', min=-2, max=2, marks=None, value=initial_params['noise_mean'],
                   tooltip=param_tooltip),
        html.Label('Noise dispersion:'),
        dcc.Slider(id='noise-covariance-slider', min=0, max=1, marks=None, value=initial_params['noise_covariance'],
                   tooltip=param_tooltip),
        html.Label('Fs:'),
        dcc.Slider(id='fs-slider', min=1, max=1000, marks=None, value=initial_params['fs'],
                    tooltip=param_tooltip),
        html.Label('Wn:'),
        dcc.Slider(id='wn-slider', min=1, max=5, marks=None, value=initial_params['wn'],
                    tooltip=param_tooltip)
    ], style={'margin': '0px'}),

    html.Div([
        dcc.Checklist(
            id='show-noise-checkbox',
            options=[{'label': 'Show noise', 'value': 'show_noise'}],
            value=['show_noise'] if initial_params['show_noise'] else []
        )
    ], style={'margin': '0px'}),

    html.Div([
        html.Button('Reset', id='reset-button', n_clicks=0)
    ], style={'margin': '0px', 'textAlign': 'center'})
])

@app.callback(
    Output('harmonic-plot', 'figure'),
    [
        Input('amplitude-slider', 'value'),
        Input('frequency-slider', 'value'),
        Input('phase-slider', 'value'),
        Input('noise-mean-slider', 'value'),
        Input('noise-covariance-slider', 'value'),
        Input('show-noise-checkbox', 'value'),
        Input('fs-slider', 'value'),
        Input('wn-slider', 'value')
    ]
)
def update_graph(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise, fs, wn):
    t, harmonic_signal, signal_with_noise = harmonic_with_noise(
        amplitude, frequency, phase, noise_mean, noise_covariance,
        show_noise='show_noise' in show_noise
    )
    fi = filter(harmonic_signal, fs, wn)
    plot_data = [
        go.Scatter(x=t, y=harmonic_signal, mode='lines'),
        go.Scatter(x=t, y=fi, mode='lines')
    ]
    if 'show_noise' in show_noise:
        plot_data.append(go.Scatter(x=t, y=signal_with_noise, mode='lines'))

    figure = {
        'data': plot_data,
        'layout': go.Layout(
            xaxis={'title': 'Time'},
            yaxis={'title': 'Amplitude'},
            hovermode='closest'
        )
    }
    return figure

@app.callback(
    [
        Output('amplitude-slider', 'value'),
        Output('frequency-slider', 'value'),
        Output('phase-slider', 'value'),
        Output('noise-mean-slider', 'value'),
        Output('noise-covariance-slider', 'value'),
        Output('show-noise-checkbox', 'value'),
        Output('fs-slider', 'value'),
        Output('wn-slider', 'value')
    ],
    [Input('reset-button', 'n_clicks')],
    prevent_initial_call=True
)
def reset_values(n_clicks):
    return (
        initial_params['amplitude'],
        initial_params['frequency'],
        initial_params['phase'],
        initial_params['noise_mean'],
        initial_params['noise_covariance'],
        ['show_noise'] if initial_params['show_noise'] else [],
        initial_params['fs'],
        initial_params['wn']
    )


if __name__ == '__main__':
    app.run_server(debug=True)
