#!/usr/bin/python3

from flask import Flask,jsonify,render_template
import json
import os
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
    result = {}
    result["max"] = 8
    result["data"] = "null"
    print("经纬度/p2p信息{}" .format(result))
    return result


if __name__ == '__main__':
    identifies_json = get_cities_json()
    aid = '97137413'
    url = 'https://music.163.com/weapi/user/getfolloweds?csrf_token=cdee144903c5a32e6752f50180329fc9'
    page = 1
    while page:

        for key in distributions:
            print("key：%s value: %s"%(key,distributions[key]))

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
    app.run(host='0.0.0.0', port=8000, debug=False)