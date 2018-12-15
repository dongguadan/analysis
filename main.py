#!/usr/bin/python3

from flask import Flask,jsonify,render_template
import json
import os
import requests
import _thread
import numpy as np
import folium
from folium.plugins import HeatMap
from lib.items import *
from lib.cities import *

app = Flask(__name__, template_folder="./", static_folder="./build")

distributions = {}

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/getData',methods=['GET','POST'])
def test_post():
    result = ProcessAnalysis()
    return json.dumps(result,ensure_ascii=False)

def ProcessAnalysis():
    addresses = []
    total = []
    for key in distributions:
        print("key：%s value: %s"%(key,distributions[key]))
        addresses.append(key)
        total.append(distributions[key])
    addrInfo = getid(addresses)
    lon = np.array([i["lng"] for i in addrInfo],dtype=float)
    lat = np.array([i["lat"] for i in addrInfo],dtype=float)
    data = [[lat[i], lon[i], total[i]] for i in range(len(addrInfo))]
    map_osm = folium.Map(location=[35,110],zoom_start=5)
    HeatMap(data).add_to(map_osm)
    file_path = r"人口.html"
    map_osm.save(file_path)
    return data

def getid(addresses):
    url = "http://api.map.baidu.com/geocoder/v2/"
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
    payload = {
    'output':'json',
    'ak':'X8zlxPUdSe2weshrZ1WqnWxb43cfBI2N'
    }
    addinfo = []
    for address in addresses:
        payload['address'] = address
        try:
            content =  requests.get(url,params=payload,headers=header).json()
            addinfo.append(content['result']['location'])
        except:
            print("地址{}获取失败，请稍后重试！".format(address))
            addinfo.append({"lng":0, "lat":0})
    return(addinfo)

def Craw():
    identifies_json = get_cities_json()
    aid = '97137413'
    url = 'https://music.163.com/weapi/user/getfolloweds?csrf_token=cdee144903c5a32e6752f50180329fc9'
    page = 1
    while page:
        offset = (page-1) * 20
        strOffset = str(offset)
        id_msg = '{userId: "' + aid + '", offset: "' + strOffset + '"' + ', total: "true", limit: "20", csrf_token: "cdee144903c5a32e6752f50180329fc9"}'
        #print("%s" % id_msg)
        params, encSecKey = get_params(id_msg)
        data = {'params': params, 'encSecKey': encSecKey}
        html = get_fans_json(url, data)
        if html is None:
            break
        else:
            for item in get_items(html):
                #print("{}\n".format(item))
                if item["location"] in identifies_json:
                #    print("%d:%s" % (item["location"], identifies_json[item["location"]]))
                    if identifies_json[item["location"]] in distributions:
                        distributions[identifies_json[item["location"]]] += 1
                    else:
                        distributions[identifies_json[item["location"]]] = 1
        page += 1

if __name__ == '__main__':
    try:
       _thread.start_new_thread(Craw, ())
    except:
       print("Error: unable to start thread")
    app.run(host='0.0.0.0', port=8000, debug=False)