#!/usr/bin/python3
import os

modules = ['paramiko']
try:
    os.system(f"pip3 install {' '.join(modules)}")
except:
    print("")