#!/usr/bin/python
#coding:utf8
import base64
import os
import pymysql
import socket
from flask import (Flask, Response, json, jsonify, make_response, redirect,
                   render_template, request, session)
app = Flask(__name__)
high_com ="READ1?\r"
mediume_com = "READ2?\r"
low_com = "READ3?\r"
usr_ip='192.168.1.200'
usr_port=8899    
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #声明socket类型，同时生成链接对象
def sendSockeInfo(com):
    value = -2.0
    data='none'
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((usr_ip, usr_port))
            s.sendall(com.encode())
            data = s.recv(1024)
        print("revicev:",str(data.decode()))
        dataStr = str(data.decode())
        index = dataStr.find(',')
        if(index  > 0):
            reqStr=dataStr[:index]
            value=float(reqStr)
        print("return :",value)
    except:
        value=-2.0
        print("could not get standard temp")
    return value
def SockeTest(com):
    value = -2.0
    data='none'
    HOST = usr_ip  # 服务器的主机名或者 IP 地址
    PORT = usr_port        # 服务器使用的端口
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(com.encode())
        data = s.recv(1024)
        print("revicev:",str(data.decode()))
        dataStr = str(data.decode())
        print(dataStr)
    return value
@app.route('/standard_value',methods = ['GET','POST'])
def standard_test():
    value = SockeTest(low_com)
    code =200
    data={
       "code":code,
        "message":"standard test value",
        "data":{
           "value":value
        }
    }
    response = app.response_class(
        response=json.dumps(data),
        status=code,
        mimetype='application/json'
    )
    return response

@app.route('/standard_value/low',methods = ['GET','POST'])
def standard_read():
    try:
        low_standard_value = sendSockeInfo(low_com)
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
        mediume_standard_value = sendSockeInfo(mediume_com)
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
        high_standard_value = sendSockeInfo(high_com)
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
        #usr_ip=load_dict['usr_ip']
        #print("usr_ip:",usr_ip)
        #usr_port=load_dict['port']
        #print("port:",usr_port)
    except:
        high_com ="READ1?\r"
        mediume_com = "READ2?\r"
        low_com = "READ3?\r"
        #usr_ip="192.168.1.200"
        #usr_port=8899
        print("could not find conf.json file!")
if __name__ == '__main__':
    readConfig()
    app.run(debug=False,host='0.0.0.0',port=5001)

