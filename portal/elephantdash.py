from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
#from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from flask_cors import CORS
import os
import psycopg2
import psycopg2.extras
import config
import json
import time
#import jinja2
#from .views.dash import view

app = Flask(__name__, static_url_path='/static'  )
CORS(app, resources={r"*":{"origins":"*"}})
#app.register_blueprint(view)

app.debug=config.debug
app.secret_key=config.appkey


if config.usemin:
    config.usemin=".min"
else:
    config.usemin=""

env={"navigation":config.navigation,
     "hosts": config.hosts,
     "usemin": config.usemin }


@app.route("/" )
def index():
    response = Response ( render_template('clusters.html', environment=env) )
    #response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:15432/cluster/'
    return response

@app.route("/detail/<host>")
def details_host(host):
    return render_template('detail.html', environment=env, detail_host=host)
@app.route("/detail/<host>/<version>/<cluster>")
def details_cluster(host, version, cluster):
    return render_template('detail.html', environment=env, detail_host=host, detail_version=version, detail_cluster=cluster)



@app.route("/state")
def state():
    time.sleep(2)
    #response = app.response_class(
    #        response=json.dumps(hosts),
    #        mimetype='application/json'
    #        )
    #return response
    return jsonify( hosts )

