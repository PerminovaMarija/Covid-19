import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime
import os


class Stat:
    def __init__(self):
        self.api_url = 'http://covid19.soficoop.com/country/RS'
        self.get_api_data()

    def get_api_data(self):
        response = requests.get(self.api_url)
        data = json.loads(response.text)

        all_cases = {}
        all_today_cases = {}
        all_deaths = {}
        all_today_deaths = {}
        all_recovered = {}
        all_active = {}
        all_critical = {}

        for item in data['snapshots']:
            converted_date = datetime.strftime(datetime.strptime(item['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                                               '%d.%m.%Y')

            all_cases[converted_date] = item['cases']
            all_today_cases[converted_date] = item['todayCases']
            all_deaths[converted_date] = item['deaths']
            all_today_deaths[converted_date] = item['todayDeaths']
            all_recovered[converted_date] = item['recovered']
            all_active[converted_date] = item['active']
            all_critical[converted_date] = item['critical']

        df = pd.DataFrame({'data': list(all_cases.keys()), 'cases': list(all_cases.values()),
                           'todayCases': list(all_today_cases.values()), 'deaths': list(all_deaths.values()),
                           'todayDeaths': list(all_today_deaths.values()), 'recovered': list(all_recovered.values()),
                           'active': list(all_active.values()), 'critical': list(all_critical.values())})

        df['pand_index'] = round((df['deaths'] + df['recovered']) / df['cases'] * 100, 2)
        df['mortality'] = round((df['deaths'] / (df['deaths'] + df['recovered']) * 100), 2)
        df.to_excel(os.path.join(os.getcwd(), 'covid_graph.xls'), index=False)

        df.plot(x='data', y=['cases', 'deaths', 'recovered'])
        plt.show()


if __name__ == "__main__":
    Stat()
