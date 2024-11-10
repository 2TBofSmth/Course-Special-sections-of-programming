from spyre import server
import pandas as pd
from functions import *
import seaborn as sns
import matplotlib.pyplot as plt


class DVapp(server.App):
    title = 'NOAA Data Visualisation'

    inputs = [{'type': 'dropdown',
               'label': 'Metric',
               'options': [{'label': 'VCI', 'value': 'VCI'},
                           {'label': 'TCI', 'value': 'TCI'},
                           {'label': 'VHI', 'value': 'VHI'}],
               'key': 'metric',
               'action_id': 'simple_html_output'},

              {'type': 'dropdown',
               'label': 'Area',
               'options': [{'label': 'Vinnytsia r.', 'value': '1'},
                           {'label': 'Volyn r.', 'value': '2'},
                           {'label': 'Dnipro r.', 'value': '3'},
                           {'label': 'Donetsk r.', 'value': '4'},
                           {'label': 'Zhytomyr r.', 'value': '5'},
                           {'label': 'Zakarpattia r.', 'value': '6'},
                           {'label': 'Zaporizhzhia r.', 'value': '7'},
                           {'label': 'Ivano-Frankivsk r.', 'value': '8'},
                           {'label': 'Kyiv r.', 'value': '9'},
                           {'label': 'Kirovohrad r.', 'value': '10'},
                           {'label': 'Luhansk r.', 'value': '11'},
                           {'label': 'Lviv r.', 'value': '12'},
                           {'label': 'Mykolaiv r.', 'value': '13'},
                           {'label': 'Odesa r.', 'value': '14'},
                           {'label': 'Poltava r.', 'value': '15'},
                           {'label': 'Rivne r.', 'value': '16'},
                           {'label': 'Sumy r.', 'value': '17'},
                           {'label': 'Ternopil r.', 'value': '18'},
                           {'label': 'Kharkiv r.', 'value': '19'},
                           {'label': 'Kherson r.', 'value': '20'},
                           {'label': 'Khmelnytshyi r.', 'value': '21'},
                           {'label': 'Cherkasy r.', 'value': '22'},
                           {'label': 'Chernivtsi r.', 'value': '23'},
                           {'label': 'Chernihiv r.', 'value': '24'},
                           {'label': 'AR Crimea', 'value': '25'},
                           {'label': 'Kyiv c.', 'value': '26'},
                           {'label': 'Sevastopol c.', 'value': '27'}],
               'key': 'area_index',
               'action_id': 'simple_html_output'},
              
              {
                  'type': 'text',
                  'key': 'range_years',
                  'label': 'Range of years',
                  'value': '1982-2024',
                  'action_id': 'simple_html_output'
              }]

    outputs = [
        {
            'type': 'plot',
            'id': 'getPlot',
            'control_id': 'update_data',
            'tab': 'Plot',
            'on_page_load': True},
        {
            'type': 'table',
            'id': 'getData',
            'control_id': 'update_data',
            'tab': 'Table',
            'on_page_load': True
        }
    ]

    tabs = ['Table', 'Plot']

    controls = [
        {
            'type': 'button',
            'id': 'update_data',
            'label': 'Show data'
        }]

    def __init__(self):
        check_folder('../tt/data')
        for i in range(1, 28):
            download_data(i)
        self.df = pd.concat([create_df(i, replacements[find_province_id(i)]) for i in get_paths('../tt/data')])

    def getData(self, params):
        filtered_df = self.df[(self.df['area'] == int(params['area_index'])) &
                              (self.df['Year'].isin(self.parseRange(params['range_years'])))]

        return filtered_df[['Year', 'Week', params['metric']]]

    def getPlot(self, params):
        filtered_df = self.df[(self.df['area'] == int(params['area_index'])) &
                              (self.df['Year'].isin(self.parseRange(params['range_years'])))]
        filtered_df['Y-M'] = self.df['Year'].astype(str) + '.' + self.df['Week'].astype(str)
        ax = sns.lineplot(x='Year', y=params['metric'], data=filtered_df)
        return ax.get_figure()

    def parseRange(self, r):
        start, end = map(int, r.split('-'))
        return range(start, end + 1)


app = DVapp()
app.launch()
