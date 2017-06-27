

import pandas as pd


class Model:
    def __init__(self):
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
        return self.ridership[unit].iloc[-60:]

    def get_most_affected(self, unit, number=6):
        ''' get the top `number` stations based on total ridership change at
            that station following closure of station `unit`
        '''
        effect = self.ratios[unit]
        mean_riders = self.ridership[unit].mean()
        delta = -effect * mean_riders
        return delta.sort_values().iloc[:number]

    def get_color(self, unit):
        sub_details = self.details.loc[unit]
        return sub_details['color'].iloc[0]
