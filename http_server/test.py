import os,base64,requests
import json
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
            f.write(base64.b64decode(image_str))
        return "OK"
    except:
        return "error"
def file_test():
    path = "2.png"
    imgstr = img2base64(path)
    print("imgstring:",imgstr)
    files = {'image': ('2.png', open('2.png', 'rb'), 'image/png', {})}
    url = 'http://192.168.3.9:5000/runningfast/api/v1.0/upload'
    body = {"image": imgstr}
    response = requests.post(url,files = files,data=body)
    print(response.text)
    print(response.status_code)

def post_test():
    path = '2.png'
    imgstr = img2base64(path)
    #url = 'http://192.168.3.9:5000/runningfast/api/v1.0/image'
    url = 'http://47.104.70.158:8080/image/upload'
    body = {"image": imgstr}
    response = requests.post(url,data=body)
    print(response.text)
    print(response.status_code)
    print(response.request.headers)
    print(response.request.headers['content-type'])
post_test()