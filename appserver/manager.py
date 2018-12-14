#!/usr/bin/env python
# -*- coding=utf8-*-
#author yanxianghui

from app import app 
from main.dbutils import dbtool

db = dbtool()
db.init_db()

if __name__ == "__main__":
	db=dbtool()
	db.init_db()
	app.run("0.0.0.0")

