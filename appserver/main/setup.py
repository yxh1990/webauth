#!/usr/bin/env python
# -*- coding:utf-8 -*-
#author yanxianghui

filename = "userhandler.py"

print("--------------------------------------")
print(" python build.py build_ext --inplace")
print("--------------------------------------")

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import sys

efile = filename.split('.')[0]

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension("%s" % efile, ["%s" % filename])]
)