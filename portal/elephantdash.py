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
     #"hosts": config.hosts,
     "usemin": config.usemin,
     "deeplinks": config.deeplinks,
     "detailview_cluster" : config.detailview_clusterinformation,
     "detailview_system" : config.detailview_systeminformation, 
     }


def get_hostlist():
    h_list = []
    try:
        with open(config.hostlist, 'r') as f:
            for line in f:
                #print(line)
                line = line.strip()
                if line != '':
                    h_list.append({'address': line}) 
    except:
        pass
    return h_list

def write_hostlist(hostlist):
    with open(config.hostlist, 'w') as f:
        for line in hostlist:
            f.write(line['address']+'\n')
            


@app.route("/" )
def index():
    env['hosts'] = get_hostlist()
    response = Response ( render_template('clusters.html', environment=env) )
    #response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:15432/cluster/'
    return response

@app.route("/host_list/" )
def host_list():
    return jsonify( get_hostlist() )

@app.route("/host_init/<string:hostname>/<string:clustername>" )
def host_init(hostname,clustername):
    
    if clustername != '':
        
        host_add(clustername)
        r= buildRequest(
                    'https://'+clustername+'/portal/host_list/',
                    request, raw=True
                    )
        r= json.load( r )
        print(r)
        for i in r:
            print(i)
            host_add(i['address'], False)
    host_add(hostname)
    return 'OK'
                    
@app.route("/host_add/<string:hostname>" )
def host_add(hostname, distribute=True):
    currentlist= get_hostlist()
    for host in currentlist:
        if host['address'] == hostname:
            return 'OK'
    write_hostlist(currentlist + [{'address':hostname},])
    if not distribute:
        return 'OK'
    for host in currentlist:
        buildRequest(
                    'https://'+host['address']+'/portal/host_add/'+hostname ,
                    request
                    )
    return 'OK'

@app.route("/host_del/<string:hostname>" )
def host_del(hostname):
    currentlist = get_hostlist()
    exists=False
    for line in currentlist:
        if line['address'] == hostname:
            exists = True
    if not exists:
        return 'OK'
    write_hostlist([line for line in currentlist if line['address'] != hostname])
    for host in get_hostlist():
        buildRequest(
                    'https://'+host['address']+'/portal/host_del/'+hostname ,
                    request
                    )
    return 'OK'



@app.route("/error" )
def error():
    response = Response ( render_template('error.html', environment=env) )
    return response

def buildRequest(url, request, raw=False):
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
            if raw:
                return e
            return Response(e.read(), mimetype='application/json', status=e.code)
        except Exception as e2:
            if raw:
                return 'ERROR'
            return Response(json.dumps({"stderr": "UNRECOVERABLE ERROR", "msg": str(e)}), mimetype='application/json', status=500)
    if raw:
        return ret
    return Response(ret.read(), mimetype='application/json', status=ret.code)


@app.route("/pgapi/proxy/cluster/<host>", methods=['POST','GET','PATCH', 'PUT','DELETE'] )
def pgapi_proxy(host):
    print(host)
    return  buildRequest(
                    'https://'+host+'/pgapi/cluster', 
                    request
                    )
@app.route("/pgapi/proxy/system/<host>", methods=['POST','GET','PATCH', 'PUT','DELETE'] )
def pgapi_proxy_system(host):
    print(host)
    return  buildRequest(
                    'https://'+host+'/pgapi/system', 
                    request
                    )



@app.route("/pgapi/proxy/cluster/<host>/<version>/<cluster>", methods=['POST','GET','PATCH','PUT','DELETE'] )
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

@app.route("/pg_settings/<version>")
def pgsettings(version):
    settingsfolder = os.path.join( os.path.dirname(__file__),'static','pg_settings' )
    if version+'.csv' in os.listdir( settingsfolder ):
        import csv
        output = {}
        with open( os.path.join( settingsfolder, version+'.csv' ) ) as csvfile:
            reader = csv.DictReader( csvfile )
            for row in reader:
                output[row['name']]=row
                #output[row['name']]= {}
                #for fieldname in reader.fieldnames:
                #    output[row['name']][fieldname]=row[fieldname]
    return jsonify( output )



@app.route("/state")
def state():
    time.sleep(2)
    #response = app.response_class(
    #        response=json.dumps(hosts),
    #        mimetype='application/json'
    #        )
    #return response
    return jsonify( hosts )

