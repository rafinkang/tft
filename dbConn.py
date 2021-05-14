import pymysql


class DbConn:
    """
    mysql dbconnection
    """

    def __init__(
        self,
        host = "jhta.cpg6w8n0aifr.ap-northeast-2.rds.amazonaws.com", 
        user = "scott", 
        password = "tigertiger", 
        db = "tft", 
        charset='utf8'
    ):
        super().__init__()
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        # self.conn = pymysql.connect(
        #     host=self.host, user=self.user, password=self.password, db=self.db, charset=self.charset)


    def select(self, sql, args=None):
        """
        단일 행 select 실행 
        ex) data = (1, 'test') 
        execute(sql, data)
        """
        conn = pymysql.connect(
            host=self.host, user=self.user, password=self.password, db=self.db, charset=self.charset)
        try:
            curs = conn.cursor()
            if args == None:
                result = curs.execute(sql)
            else:
                result = curs.execute(sql, args)
                
            if result:
                return curs.fetchall()
            
        except Exception as e:
            return e    
        
        finally:
            conn.commit()
            conn.close()
            
    def selectdict(self, sql, args=None):
        """
        단일 행 select 실행 return dictionary
        ex) data = (1, 'test') 
        execute(sql, data)
        """
        conn = pymysql.connect(
            host=self.host, user=self.user, password=self.password, db=self.db, charset=self.charset)
        try:
            curs = conn.cursor()
            if args == None:
                result = curs.execute(sql)
            else:
                result = curs.execute(sql, args)
                
            if result:
                return self.dictfetchall(curs)
            
        except Exception as e:
            return e    
        
        finally:
            conn.commit()
            conn.close()
            
    def execute(self, sql, args=None):
        """
        단일 행 실행 
        ex) data = (1, 'test') 
        execute(sql, data)
        """
        conn = pymysql.connect(
            host=self.host, user=self.user, password=self.password, db=self.db, charset=self.charset)
        try:
            print(sql, args)
            curs = conn.cursor()
            if args == None:
                result = curs.execute(sql)
            else:
                result = curs.execute(sql, args)
                
            print(result)
            return result
            
        except Exception as e:
            return e    
        
        finally:
            conn.commit()
            conn.close()
            
    def executemany(self, sql, args=None):
        """
        다중 행 실행 
        ex) data = [[1, 'test'],[2, 'test2'],[3, 'test3'],[4, 'test4']]
        executemany(sql, data)
        """
        conn = pymysql.connect(
            host=self.host, user=self.user, password=self.password, db=self.db, charset=self.charset)
        try:
            curs = conn.cursor()
            if args == None:
                result = curs.executemany(sql)
            else:
                result = curs.executemany(sql, args)
                
            return result
            
        except Exception as e:
            return e
            
        finally:
            conn.commit()
            conn.close()
            
    def dictfetchall(self, cursor):
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
            
            
if __name__ == "__main__":
#     db = DbConn()
#     sql = 'select * from crawl_color'
#     print(db.select(sql))
    
#     # sql = "insert into crawl_color(h1,s1,v1,h2,s2,v2,h3,s3,v3,h4,s4,v4,color,filename) values(2,2,2,2,2,2,3,3,3,4,4,4,'color','test.test')"
    
#     sql = "insert into test(test, test2, test3) values(%s, %s, %s);"
#     data = [['1','1','1'], ['2','2','2'], ['3','3','3']]
#     print(db.executemany(sql, data))

    db = DbConn()
    print(db.select('select * from items_info'))
    # db.execute("insert into items_info (ii_id, ii_name, ii_is_unique, ii_is_shadow) values (%d, %s, %d, %d)", (6,"Negatron Cloak", 0, 0))
    db.execute(f"insert into items_info (ii_id, ii_name, ii_is_unique, ii_is_shadow) values ({6}, {'Negatron Cloak'}, {0}, {0})")
    print(db.select('select * from items_info'))
















# import mysql.connector

# class DbConn:
#     def __init__(
#         self, 
#         host = "jhta.cpg6w8n0aifr.ap-northeast-2.rds.amazonaws.com", 
#         dbname = "tft", 
#         user = "scott", 
#         password = "tigertiger", 
#         port = "3306"
#         ):
#         self.host = host
#         self.dbname = dbname
#         self.user = user
#         self.password = password
#         self.port = port
#         self.connection = mysql.connector.connect(
#             host = self.host,
#             user = self.user,
#             passwd = self.password,
#             database = self.dbname
#             )
#         # self.user, self.password, self.host+":"+self.port+"/"+self.dbname
        
        

#     def select(self, sql, args=None):
#         """
#         단일 행 select 실행 
#         ex) data = (1, 'test') 
#         execute(sql, data)
#         """
        
#         try:
#             curs = self.connection.cursor()
            
#             if args == None:
#                 curs.execute(sql)
#             else:
#                 curs.execute(sql, args)

#             return self.dictfetchall(curs) # dictionary로 return
                
#         except Exception as e:
#             return e    
            
#     def execute(self, sql, args=None):
#         """
#         단일 행 실행 
#         ex) data = (1, 'test') 
#         execute(sql, data)
#         """
#         try:
#             curs = self.connection.cursor()
#             if args == None:
#                 curs.execute(sql)
#             else:
#                 curs.execute(sql, args)
            
#         except Exception as e:
#             return e    
        
#         finally:
#             self.connection.commit()
#             return True
            
#     def executemany(self, sql, args=None):
#         """
#         다중 행 실행 
#         ex) data = [[1, 'test'],[2, 'test2'],[3, 'test3'],[4, 'test4']]
#         executemany(sql, data)
#         """

#         try:
#             curs = self.connection.cursor()
#             if args == None:
#                 curs.executemany(sql)
#             else:
#                 curs.executemany(sql, args)
                
#         except Exception as e:
#             return e
            
#         finally:
#             self.connection.commit()
#             return True

#     def dictfetchall(self, curs):

#         columns = [col[0] for col in curs.description]
#         rows = [dict(zip(columns, row)) for row in curs.fetchall()]

#         return rows
    
#     def close(self):
#         self.connection.close()
        

# dbtest = DbConn()
# print(dbtest.select('select * from items_info'))
# # dbtest.execute("insert into items_info (ii_id, ii_name, ii_is_unique, ii_is_shadow) values (%d, %s, %d, %d)", (6,"Negatron Cloak", 0, 0))
# dbtest.execute(f"insert into items_info (ii_id, ii_name, ii_is_unique, ii_is_shadow) values ({6}, {'Negatron Cloak'}, {0}, {0})")
# print(dbtest.select('select * from items_info'))
# dbtest.close()