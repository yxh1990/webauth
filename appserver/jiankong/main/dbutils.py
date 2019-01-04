

from datetime import date,datetime
from datetime import timedelta
import time

from jiankong.model.appmodel import UserLog
from jiankong import db

def insert_logs(name,action):
	now_str = time.strftime("%Y-%m-%d %H:%M:%S")
	logtime = datetime.strptime(now_str, "%Y-%m-%d %H:%M:%S")
	userlog=UserLog(name=name,action=action,time=logtime)
	db.session.add(userlog)
	db.session.commit()




