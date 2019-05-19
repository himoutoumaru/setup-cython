import json
from sklearn import svm
from flask import Flask
import psutil
import numpy as np
from sklearn import datasets

app = Flask(__name__)


@app.route('/')
def hello_world():
    iris = datasets.load_iris()
    digits = datasets.load_digits()
    clf = svm.SVC(gamma=0.001, C=100.)
    clf.fit(digits.data[:-1], digits.target[:-1])

    arr = np.array([1, 2, 3])
    return json.dumps(dict(cpu=str(psutil.cpu_freq()), np=arr.mean(), sci=str(clf.predict(digits.data[:-1]))))
