# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

@app.route("/")
def Index():
    return render_template("index.html")

@app.route("/_update")
def _update():
    data = json.dumps(request.args)
    print data
    return ""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8083, debug=True)
