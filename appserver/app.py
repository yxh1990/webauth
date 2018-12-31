#!/usr/bin/env python
# -*- coding=utf8-*-
#author yanxianghui

from flask import Flask,render_template,request,redirect,session
from flask import jsonify,abort,json,make_response,send_from_directory,send_file
from flask_bootstrap import Bootstrap
from main import userhandler
from main import msgconfig as m
import os
from urllib.parse import unquote,quote
import json

from flask_sqlalchemy import SQLAlchemy
from datetime import date,datetime
from datetime import timedelta
import time

app = Flask(__name__)
app.debug = True


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/monitor.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

from model.appmodel import Userinfo
from model.appmodel import UserLog

@app.route('/index',methods=['GET'])
def index():
	return send_file("static/pages/sitetable.html")

@app.route('/')
def main():
	#打开登录页的时候进行数据库初始化
	db.create_all()
	users=Userinfo.query.filter_by(name='admin').first()
	#users = Userinfo.query.filter_by(name='sjz-jx').first()
	if not users:
		admin=Userinfo(name='admin',passwd='admin',type=1)
		loguser=Userinfo(name='sjzuser',passwd='sjzuser',type=2)
		#admin = Userinfo(name='sjz-jx', passwd='Sjzjx123$%^', type=1)
		db.session.add(admin)
		db.session.add(loguser)
		db.session.commit()
	dict={}
	dict["msg"]=m.loginmsg
	dict["username"]=m.loginame
	dict["count"]=m.count
	return render_template('index.html',**dict)

@app.route('/login',methods=['POST'])
def login():
	loginame = request.form.get('loginuser')
	loginpwd = request.form.get('loginpwd')
	logincount=request.form.get('logincount')
	#result = userhandler.checkuser(loginame, loginpwd)
	user = Userinfo.query.filter_by(name=loginame,passwd=loginpwd).first()
	if user:
		date1 = user.usertime
		date2 = date.today()
		tmpday = (date2-date1).days
		days = 60 - tmpday
		session['user'] = {'user':loginame,'type':user.type,'days':days}
		user.locktime=None
		user.failcount=0
		db.session.commit()
		m.loginame=""
		m.count=0
		#设置session超时时间为20分钟没有进行任何操作
		session.permanent = True
		app.permanent_session_lifetime = timedelta(minutes=10)
		insert_logs(loginame,"登录")
		if user.type == 2:
			return send_file("static/pages/logtable.html")
		else:
			return redirect("/index")

	lockuser = Userinfo.query.filter_by(name=loginame).first()
	if lockuser:
		if lockuser.failcount>=2:
			now_str = time.strftime("%Y-%m-%d %H:%M:%S")
			lockuser.locktime= datetime.strptime(now_str, "%Y-%m-%d %H:%M:%S")
		lockuser.failcount=lockuser.failcount+1
		m.count=lockuser.failcount
		db.session.commit()
		m.loginmsg="%s已经登录失败%d次" %(loginame,lockuser.failcount)
	else:
		m.loginmsg="用户名%s错误,登录失败" %(loginame)
		m.count=-1
	m.loginame=loginame
	return redirect("/")


@app.route("/logout",methods=["GET"])
def logout():
	insert_logs(session['user']['user'], "登出系统")
	session.pop('user')  # 删除session
	session.clear()      # 清除所有session
	return redirect("/")


@app.route('/site',methods=['GET'])
def get_sites():
	sites = userhandler.get_sitesexcelfile()
	return jsonify({'sites': sites})


@app.route('/logs',methods=['GET'])
def get_logs():
	logs = UserLog.query.order_by(UserLog.time.desc()).all()
	res=[]
	for log in logs:
		obj=log.jsonstr()
		res.append(obj)
	return jsonify({'logs': res})

@app.route('/upload',methods=['POST'])
def upload():
	f = request.files['file']
	userhandler.upload_excelfile(f)
	return "success"


@app.route('/downsite',methods=['GET'])
def downtxt():
	return send_from_directory('static/files/','sites.xlsx', as_attachment=True)


@app.route('/initsites',methods=['POST'])
def uploadtxt():
	f = request.files.get('myfile')
	if f:
		userhandler.upload_sitesexcel(f)
		insert_logs(session['user']['user'], "上传站点数据文件")
		return send_file("static/pages/sitetable.html")
	else:
		return "error"


@app.route('/initdir',methods=['GET'])
def initexecledir():
	userhandler.initexceldir()
	return "success"


@app.route('/excellist',methods=['GET'])
def getexcellist():
	sitename = request.args.get("sitename")
	templateName = request.args.get("templateName")
	sitename= unquote(unquote(sitename)).encode('utf-8').decode('utf-8-sig')
	filelist = userhandler.getexcellist(sitename, templateName)
	return jsonify(filelist)

@app.route('/uploadexcel',methods=['POST'])
def uploadexcel():
	f = request.files.get('myfile')
	sitename = request.form.get('sitename')
	templateName = request.form.get("templateName")
	userhandler.upload_excelfile(f, sitename, templateName)
	return send_file("static/pages/exceltable.html")

@app.route('/deletefile',methods=['GET'])
def deletefile():
	sitename = unquote(unquote(request.args.get("sitename")))
	filename = unquote(unquote(request.args.get("filename")))
	templateName = request.args.get("templateName")
	userhandler.deletefile(sitename, filename, templateName)
	return "success"


@app.route("/getusertype",methods=["GET"])
def getusertype():
	user_dict={}
	user_dict["username"]=session["user"]["user"]
	user_dict["usertype"]=session["user"]["type"]
	user_dict["redays"]=session["user"]["days"]
	return json.dumps(user_dict)


@app.route("/updateuserpasswd",methods=["POST"])
def updatepasswd():
	newpwd = request.form.get('newpwd')
	username=session["user"]["user"]
	#result = userhandler.updateuserpasswd(username, newpwd)
	user = Userinfo.query.filter_by(name=username).first()
	if len(newpwd) >=8 and len(newpwd)<=20:
		user.passwd=newpwd
		user.usertime=date.today()
		db.session.commit()
		insert_logs(session['user']['user'], "修改登录密码")
		return "1"
	else:
		return "0"

@app.route("/adduser",methods=["POST"])
def adduser():
	username=request.form.get('username')
	userpass=request.form.get('userpass')
	usertype=request.form.get('usertype')

	#result = userhandler.adduser(username, userpass,usertype)
	if checkuser(username,userpass,usertype):
		user = Userinfo(name=username, passwd=userpass, type=usertype)
		db.session.add(user)
		db.session.commit()
		insert_logs(session['user']['user'], "创建用户%s" % (username))
		return "1"
	else:
		return "0"


def insert_logs(name,action):
	now_str = time.strftime("%Y-%m-%d %H:%M:%S")
	logtime = datetime.strptime(now_str, "%Y-%m-%d %H:%M:%S")
	userlog=UserLog(name=name,action=action,time=logtime)
	db.session.add(userlog)
	db.session.commit()



def checkuser(username,userpass,usertype):
	username=username.replace(' ','')
	userpass=userpass.replace(' ','')
	if len(username)<8  or len(username)>20:
		print("username is invalid")
		return False
	if len(userpass)<8  or len(userpass)>20:
		print("userpass is invalid")
		return False
	if usertype not in ['0','1']:
		print("usertype is invalid")
		return False
	return True

@app.route("/deluser",methods=["POST"])
def deluser():
	username = request.form.get('username')
	if username == "admin":
	#if username == "sjz-jx":
		return "0"

	user = Userinfo.query.filter_by(name=username).first()
	db.session.delete(user)
	db.session.commit()
	insert_logs(session['user']['user'], "删除用户%s" %(username))
	return "1"


@app.route('/users',methods=['GET'])
def get_users():
	users = Userinfo.query.all()
	res=[]
	for user in users:
		obj=user.jsonstr()
		res.append(obj)
	return jsonify({'users':res})

@app.route('/getlocktime',methods=['GET'])
def getlocktime():
	username = request.args.get('username')
	user = Userinfo.query.filter_by(name=username).first()
	if user and user.locktime:
		locktime=user.locktime.strftime("%Y-%m-%d %H:%M:%S")
	else:
		locktime=None
	return jsonify({'username':username,'locktime':locktime})


@app.before_first_request
def process_first_request():
	m.loginame=""
	m.count=0
	m.loginmsg=""

@app.before_request
def process_request():
	no_handler_paths=["/","/login","/getlocktime"]
	if request.path in no_handler_paths:
 		return None
	static_urls=["js","images"]
	for str in static_urls:
		if request.path.find(str):
			return None
	if not session.get("user"):
	 	return redirect("/")

@app.after_request
def process_response(response):
	response.headers["Access-Control-Allow-Credentials"]="true";
	handlers=["/"]
	if request.path in handlers:
		m.loginame = ""
		m.count = 0
		m.loginmsg = ""

	return response


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

