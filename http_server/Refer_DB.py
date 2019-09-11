import os,pymysql,base64
from Mysql_DB import Database_MYSQL
class Refer_MYSQL():
    def __init__(self):
        self.m_DB=Database_MYSQL()
        self.m_Conn=self.m_DB.getConn("127.0.0.1","root","root","thermometers")
        self.m_query_point_list={}
        self.m_query_point_list['unfinished']="select 名义温度 from tbpoint where `自编号` LIKE '%s' AND `结果` IS NULL AND `名义温度` BETWEEN %s AND %s;" 
        self.m_query_point_list['finished']="select 名义温度 from tbpoint where `自编号` LIKE '%s' AND `结果` IS NOT NULL AND `名义温度` BETWEEN %s AND %s;" 
        self.m_query_point_list['total']="select 名义温度 from tbpoint where `自编号` LIKE '%s' AND `名义温度` BETWEEN %s AND %s;" 
        self.m_query_custom_list={}
        self.m_query_custom_list['unfinished']="select 自编号 from tbpoint where `名义温度` BETWEEN %s AND %s AND `结果` IS NULL group by 自编号 asc;" 
        self.m_query_custom_list['finished']="select 自编号 from tbpoint where `名义温度` BETWEEN %s AND %s AND `结果` IS NOT NULL group by 自编号 asc;" 
        self.m_query_custom_list['total']="select 自编号 from tbpoint where `名义温度` BETWEEN %s AND %s  group by 自编号 asc;"
    
    def query_calibration_info(self,custom_type,upper_limit,lower_limit):
        query_custom_cmd="select 自编号 from tbpoint group by 自编号 asc;"
        custom_id_list=self.m_DB.query(query_custom_cmd)
        calibratioin_info_list=[]
        for i in range(len(custom_id_list)):
            own_id_dic=custom_id_list[i]
            own_id=own_id_dic['自编号']
            point_cmd= str(self.m_query_point_list[custom_type]) %(own_id,lower_limit,upper_limit)
            print(point_cmd)
            calibration_list=self.m_DB.query(point_cmd)
            calibration_point_list=[]
            for point_i in range(len(calibration_list)):
                nominal_point_dic=calibration_list[point_i]
                nominal_point=nominal_point_dic['名义温度']
                calibration_point_list.append(nominal_point)
            calibration_point_dic={"custom_id":own_id,"calibration_point_list":calibration_point_list}
            calibratioin_info_list.append(calibration_point_dic)
        print(calibratioin_info_list)    
        return calibratioin_info_list

    def query_custom_id(self,custom_type,upper_limit,lower_limit):
        query_custom_cmd=str(self.m_query_custom_list[custom_type]) %(lower_limit,upper_limit)
        print(query_custom_cmd)
        custom_id_list=self.m_DB.query(query_custom_cmd)
        custom_info_list=[]
        for i in range(len(custom_id_list)):
            own_id_dic=custom_id_list[i]
            own_id=own_id_dic['自编号']
            custom_info_list.append(own_id)
        return custom_info_list

    def query_calibration_from_custom(self,custom_id,custom_type,upper_limit,lower_limit):
        point_cmd= str(self.m_query_point_list[custom_type]) %(custom_id,lower_limit,upper_limit)
        #print(point_cmd)
        calibration_list=self.m_DB.query(point_cmd)
        calibration_point_list=[]
        for point_i in range(len(calibration_list)):
            nominal_point_dic=calibration_list[point_i]
            nominal_point=nominal_point_dic['名义温度']
            calibration_point_list.append(nominal_point)
        calibration_point_dic={"custom_id":custom_id,"calibration_point_list":calibration_point_list}
        return calibration_point_dic


    def update_calibration_info(self,custom_id,user_id,calibration_point,calibration_value_list,calibratioin_average,standard_value_list,standard_average,img_data_str):
        query_update_cmd= "UPDATE tbpoint SET 标准1次 = '%s' ,标准2次 = '%s' ,标准3次 = '%s',"\
		                    "标准4次 = '%s',标准5次 = '%s' ,标准6次 = '%s',"\
		                    "标准7次 = ' %s',标准8次 = '%s',显示1次 = '%s',"\
		                    "显示2次 = '%s' ,显示3次 = '%s',显示4次 = '%s',"\
		                    "显示5次 = '%s' ,显示6次 = '%s',显示7次 = '%s',"\
		                    "显示8次 = '%s', 标准平均 = '%s',显示平均 = '%s',结果 = '完成' ,检测次数='8', 校准人 = '%s', 图像1  = '%s' "\
                            "WHERE 自编号 = '%s' AND 名义温度 = %s;"\
                            %(standard_value_list[0],
                            standard_value_list[1],
                            standard_value_list[2],
                            standard_value_list[3],
                            standard_value_list[4],
                            standard_value_list[5],
                            standard_value_list[6],
                            standard_value_list[7],
                            calibration_value_list[0],
                            calibration_value_list[1],
                            calibration_value_list[2],
                            calibration_value_list[3],
                            calibration_value_list[4],
                            calibration_value_list[5],
                            calibration_value_list[6],
                            calibration_value_list[7],
                            standard_average,
                            calibratioin_average,
                            user_id,
                            img_data_str,
                            custom_id,
                            calibration_point)
        self.m_DB.commit(query_update_cmd)

    def standard_range_limit(self,standard_name):
        query_standard_range="select upper,lower from settings where standard_name like '%s';"%(standard_name)
        standard_range_list=self.m_DB.query(query_standard_range)
        standard_range_dic=standard_range_list[0]
        upper=standard_range_dic['upper']
        lower=standard_range_dic['lower']
        return upper,lower

    def reset_standard_range(self,standard_name,upper,lower):
        query_standar_range="update settings set upper = %s,lower = %s  where standard_name like '%s';"%(upper,lower,standard_name)
        self.m_DB.commit(query_standar_range)

    def close_db(self):
        self.m_DB.close()

