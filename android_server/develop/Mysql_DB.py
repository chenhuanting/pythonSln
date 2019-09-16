import os,pymysql,base64
class Database_MYSQL():  
    def getConn(self,ip_url, user, passwrd, database_name):
        try:
            self.db = pymysql.connect(ip_url, user, passwrd, database_name) 
            return 1
        except Exception as e:
            print(str(e))
            return 0
            
    def query(self, sql ,param=None):
        '''查询'''
        try:
             with self.db.cursor(pymysql.cursors.DictCursor) as cursor:
                
                if param == None :
                    cursor.execute(sql)
                else:
                    cursor.execute(sql, param)
                
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(str(e))
        
    def commit(self,sql,param=None):
        try:
            with self.db.cursor(pymysql.cursors.DictCursor) as cursor:
                
                if param == None :
                    cursor.execute(sql)
                else:
                    cursor.execute(sql, param)
                
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(str(e))

    def close(self):
        '''数据库关闭'''
        try:
            self.db.close()
        except Exception:
            pass
