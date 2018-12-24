#!/usr/bin/env python
# -*- coding:utf-8 -*-
#author yanxianghui

import time
import datetime
import os
import json
from decimal import *


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

def getexceldirName():
    dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_path = os.path.join(dir_name, "static", "files", "excel")
    return excel_path






