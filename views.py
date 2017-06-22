

from flask import render_template
from flask import request

import json
import os
import random

import numpy as np
import pandas as pd
import plotly

from . import app, model


model = model.Model()


@app.route('/')
@app.route('/index')
def index():
    unit = request.args.get('unit')
    index = request.args.get('i')
    unit = 'R001' if unit is None else unit
    index = 1 if index is None else index
    model.update(unit)
    details = model.details.values.tolist()
    details.sort(key=lambda x: x[1])
    color = model.get_color(unit)
    affected = condense_affected_data()
    logo_file = get_random_logo()

    graphs = build_graphs()
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           unit=unit,
                           index=index,
                           details=details,
                           logo_file=logo_file,
                           data=model.station_data,
                           affected=affected,
                           color=color,
                           ids=ids,
                           graphJSON=graphJSON)


def get_random_logo():
    print(os.getcwd())
    files = list(filter(lambda x: x.endswith('png'),
                        os.listdir('switchyard/static/images')))
    return random.choice(files)


def condense_affected_data():
    details = []
    for station in model.affected_station_data:
        # station contains two dataframes, one for before and after shock
        unit = station.name
        unit_details = model.details[model.details.unit == unit]
        name = unit_details['station'].iloc[0]
        line = unit_details['line'].iloc[0]
        color = unit_details['color'].iloc[0]
        details.append((name, line, color, station))
    return details


def build_graphs():
    rng = pd.date_range('1/1/2011', periods=7500, freq='H')
    ts = pd.Series(np.random.randn(len(rng)), index=rng)
    ts = np.abs(ts)

    return [
        dict(
            data=[
                dict(
                    x=[1, 2, 3],
                    y=[10, 20, 30],
                    type='scatter'
                ),
            ],
            layout=dict(
                title='first graph'
            )
        ),

        dict(
            data=[
                dict(
                    x=[1, 3, 5],
                    y=[10, 50, 30],
                    type='bar'
                ),
            ],
            layout=dict(
                title='second graph'
            )
        ),

        dict(
            data=[
                dict(
                    x=ts.index,  # Can use the pandas data structures directly
                    y=ts,
                    line=dict(
                        color=('rgb(30,105,10)'),
                        width=2
                    )
                )
            ],
            layout=dict(
                title='test time series graph'
            )
        )
    ]


@app.route('/about')
def about():
    return render_template('about.html')
