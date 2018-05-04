# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 21:14:05 2017

@author: Ramakant
"""
import json, os
import shutil
from distutils.dir_util import copy_tree
from dbop import SQLiteDB as sqlitedb
#import shutil
from flask import Flask, render_template, request, redirect, session, abort
app = Flask(__name__, static_url_path='/images/')

@app.route("/")
def main():
    return "Welcome"

@app.route("/images")
def Authenticate():
    conn = sqlitedb.create_connection('ebite.sqlite')
    rows = sqlitedb.getAllPhotos(conn)
    columns = sqlitedb.getColumnName(conn)
    result = [{columns[index][0]:column for index, column in enumerate(value)}   for value in rows]
    final_result = result
    print(result)
    # final_result = json.loads(str(result))
    # print(final_result)
    #json_result = json.dumps(result)
    sqlitedb.closedb(conn)
    
    data = [{
            "Name":"Ramakant",
            "Name1":"Kushwaha",
            "Name2":"rk"
            },
            {
            "Name":"Ramakant",
            "Name1":"Kushwaha",
            "Name2":"rk"
            }]
    #print(json_result)
    if rows is None:
        print("Username or Password is wrong")
    else:  
        print("Logged in successfully")
    
    return render_template(
        'index.html',**locals())

# try:
#     path = "C:/Users/Ramakant/AnacondaProjects/opencvocr/WebApp/"
#     for dir in os.listdir(path):
#         if(dir == "static"):
#             shutil.rmtree(os.path.join(path, dir))
            
#     shutil.copytree("C:/Users/Ramakant/AnacondaProjects/opencvocr/outputdata/","C:/Users/Ramakant/AnacondaProjects/opencvocr/WebApp/static/")

# except :
#     print("error in copy images")
    
if __name__ == "__main__":
    app.run()
