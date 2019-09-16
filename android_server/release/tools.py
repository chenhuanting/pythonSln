import os,base64,json
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

   