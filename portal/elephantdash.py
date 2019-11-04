import os
import psycopg2
import psycopg2.extras
import config
import json
import time
import urllib.request
import base64
import ssl

from collections import deque
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response


app = Flask(__name__, static_url_path='/static'  )

app.config["APPLICATION_ROOT"]=config.application_root
app.debug=config.debug
app.secret_key=config.appkey


if config.usemin:
    config.usemin=".min"
else:
    config.usemin=""

env={"navigation":config.navigation,
     "usemin": config.usemin,
     "deeplinks": config.deeplinks,
     "detailview_cluster" : config.detailview_clusterinformation,
     "detailview_system" : config.detailview_systeminformation, 
     "version": config.version,
     "disabled_features": config.disabled_features
     }

logged_actions = deque([], 5)

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
    return response


@app.route("/log" )
def log():
    return jsonify( [ action for action in logged_actions ] )

@app.route("/host_list/" )
def host_list():
    return jsonify( get_hostlist() )

@app.route("/host_init/", methods=['GET'] )
def host_init():
    hostaddress = request.args.get('hostaddress')
    clusteraddress = request.args.get('clusteraddress')
    if clusteraddress != '':
        
        host_add(clusteraddress)
        r= buildRequest(
                    'https://'+clusteraddress+'/portal/host_list/',
                    request, raw=True
                    )
        r= json.load( r )
        print(r)
        for i in r:
            print(i)
            host_add(i['address'], False)
    host_add(hostaddress)
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
    try:
        ret =  urllib.request.urlopen( req, payload, context=ctx )
    except Exception as e:
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
    logged_actions.append( 'Pushed something to %s'%(host) )    
    return  buildRequest(
                    'https://'+host+'/pgapi/cluster', 
                    request
                    )
    
@app.route("/pgapi/proxy/system/<host>", methods=['POST','GET','PATCH', 'PUT','DELETE'] )
def pgapi_proxy_system(host):
    print(host)
    logged_actions.append( 'Pushed something to %s'%(host) )    
    return  buildRequest(
                    'https://'+host+'/pgapi/system', 
                    request
                    )


@app.route("/pgapi/proxy/backup/<host>", methods=['POST','GET','PATCH', 'PUT','DELETE'] )
@app.route("/pgapi/proxy/backup/<host>/<stanza>", methods=['POST', 'GET', 'PATCH', 'PUT', 'DELETE'])
@app.route("/pgapi/proxy/backup/<host>/<stanza>/<backup_id>", methods=['POST', 'GET', 'PATCH', 'PUT', 'DELETE'])
def pgapi_proxy_backup(host, stanza='', backup_id=''):
    stanza = '/' + stanza if stanza != '' else '';
    if backup_id:
        stanza += '/'+backup_id
    logged_actions.append( 'Pushed something to %s'%(host) )    
    return  buildRequest(
                    'https://'+host+'/pgapi/backup'+stanza, 
                    request
                    )

@app.route("/pgapi/proxy/backup_activity/<host>", methods=['POST','GET','PATCH', 'PUT','DELETE'] )
def pgapi_proxy_backupactivity(host):
    logged_actions.append( 'Pushed something to %s'%(host) )    
    return  buildRequest(
                    'https://'+host+'/pgapi/backup_activity/',
                    request
                    )

@app.route("/pgapi/proxy/cluster/<host>/<version>/<cluster>", methods=['POST','GET','PATCH','PUT','DELETE'] )
def pgapi_proxy_cluster(host,version,cluster):
    logged_actions.append( 'Pushed something to %s'%(host) )    
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
    return jsonify( output )



@app.route("/state")
def state():
    time.sleep(2)
    return jsonify( hosts )

