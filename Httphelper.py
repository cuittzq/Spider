# coding=utf-8
__author__ = 'tzq'
import urllib
import urllib2
import re
import tool
import dbheper
from dbheper import *
import os
import time;
import threading;


class Meituiwang:
    def __init__(self):
        self.siteURL = 'http://www.4493.com/siwameitui/index-2.htm'
        self.tool = tool.Tool()