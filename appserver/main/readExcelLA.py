#!/usr/bin/env python
# -*- coding:utf-8 -*-
#author yanxianghui


import xlrd
import os
import json
import commons

def read_excel(sitename):
    excel_dirname = commons.getexceldirName()
    filename = os.path.join(excel_dirname, sitename,"LA","基准数据.xls")
    workbook = xlrd.open_workbook(filename)
    table = workbook.sheets()[0]
    nrows = table.nrows

    data=[]
    for i in range(nrows):
        if i>1:
            number = table.row_values(i)[5]
            if number:
                item = {"number":number,"data":[[table.row_values(i)[7],table.row_values(i)[8],table.row_values(i)[9],table.row_values(i)[10]],[table.row_values(i+1)[7],table.row_values(i+1)[8],table.row_values(i+1)[9],table.row_values(i+1)[10]],[table.row_values(i+2)[7],table.row_values(i+2)[8],table.row_values(i+2)[9],table.row_values(i+2)[10]]]}
                data.append(item)

    return json.dumps(data)


