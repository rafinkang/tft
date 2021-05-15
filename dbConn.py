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
                
            if result != None:
                return curs.fetchall()
            
        except Exception as e:
            print(e)
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
                
            if result != None:
                return self.dictfetchall(curs)
            
        except Exception as e:
            print(e)
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
            curs = conn.cursor()
            if args == None:
                result = curs.execute(sql)
            else:
                result = curs.execute(sql, args)
                
            if result != None:
                return curs.lastrowid
            else:
                raise Exception('에러발생!! ----- \n '+sql)
            
        except Exception as e:
            print(e)
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
                
            if result != None:
                return True
            else:
                raise Exception('에러발생!! ----- \n '+sql)
            
        except Exception as e:
            print(e)
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
            
            
# if __name__ == "__main__":
#     db = DbConn()
#     sql = 'select * from crawl_color'
#     print(db.select(sql))
    
#     # sql = "insert into crawl_color(h1,s1,v1,h2,s2,v2,h3,s3,v3,h4,s4,v4,color,filename) values(2,2,2,2,2,2,3,3,3,4,4,4,'color','test.test')"
    
#     sql = "insert into test(test, test2, test3) values(%s, %s, %s);"
#     data = [['1','1','1'], ['2','2','2'], ['3','3','3']]
#     print(db.executemany(sql, data))

    # db = DbConn()
    # print(db.selectdict('select * from items_info'))
    # db.execute("insert into items_info (ii_id, ii_name, ii_is_unique, ii_is_shadow) values (%d, %s, %d, %d)", (6,"Negatron Cloak", 0, 0))
    # # db.execute(f'insert into items_info (ii_id, ii_name, ii_is_unique, ii_is_shadow) values (6, "Negatron Cloak", 0, 0)')
    # print(db.select('select * from items_info'))