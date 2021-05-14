import mysql.connector

class DbConn:
    def __init__(
        self, 
        host = "jhta.cpg6w8n0aifr.ap-northeast-2.rds.amazonaws.com", 
        dbname = "tft", 
        user = "scott", 
        password = "tigertiger", 
        port = "3306"
        ):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
        self.connection = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.password,
            database = self.dbname
            )
        # self.user, self.password, self.host+":"+self.port+"/"+self.dbname
        
        

    def select(self, sql, args=None):
        """
        단일 행 select 실행 
        ex) data = (1, 'test') 
        execute(sql, data)
        """
        
        try:
            curs = self.connection.cursor()
            
            if args == None:
                curs.execute(sql)
            else:
                curs.execute(sql, args)

            return self.dictfetchall(curs) # dictionary로 return
                
        except Exception as e:
            return e    
        
        finally:
            self.connection.close()
            
    def execute(self, sql, args=None):
        """
        단일 행 실행 
        ex) data = (1, 'test') 
        execute(sql, data)
        """
        try:
            curs = self.connection.cursor()
            if args == None:
                result = curs.execute(sql)
            else:
                result = curs.execute(sql, args)
                
            return result
            
        except Exception as e:
            return e    
        
        finally:
            self.connection.commit()
            self.connection.close()
            
    def executemany(self, sql, args=None):
        """
        다중 행 실행 
        ex) data = [[1, 'test'],[2, 'test2'],[3, 'test3'],[4, 'test4']]
        executemany(sql, data)
        """

        try:
            curs = self.connection.cursor()
            if args == None:
                result = curs.executemany(sql)
            else:
                result = curs.executemany(sql, args)
                
            return result
            
        except Exception as e:
            return e
            
        finally:
            self.connection.commit()
            self.connection.close()

    def dictfetchall(self, curs):

        columns = [col[0] for col in curs.description]
        rows = [dict(zip(columns, row)) for row in curs.fetchall()]

        return rows
        
        

dbtest = DbConn()
print(dbtest.select('select * from items_info'))