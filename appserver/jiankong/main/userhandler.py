#!/usr/bin/env python
# -*- coding:utf-8 -*-
#author yanxianghui
import os
from jiankong.main import commons as m
import json
import yaml
import xlrd


def get_sitesyamlfile():
	dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	sitefile = os.path.join(dir_name,"static","files","site.yaml")
	with open(sitefile, 'rb') as f:
		temp = yaml.load(f.read())
	return temp["sites"]

def get_sitesexcelfile():
	dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	sitefile = os.path.join(dir_name,"static","files","sites.xlsx")
	workbook = xlrd.open_workbook(sitefile)
	tables = workbook.sheets()
	sites = []
	for table in tables:
		nrows = table.nrows
		site = {"name": table.name, "data": None}
		site["data"] = []  # 站名
		for i in range(nrows):
			if i > 1:
				if table.row_values(i)[1]:
					guizi = {}
					itemlist = []
					guizi["guizi"] = table.row_values(i)[1]
					guizi["items"] = itemlist
					site["data"].append(guizi)
					continue
				if table.row_values(i)[2]:
					itemlist.append({"po": table.row_values(i)[2], "pv": table.row_values(i)[3]})
					continue
		sites.append(site)
	return sites

# sheet = ExcelFile.sheet_by_index(0)
	# flag = False
	# sites = []
	# for i in sheet.get_rows():
	# 	if flag:
	# 		if i[0].value:
	# 			site = {"name": None, "cabinets": []}
	# 			site["name"] = i[0].value
	# 			sites.append(site)
	# 		if i[1].value:
	# 			cabinet = {"name": None, "numbers": []}
	# 			cabinet["name"] = i[1].value
	# 			site["cabinets"].append(cabinet)
	# 		if i[2].value:
	# 			cabinet["numbers"].append(i[2].value)
	# 	flag = True
	# return sites

def upload_excelfile(f,sitename,templateName):
	sitename = sitename.encode('utf-8').decode('utf-8-sig')
	dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	excelfile_path = os.path.join(dir_name, "static","files","excel",sitename,templateName,f.filename)
	f.save(excelfile_path)


def upload_sitetxt(f):
	dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	sitetxt_path = os.path.join(dir_name,"static","files","site.txt")
	f.save(sitetxt_path)
	print("保存文件成功")

def upload_sitesexcel(f):
	dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	sitetxt_path = os.path.join(dir_name,"static","files","sites.xlsx")
	f.save(sitetxt_path)
	print("保存excel文件成功")


def initexceldir():
	sites = get_sitesyamlfile()
	dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	for item in sites:
		LA_exceldir_path = os.path.join(dir_name, "static","files","excel",item.strip('\n'),"LA")
		CT_exceldir_path = os.path.join(dir_name, "static","files","excel",item.strip('\n'),"CT")

		if os.path.exists(LA_exceldir_path):
			print(LA_exceldir_path+"已经存在.....")
		else:
			os.makedirs(LA_exceldir_path)

		if os.path.exists(CT_exceldir_path):
			print(CT_exceldir_path + "已经存在.....")
		else:
			os.makedirs(CT_exceldir_path)


def getexcellist(sitename,templateName):
	dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	site_dir_path = os.path.join(dir_name,"static","files","excel",sitename,templateName)
	filelist=[]
	for filename in os.listdir(site_dir_path):
		filePath = os.path.join(site_dir_path,filename)
		t = os.path.getctime(filePath)
		fileobj={"fname":filename,"ftime":m.TimeStampToTime(t),"sitename":sitename,"templatename":templateName}
		filelist.append(fileobj)
	return filelist


def deletefile(sitename,filename,templateName):
	dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	file_path = os.path.join(dir_name, "static", "files", "excel", sitename,templateName,filename)
	os.remove(file_path)


def renamefile(sitename,filename,templateName):
	dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	old_file_path = os.path.join(dir_name, "static", "files", "excel", sitename,templateName,filename)
	new_file_path = os.path.join(dir_name, "static", "files", "excel", sitename,templateName,"基准数据.xls")
	os.rename(old_file_path, new_file_path)


def sitebak():
	pass


def save_phoneexcel(sitename,data):
	pass

def get_phonebasedata(sitename):
	pass

def save_phoneexcelct(sitename,data):
	pass









