from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
#from flask_login import LoginManager, login_required, login_user, current_user, logout_user
#from flask_cors import CORS

import os
import psycopg2
import psycopg2.extras
import config
import json
import time
import urllib.request
import base64
import ssl
#import jinja2
#from .views.dash import view

app = Flask(__name__, static_url_path='/static'  )
#CORS(app, resources={r"*":{"origins":"*"}})
#app.register_blueprint(view)
app.config["APPLICATION_ROOT"]=config.application_root
app.debug=config.debug
app.secret_key=config.appkey


if config.usemin:
    config.usemin=".min"
else:
    config.usemin=""

env={"navigation":config.navigation,
     "hosts": config.hosts,
     "usemin": config.usemin,
     "deeplinks": config.deeplinks,
     }


@app.route("/" )
def index():
    response = Response ( render_template('clusters.html', environment=env) )
    #response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:15432/cluster/'
    return response


def buildRequest(url, request):
    method = request.method
    payload = "{}"
    try:
        payload = json.dumps( request.json )
    except:
        pass
    payload = payload.encode('utf-8')
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Content-Length', len(payload))
    req.add_header('Authorization', request.environ.get('HTTP_AUTHORIZATION') )
    req.method = method

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE    # FIX ME  ## TODO
    print (payload)
    try:
        ret =  urllib.request.urlopen( req, payload, context=ctx )
    except Exception as e:
        #print( "-----"  )
        #print( e.code   )
        #print( e.read() )
        try:
            return Response(e.read(), mimetype='application/json', status=e.code)
        except Exception as e2:
            return Response(json.dumps({ "stderr" : "UNRECOVERABLE ERROR", "msg" : str(e) }) , mimetype='application/json', status=500)
    return Response(ret.read(), mimetype='application/json')


@app.route("/pgapi/proxy/<host>", methods=['POST','GET','PATCH', 'PUT','DELETE'] )
def pgapi_proxy(host):
    print(host)
    return  buildRequest(
                    'https://'+host+'/pgapi/cluster', 
                    request
                    )

@app.route("/pgapi/proxy/<host>/<version>/<cluster>", methods=['POST','GET','PATCH','PUT','DELETE'] )
def pgapi_proxy_cluster(host,version,cluster):
    print (host, version, cluster)
    return buildRequest(
                    'https://'+host+'/pgapi/cluster/'+version+'/'+cluster, 
                    request
                    )


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

