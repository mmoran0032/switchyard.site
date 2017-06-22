

from flask import render_template
from flask import request

import json
import os
import random

import numpy as np
import plotly

from . import app, model


model = model.Model()


@app.route('/')
@app.route('/index')
def index():
    unit = request.args.get('unit')
    index = request.args.get('i')
    unit = 'R248' if unit is None else unit
    index = 1 if index is None else index
    logo_file = get_random_logo()
    details = sorted([(u, *d) for u, d in
                      zip(model.details.index, model.details.values)],
                     key=lambda x: x[1])
    test_units = [unit, *np.random.choice(
        model.details.index.values, size=6, replace=False)]
    graphs = build_graphs(test_units)
    ids = [f'graph-{i}' for i, _ in enumerate(graphs)]
    names = [create_name_string(u) for u in test_units]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           unit=unit,
                           index=index,
                           logo_file=logo_file,
                           details=details,
                           ids=ids,
                           names=json.dumps(names),
                           graphJSON=graphJSON)


def get_random_logo():
    files = list(filter(lambda x: x.endswith('png'),
                        os.listdir('switchyard_site/static/images')))
    return random.choice(files)


def build_graphs(units):
    graphs = [create_single_graph(u) for u in units]
    return graphs


def create_single_graph(unit):
    color = model.details.loc[unit, 'color']
    x = model.ridership.index
    y = model.ridership[unit]
    marker = dict(color=color)
    data = [dict(x=x, y=y, type='bar', marker=marker)]
    layout = dict(margin=dict(l=50, r=50, b=50, t=50, pad=4))
    return dict(data=data, layout=layout)


def create_name_string(unit):
    station = model.details.loc[unit, 'station']
    line = model.details.loc[unit, 'line']
    return f'{station} | {line}'


@app.route('/about')
def about():
    return render_template('about.html')
