#!/usr/bin/env python
# -*- coding:utf-8 -*-


from flask import Blueprint
from flask import render_template
from flask import request,jsonify
from flask import Flask,render_template,request,redirect,session
import json
from jiankong.model.appmodel import Userinfo
from jiankong.main.dbutils import insert_logs

from datetime import date,datetime
from datetime import timedelta
import time

from jiankong import db
user = Blueprint('usersview', __name__)


@user.route("/getusertype",methods=["GET"])
def getusertype():
	user_dict={}
	user_dict["username"]=session["user"]["user"]
	user_dict["usertype"]=session["user"]["type"]
	user_dict["redays"]=session["user"]["days"]
	return json.dumps(user_dict)

@user.route("/updateuserpasswd",methods=["POST"])
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

@user.route("/adduser",methods=["POST"])
def adduser():
	username=request.form.get('username')
	userpass=request.form.get('userpass')
	usertype=request.form.get('usertype')

	#result = userhandler.adduser(username, userpass,usertype)
	if checkuser(username,userpass,usertype):
		user = Userinfo(name=username, passwd=userpass, type=usertype)
		db.session.add(user)
		db.session.commit()
		return "1"
	else:
		return "0"


@user.route("/deluser",methods=["POST"])
def deluser():
	username = request.form.get('username')
	if username == "admin":
	#if username == "sjz-jx":
		return "0"

	user = Userinfo.query.filter_by(name=username).first()
	db.session.delete(user)
	db.session.commit()
	return "1"



@user.route('/users',methods=['GET'])
def get_users():
	users = Userinfo.query.all()
	res=[]
	for user in users:
		obj=user.jsonstr()
		res.append(obj)
	return jsonify({'users':res})