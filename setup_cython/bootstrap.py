import json
from flask import Flask
import psutil
import numpy as np
from sklearn import linear_model

app = Flask(__name__)


@app.route('/')
def hello_world():
    x = [x for x in range(100)]
    reg = linear_model.LinearRegression()
    reg.fit([[0, 0], [1, 1], [2, 2]], [0, 1, 2])
    arr = np.array([1, 2, 3])
    return json.dumps(dict(cpu=str(psutil.cpu_freq()), np=arr.mean(), sci=str(reg.coef_)))
