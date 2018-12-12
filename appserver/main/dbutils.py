import sqlite3
import os


class dbtool:

    def get_dbfile(self):
        dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dbfile = os.path.join(dir_name, "db/userdata")
        return dbfile

    def connect_db(self):
        dbfile = self.get_dbfile()
        if os.path.exists(dbfile):
            return False
        else:
            return sqlite3.connect(dbfile)

    def init_db(self):
        conn=self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE user_info (name VARCHAR(20) PRIMARY KEY,passwd VARCHAR(30),type INT)')
            cursor.execute('insert into user_info (name,passwd,type) values (\'admin\',\'admin\',1)')
            cursor.close()
            conn.commit()
            conn.close()

class usertable():

    def __init__(self):
        dbt = dbtool()
        self.conn=sqlite3.connect(dbt.get_dbfile())

    def user_query(self,wherestr="1=1"):
        cursor = self.conn.cursor()
        cursor.execute('select * from user_info where %s' %wherestr)
        values = cursor.fetchall()
        cursor.close()
        self.conn.close()
        return values


    def updateuserpasswd(self,username,newpasswd):
        cursor = self.conn.cursor()
        cursor.execute("update user_info set passwd='%s' where name='%s'"  %(newpasswd,username))
        self.conn.commit()
        cursor.close()
        self.conn.close()
        return True


    def user_add(self,username,userpass,usertype):
        cursor = self.conn.cursor()
        cursor.execute("insert into user_info (name,passwd,type) values ('"+username+"','"+userpass+"',"+usertype+")")
        cursor.close()
        self.conn.commit()
        cursor.close()
        self.conn.close()
        return True


    def user_del(self,username):
        cursor = self.conn.cursor()
        cursor.execute("delete from user_info where name='%s'" %username)
        cursor.close()
        self.conn.commit()
        cursor.close()
        self.conn.close()
        return True




