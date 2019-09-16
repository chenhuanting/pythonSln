#!/usr/bin/python
#coding:utf8
import base64
import os
import pymysql
from flask import (Flask, Response, json, jsonify, make_response, redirect,
                   render_template, request, session)
app = Flask(__name__)
from m_serialport import P_Serial

high_com ="READ1?\r"
mediume_com = "READ2?\r"
low_com = "READ3?\r"

@app.route('/standard_value/low',methods = ['GET','POST'])
def standard_read():
    try:
        low_standard_value = pSer.data_receive(low_com)
        code =200
    except:
        code = 400
        low_standard_value = -1

    data={
       "code":code,
        "message":"standard low value",
        "data":{
           "value":low_standard_value
        }
    }

    response = app.response_class(
        response=json.dumps(data),
        status=code,
        mimetype='application/json'
    )
    return response


@app.route('/standard_value/mediume',methods = ['GET','POST'])
def standard_read_mediume():
    try:
        mediume_standard_value = pSer.data_receive(mediume_com)
        code =200
    except:
        code = 400
        mediume_standard_value = -1

    data={
       "code":code,
        "message":"standard mediume value",
        "data":{
           "value":mediume_standard_value
        }
    }

    response = app.response_class(
        response=json.dumps(data),
        status=code,
        mimetype='application/json'
    )
    return response


@app.route('/standard_value/high',methods = ['GET','POST'])
def standard_read_high():
    code = 200
    try:
        high_standard_value = pSer.data_receive(high_com)
        code =200
    except:
        code = 400
        high_standard_value=-1

    data={
       "code":code,
        "message":"standard high value",
        "data":{
           "value":high_standard_value
        }
    }

    response = app.response_class(
        response=json.dumps(data),
        status=code,
        mimetype='application/json'
    )
    return response



def readConfig():
    with open("./conf.json",'r') as load_f:
        load_dict = json.load(load_f)
        print(load_dict)
    try:
        low_com = load_dict['low']
        print("low:",low_com)
        mediume_com = load_dict['low']
        print("mediume:",mediume_com)
        high_com = load_dict['low']
        print("high:",high_com)
    except:
        high_com ="READ1?\r"
        mediume_com = "READ2?\r"
        low_com = "READ3?\r"
        print("could not find conf.json file!")
if __name__ == '__main__':
    readConfig()
    pSer=P_Serial('COM5',9600,'N',1,8)
    pSer.port_open()
    app.run(debug=False,host='0.0.0.0',port=5001)
    

