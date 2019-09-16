#!/usr/bin/python
#coding:utf8

from flask import Flask, render_template, url_for, request,redirect,make_response,session ,jsonify,Response,json
import os,pymysql,base64,datetime
import requests as http_request 
import config
import tools
from Refer_DB import Refer_MYSQL
from Mysql_DB import Database_MYSQL
app = Flask(__name__)

@app.route('/runningfast/api/v1.0/info/filt',methods = ['GET','POST'])
def info_filt():
    try:
        calibration_level=request.args.get('type')
        standard_name=request.args.get('range')
        code = 200
        message="return all custom id and calibration point list "

    except:
        code = 400
        message="'type,range'informat error"
        data={}
    if code == 200:
        try:
            upper,lower=refer_db.standard_range_limit(standard_name)
            custom_num_list=refer_db.query_calibration_info(calibration_level,upper,lower)
            data= { "custom_num_list":custom_num_list}
        except:
            code=400
            message="system internal databases error"
            data={}

    
    response_body={
        "code":code,
        "message":message,
        "data":data
    }   
    response = app.response_class(
            response=json.dumps(response_body),
            status=code,
            mimetype='application/json'
        )
    return response

@app.route('/runningfast/api/v1.0/info/doc',methods = ['GET','POST'])
def info_doc():
    try:
        calibration_level=request.args.get('type')
        standard_name=request.args.get('range')
        code = 200
        message="return all custom id and calibration point list "

    except:
        code = 400
        message="'type,range'informat error"
        data={}
    if code == 200:
        try:
            print("code",code)
            upper,lower=refer_db.standard_range_limit(standard_name)
            print(upper,lower)
            all_point_list=refer_db.get_all_point(calibration_level,upper,lower)
            data= { "point_custom_list":all_point_list}
        except:
            code=400
            message="system internal databases error"
            data={}

    
    response_body={
        "code":code,
        "message":message,
        "data":data
    }   
    response = app.response_class(
            response=json.dumps(response_body),
            status=code,
            mimetype='application/json'
        )
    return response

@app.route('/runningfast/api/v1.0/info/custom/',methods = ['GET','POST'])
def info_custom():
    try:
        calibration_level=request.args.get('type')
        standard_name=request.args.get('range')
        code = 200
    except:
        code = 400
        message=" 'type','range' informat error"
        data={'null'}

    if code == 200:
        try:
            upper,lower=refer_db.standard_range_limit(standard_name)
            custom_num_list=refer_db.query_custom_id(calibration_level,upper,lower)
            data={ "custom_id_list":custom_num_list}
        except:
            code = 400
            message = "system internal databases error"
            data={'null'}

    response_body={
        "code":code,
        "message":message,
        "data":data
    }   
    response = app.response_class(
        response=json.dumps(response_body),
        status=code,
        mimetype='application/json'
    )

    return response

@app.route('/runningfast/api/v1.0/info/calibration/',methods = ['GET','POST'])
def info_calibration_from_custom():
    try :
        calibration_level=request.args.get('type')
        standard_name=request.args.get('range')
        custom_id=request.args.get('custom_id')
        code = 200
    except:
        code = 400
        message=" 'type','range' ,'custom_id' informat error"
        data={'null'}
    if code == 200:
        try:
            upper,lower=refer_db.standard_range_limit(standard_name)
            custom_num_list=refer_db.query_calibration_from_custom(custom_id,calibration_level,upper,lower)
            message =  "return custom id and calibration point list "
            data=custom_num_list
        except:
            code = 400
            message = "system internal databases error"
            data={'null'}
    response_body={
        "code":code,
        "message":message,
        "data":data
    }   
    response = app.response_class(
        response=json.dumps(response_body),
        status=code,
        mimetype='application/json'
    )
    return response
 
@app.route('/runningfast/api/v1.0/result', methods=['GET','POST'])
def submit():
    if request.method == 'POST':
        try:
            #user_id = request.form['user_id']
            custom_id= request.form['custom_id']
            calibration_point= eval(request.form['calibration_point'])
            calibration_value_list=eval(request.form['calibration_value_list'])
            calibration_average=eval(request.form['calibration_average'])
            standard_value_list=eval(request.form['standard_value_list'])
            standard_average=eval(request.form['standard_average'])
            try:
                img_data_str=request.form['image']
                date_str=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                image_path=date_str+str(".png")
                image_folder=m_Config['image_folder']
                
                save_image_path = str(image_folder)+image_path
                print("save image path:",save_image_path)
                net = tools.str2img(save_image_path,str(img_data_str))
            except:
                #print("image base64:",img_data_str)
                img_data_str = "null"
                net = "null"

            data = {
            "code":200,
            "message":"submit result",
            "data":{
                "custom_id":custom_id,
                "calibration_point": calibration_point,
                "calibration_value_list":calibration_value_list,
                "calibration_average":calibration_average,
                "standard_value_list":standard_value_list,
                "standard_average":standard_average,
                "image:":net
                }
            }
            
            try:
                refer_db.update_calibration_info(custom_id,calibration_point,calibration_value_list,calibration_average,standard_value_list,standard_average,img_data_str)
            except:
                print("update info error")
                print("submit data :",data)  
            try:
                upload_url = m_Config['upload_url']
                upload_body = {"image": img_data_str}
                upload_response = http_request.post(upload_url,data=upload_body)
                print(upload_response.text) 
            except:
                print("could not upload image to esc")         
            response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
            )      
        except:
            data = {
                "code":400,
                "message":"submit format error"
            }
            response = app.response_class(
            response=json.dumps(data),
            status=400,
            mimetype='application/json'
            )
        return response
       
    else:
        data = {
                "code":400,
                "message":" method format error"
        }
        response = app.response_class(
            response=json.dumps(data),
            status=400,
            mimetype='application/json'
            )
        return response

@app.route('/runningfast/api/v1.0/standard/settings', methods=['GET','POST'])
def standard_settings():
    if request.method == 'POST':
        try:
            low_ranges = eval(request.form['low_range'])
            medium_ranges= eval(request.form['medium_range'])
            high_ranges= eval(request.form['high_range'])
            refer_db.reset_standard_range('low',low_ranges[1],low_ranges[0])
            refer_db.reset_standard_range('medium',medium_ranges[1],medium_ranges[0])
            refer_db.reset_standard_range('high',high_ranges[1],high_ranges[0])
            data = {
            "code":200,
            "message":"reset standard settings",
            "data":{
            "low_range":low_ranges,
            "medium_range":medium_ranges,
            "high_range":high_ranges
                }

            }
            response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
            )
        except:
            data={
                "code":400,
                "message":"reset format error"
            }
            response = app.response_class(
            response=json.dumps(data),
            status=400,
            mimetype='application/json'
            )
        return response
    else:
        try:
            db_low_range,db_meduime_range,db_high_range = refer_db.get_standard_range()
            code = 200
        except:
            code = 400
            db_low_range= db_meduime_range=db_high_range = [-1,-1]

        data={
                "code":code,
                "message":"recieve standarad range",
                "data":{
                    "low_range":db_low_range,
                    "mediume_range":db_meduime_range,
                    "high_range":db_high_range
                }
        }
        response = app.response_class(
            response=json.dumps(data),
            status=code,
            mimetype='application/json'
        )
        return response
def getConfigPara(Config):
    try:
        db_ip = m_Config['db_ip']
        db_name=m_Config['db_name']
        db_user_name=m_Config['user_name']
        db_user_passwd=m_Config['user_passwd']
    except:
        return -1
    return 0
if __name__ == '__main__':
    m_Config=config.INIT_CONFIG()
    nRet = getConfigPara(m_Config)
    if nRet == 0:
        db_ip = m_Config['db_ip']
        db_name=m_Config['db_name']
        db_user_name=m_Config['user_name']
        db_user_passwd=m_Config['user_passwd']
        refer_db=Refer_MYSQL(db_ip,db_user_name,db_user_passwd,db_name)
        app.run(debug=False,host='0.0.0.0',port=5000)
    else:
        print("config error")
    
   