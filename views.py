

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
    logo_file = get_random_logo()
    details = sorted([(u, *d) for u, d in
                      zip(model.details.index, model.details.values)],
                     key=lambda x: x[1])

    graphs = build_graphs()
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           unit=unit,
                           index=index,
                           logo_file=logo_file,
                           ids=ids,
                           details=details,
                           graphJSON=graphJSON)


def get_random_logo():
    print(os.getcwd())
    files = list(filter(lambda x: x.endswith('png'),
                        os.listdir('switchyard_site/static/images')))
    return random.choice(files)


def build_graphs():
    rng = pd.date_range('1/1/2011', periods=7500, freq='H')
    ts = pd.Series(np.random.randn(len(rng)), index=rng)
    ts = np.abs(ts)

    graphs = [
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
                    type='bar',
                    marker=dict(
                        color=('rgb(30,145,20)')
                    )
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
                    type='bar',
                    marker=dict(
                        color=('rgb(145,20,30)')
                    )
                )
            ]
        )
    ]
    return graphs


def create_single_graph(unit):
    color = model.details.loc[unit, 'color']
    x = model.ridership.index
    y = model.ridership[unit]
    type = 'bar'
    marker = dict(color=(color))
    data = dict(x=x, y=y, type=type, marker=marker)
    return dict(data=data)


@app.route('/about')
def about():
    return render_template('about.html')
