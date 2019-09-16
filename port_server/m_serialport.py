import sys
import serial
import serial.tools.list_ports
import time
class P_Serial():
    def __init__(self,port,baud,parity,stopbits,bystesize):
        self.port=port
        self.baud=int(baud)
        self.parity=parity
        self.stopbits=int(stopbits)
        self.bytesize=int(bystesize)
        self.ser = serial.Serial()
        # 接收数据和发送数据数目置零
        self.data_num_received = 0
        self.standard_temp_value_dic={'low':0,'medium':0,'high':0}


    # 打开串口
    def port_open(self):
        self.ser.port = self.port
        self.ser.baudrate = self.baud
        self.ser.bytesize = self.bytesize
        self.ser.stopbits = self.stopbits
        self.ser.parity = self.parity

        try:
            self.ser.open()
        except:
            print("Port Error", "此串口不能被打开！")
            return None

        if self.ser.isOpen():
            print("串口状态（已开启）")

    # 关闭串口
    def port_close(self):
        try:
            self.ser.close()
        except:
            pass

    # 接收数据
    def data_receive(self,com):
        print("com:",com)
        reqValue = -1.0
        try:
            num = self.ser.write(com.encode('gbk'))
            num = self.ser.inWaiting()
            while num <= 0:
                num = self.ser.inWaiting()
                if num > 0:
                    data = self.ser.read(num)
                    num = len(data)
                    print("recieve:",data)
                    dataStr = str(data)
                    index  = dataStr.find(',')
                    #print("index",index)    
                    dataStr = dataStr[2:index]
                    #print("temp:",dataStr)
                    reqValue = float(dataStr)
                    break
        except:
            pass
        print("return :",reqValue)
        return reqValue
    def updateStandard(self):
        return self.standard_temp_value_dic['low'],self.standard_temp_value_dic['medium'],self.standard_temp_value_dic['high']

