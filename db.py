import sqlite3

class Database:
    def __init__(self):
        self.conn=sqlite3.connect("schedule.db")
        self.conn.row_factory=sqlite3.Row
        self.cur=self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS auth_data(username TEXT,pin TEXT,created_at TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY,username TEXT,task TEXT, start TEXT, end TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS checks(username TEXT,checked_id TEXT,date TEXT)")
    def add_user(self,username,pin,date):
        self.cur.execute("INSERT INTO auth_data(username,pin,created_at) VALUES(?,?,?)",(username,pin,date))
        self.conn.commit()
        self.conn.close()
    def check_user(self,username,pin):
        db_pin=self.cur.execute("SELECT pin FROM auth_data WHERE username=?",(username,)).fetchone()
        self.conn.close()
        if db_pin is None or db_pin["pin"]!=pin:
            return False
        else:
            return True
    def add_task(self,username,task,start,end):
        self.cur.execute("INSERT INTO data(username,task,start,end) VALUES(?,?,?,?)",(username,task,start,end))
        self.conn.commit()
        self.conn.close()
    def fetch_tasks(self,username):
        data=self.cur.execute("SELECT id,task,start,end FROM data WHERE username=?",(username,)).fetchall()
        self.conn.close()
        return data
    def add_checks(self,username,checks,date):
        self.cur.execute("INSERT INTO checks(username,checked_id,date) VALUES(?,?,?)",(username,checks,date))
        self.conn.commit()
        self.conn.close()
    def get_first_date(self,username):
        date=self.cur.execute("SELECT created_at FROM auth_data WHERE username=?",(username,)).fetchone()
        self.conn.close()
        return date["created_at"]
    def get_checks(self,username,date):
        checks=self.cur.execute("SELECT checked_id FROM checks WHERE username=? AND date=?",(username,date)).fetchall()
        self.conn.close()
        return [row["checked_id"] for row in checks]
    def delete_tasks(self,id):
        self.cur.execute("DELETE FROM data WHERE id=?",(id,))
        self.conn.commit()
        self.conn.close()
    def get_all_checks(self,username):
        checks=self.cur.execute("SELECT checked_id,date FROM checks WHERE username=? ",(username,)).fetchall()
        self.conn.close()
        return [[row["checked_id"],row["date"]] for row in checks]
