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


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.debug = True


@app.route('/index',methods=['GET'])
def index():
	return send_file("static/pages/sitetable.html")

@app.route('/')
def main():
	return render_template('index.html', msg=m.loginmsg)

@app.route('/login',methods=['POST'])
def login():
	loginame = request.form.get('loginuser')
	loginpwd = request.form.get('loginpwd')
	result = userhandler.checkuser(loginame, loginpwd)
	if result:
		session['user'] = {'user':loginame,'type':result[0][2]}
		m.loginmsg=""
		return redirect("/index")
	m.loginmsg="登录失败"
	return redirect("/")


@app.route("/logout",methods=["GET"])
def logout():
	session.pop('user')  # 删除session
	session.clear()      # 清除所有session
	return redirect("/")


@app.route('/site',methods=['GET'])
def get_sites():
	sites = userhandler.get_sitesexcelfile()
	return jsonify({'sites': sites})

@app.route('/phone/site',methods=['GET'])
def get_phonesites():
	sites = userhandler.get_sitesyamlfile()
	return jsonify({'sites': sites})


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


@app.route("/renamebase",methods=['GET'])
def renamefile():
	sitename =  unquote(unquote(request.args.get("sitename")))
	filename =  unquote(unquote(request.args.get("filename")))
	templateName = request.args.get("templateName")
	userhandler.renamefile(sitename, filename, templateName)
	return "success"

@app.route("/baksite",methods=['GET'])
def baksite():
	userhandler.sitebak()
	return "success"

@app.route("/getusertype",methods=["GET"])
def getusertype():
	user_dict={}
	user_dict["username"]=session["user"]["user"]
	user_dict["usertype"]=session["user"]["type"]
	return json.dumps(user_dict)


@app.route("/updateuserpasswd",methods=["POST"])
def updatepasswd():
	newpwd = request.form.get('newpwd')
	username=session["user"]["user"]
	result = userhandler.updateuserpasswd(username, newpwd)
	if result:
		return "1"
	else:
		return "0"

@app.route("/adduser",methods=["POST"])
def adduser():
	username=request.form.get('username')
	userpass=request.form.get('userpass')
	usertype=request.form.get('usertype')
	result = userhandler.adduser(username, userpass,usertype)
	if result:
		return "1"
	else:
		return "0"


@app.route("/deluser",methods=["POST"])
def deluser():
	username = request.form.get('username')
	result = userhandler.deluser(username)
	if result:
		return "1"
	else:
		return "0"


@app.route('/users',methods=['GET'])
def get_users():
	users = userhandler.get_users()
	return jsonify({'users': users})

@app.route('/phone/save',methods=['POST'])
def phonesaveexcel():
	sitename = request.form.get('sitename')
	sitename = unquote(unquote(sitename))
	data = request.form.get("data")
	userhandler.save_phoneexcel(sitename, data)
	return "success"


@app.route('/phone/basedata',methods=['GET'])
def getbasedatabyexcel():
	sitename = request.args.get("sitename")
	sitename = unquote(unquote(sitename))
	return userhandler.get_phonebasedata(sitename)


@app.route('/phone/savect',methods=['POST'])
def phonesavect():
	sitename = request.form.get('sitename')
	sitename = unquote(unquote(sitename))
	data = request.form.get("data")
	userhandler.save_phoneexcelct(sitename, data)
	return "success"




@app.before_request
def process_request():
	if request.path == "/" or request.path== "/login" or "/phone" in request.path:
		return None
	if not session.get("user"):
		return redirect("/")

@app.after_request
def process_response(response):
	response.headers["Access-Control-Allow-Credentials"]="true";
	return response


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

