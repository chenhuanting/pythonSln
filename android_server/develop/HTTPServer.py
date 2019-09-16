#!/usr/bin/python
#coding:utf8

from flask import Flask, render_template, url_for, request,redirect,make_response,session ,jsonify,Response,json
import os,pymysql,base64,datetime
from Refer_DB import Refer_MYSQL
import urllib
from urllib import request as url_request
import requests as http_request 
from io import BytesIO
app = Flask(__name__)
app.secret_key='afjlsjfowflajflkajfkjfkaljf'
user_list = ['jim','max','py']
imagepath = os.path.join(os.getcwd(),"static/images")
null_data = {
        "code":200,
        "message":"OK",
    }
null_response = app.response_class(
        response=json.dumps(null_data),
        status=200,
        mimetype='application/json'
    )
error_code={
    "code":410,
    "message":"format error"
}
standard_url = 'http://127.0.0.1:5001/standard_value/'
#设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def img2base64(path):
    try:
        with open(path,'rb') as f:
            base64_data = base64.b64encode(f.read())
            s = base64_data.decode()
        return s
    except:
        return "image to base64 error"
def str2img(path,image_str):
    try:
        with open(path,'wb') as f:
            f.write(base64.decodebytes(image_str.encode()))
        return "OK"
    except:
        return "error"

@app.route('/runningfast/api/v1.0/info/filt',methods = ['GET','POST'])
def info_filt():
    try:
        calibration_level=request.args.get('type')
        standard_name=request.args.get('range')
    except:
        data={
            "code":400,
            "message":"'type,range'informat error"
        }
        response = app.response_class(
        response=json.dumps(data),
        status=400,
        mimetype='application/json')
        return response

    try:
        upper,lower=refer_db.standard_range_limit(standard_name)
        custom_num_list=refer_db.query_calibration_info(calibration_level,upper,lower)
        data={
            "code":200,
            "message" : "return all custom id and calibration point list ",
            "data":{ "custom_num_list":custom_num_list
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
            "message":"system internal databases error"
        }
        response = app.response_class(
        response=json.dumps(data),
        status=400,
        mimetype='application/json'
        )

    return response

@app.route('/runningfast/api/v1.0/info/custom/',methods = ['GET','POST'])
def info_custom():
    calibration_level=request.args.get('type')
    standard_name=request.args.get('range')
    upper,lower=refer_db.standard_range_limit(standard_name)
    custom_num_list=refer_db.query_custom_id(calibration_level,upper,lower)
    data={
        "code":200,
        "message" : "return custom id",
        "data":{ "custom_id_list":custom_num_list
        }
    }
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )

    return response

@app.route('/runningfast/api/v1.0/info/calibration/',methods = ['GET','POST'])
def info_calibration_from_custom():
    calibration_level=request.args.get('type')
    standard_name=request.args.get('range')
    custom_id=request.args.get('custom_id')
    upper,lower=refer_db.standard_range_limit(standard_name)
    custom_num_list=refer_db.query_calibration_from_custom(custom_id,calibration_level,upper,lower)
    data={
        "code":200,
        "message" : "return custom id and calibration point list ",
        "data":custom_num_list
        
    }
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )

    return response
@app.route('/runningfast/api/v1.0/standard/ready/',methods = ['GET','POST'])
def standard_read():
    try:
        response = url_request.urlopen(standard_url)
        jsondata=str(response.read())
        jsondata=jsondata[1:]
        jsondata=eval(jsondata)
        jsondata= json.loads(jsondata)
        jsondata=jsondata['data']
        low=jsondata['low']
        medium=jsondata['medium']
        high=jsondata['high']
        print("data:",jsondata,"length:",len(jsondata),"type:",type(jsondata))
        print('low:',low,'medium:',medium,'high:',high)
    except:
        low=medium=high=0
        
    data={
        "code":200,
        "message":"read standard value",
        "data":{
           "low_value":low,
           "medium_value":medium,
           "high_value":high
        }
    }

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/runningfast/api/v1.0/standard/read',methods = ['GET','POST'])
def standard_read_value():
    try:
        standard_range=request.args.get('range')
        request_url = standard_url+str(standard_range)
        print("url:",request_url)
        response = url_request.urlopen(request_url)
        jsondata=str(response.read())
        jsondata=jsondata[1:]
        jsondata=eval(jsondata)
        jsondata= json.loads(jsondata)
        jsondata=jsondata['data']
        value=jsondata['value']
        print("data:",jsondata,"length:",len(jsondata),"type:",type(jsondata))
        print('value:',value)
    except:
        value=0
        
    data={
        "code":200,
        "message":"read standard value",
        "data":{
           "value":value,
        }
    }

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/runningfast/api/v1.0/standard/',methods = ['GET','POST'])
def standard_agency():
    s = http_request.get(standard_url)
    print("standard url:",standard_url)
    print(s.text)
    data = http_request.get(standard_url).json()
    response = app.response_class(
            response=json.dumps(data),
            status=400,
            mimetype='application/json'
        )
    return response

@app.route('/runningfast/api/v1.0/standard/acquisition/',methods = ['GET','POST'])
def standard_acquisition():
    data = {
        "code":200,
        "message":"recieve standard value info",
        "data":{
        "standard_value_list":[10.1,20.2,30.3,40.5,50.6,60.7,70.9,80]
        }

    }
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/runningfast/api/v1.0/result', methods=['GET','POST'])
def submit():
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
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
                save_image_path = str('images/')+image_path
                net = str2img(save_image_path,str(img_data_str))
            except:
                print("image base64:",img_data_str)
                img_data_str = "null"
                net = "null"

            data = {
            "code":200,
            "message":"submit result",
            "data":{
                "user_id":user_id,
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
                refer_db.update_calibration_info(custom_id,user_id,calibration_point,calibration_value_list,calibration_average,standard_value_list,standard_average,img_data_str)
            except:
                print("update info error")
                print("submit data :",data)  
            try:
                upload_url = 'http://47.104.70.158:8080/image/upload'
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
        #request.args['username']
        return null_response

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

@app.route('/runningfast/api/v1.0/image', methods=['GET','POST'])
def submit_image():
    if request.method == 'POST':
        try:
            src = request.get_data()
            img_data_str = request.form['image']
            #print("image_data_str",img_data_str)
            date_str=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            image_path=date_str+str(".png")
            save_image_path = str("images/")+image_path
            nRet = str2img(save_image_path,img_data_str)
        except:
            try:
                print("error")
                src = request.get_data()
                src_json = eval(src)
                img_data_str =src_json['image']
                date_str=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                image_path=date_str+str(".png")
                save_image_path = str("images/")+image_path
                nRet = str2img(save_image_path,str(img_data_str)) 
            except:
                print(request.get_data())
            #print(src_json)
    data = {
           "code":200,
            "message":"submit sucess",
            } 
    response = app.response_class(
           response=json.dumps(data),
            status=200,
            mimetype='application/json'
            )      
    return response


@app.route('/runningfast/api/v1.0/upload', methods=['POST', 'GET']) 
def upload():
    if request.method == 'POST':
        print(request.get_data())
        f = request.files['image']
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
        date_str=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        image_path=date_str+str(".png")
        static_image_path = str("static/")+image_path
        f.save(static_image_path)
    data = {
            "code":200,
            "message":"submit sucess",
            } 
    response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
            )      
    return response

def readServerIP():
    with open("./conf.json",'r') as load_f:
        load_dict = json.load(load_f)
        print(load_dict)
    try:
        standard_url = load_dict['url']
        print("standard_url:",standard_url)
    except:
        standard_url = 'http://127.0.0.1:5001/standard_value/'
        print("could not find conf.json file!")
        
if __name__ == '__main__':
    readServerIP()
    refer_db=Refer_MYSQL()
    app.run(debug=True,host='0.0.0.0',port=5000)