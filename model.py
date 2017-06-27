

import os

import pandas as pd


class Model:
    def __init__(self):
        print(os.getcwd())
        self.data_directory = 'switchyard/static/data'
        self.ridership = pd.read_csv(
            f'{self.data_directory}/ridership_since_dec.csv')
        self.ridership.set_index('date', inplace=True)
        self.ridership.columns = self.ridership.columns.str.upper()
        self.ratios = pd.read_csv(
            f'{self.data_directory}/ratio_sas.csv')
        self.ratios.set_index('unit', inplace=True)
        self.details = (pd.read_csv(
            f'{self.data_directory}/line_station_color_details.csv')
            .set_index('unit'))
        self.station_data = None
        self.affected_station_data = None

    def update(self, unit):
        self.station_data = self.get_main_station(unit)
        self.affected_station_data = self.get_most_affected(unit)

    def get_main_station(self, unit):
        return self.ridership.iloc[-60:, unit]

    def get_affected_station(self, unit, delta):
        print(delta)
        riders = self.ridership[unit]
        pre = riders.loc[:'2017-04-30']
        post = riders.loc['2017-05-01':].add(
            delta, fill_value=1)
        riders = pd.concat([pre, post], axis=0)
        return riders

    def get_most_affected(self, unit, number=6):
        ''' get the top `number` stations based on total ridership change at
            that station following closure of station `unit`
        '''
        effect = self.ratios[unit]
        mean_riders = self.ridership[unit].mean()
        delta = -effect * mean_riders
        return delta.sort_values().iloc[:number]

    def get_color(self, unit):
        sub_details = self.details[self.details.unit == unit]
        return sub_details['color'].iloc[0]
