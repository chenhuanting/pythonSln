import os,base64,json
def INIT_CONFIG(): 
    try:
        with open("./conf.json",'r') as load_f:
            Config = json.load(load_f)
        print(Config)
    except:
        print("could not find conf.json file!")
    return Config