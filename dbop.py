#!/usr/bin/python
 
import sqlite3
from sqlite3 import Error
 
 
class SQLiteDB():
 	def __init__(self):
 		print("init")

 	def create_connection(db_file):
 		try:
 			conn = sqlite3.connect(db_file)
 			return conn
 		except Error as e:
 			print(e)
 		return None

 	def create_photos_table(connection):
 		cursor = connection.cursor()
 		cursor.execute('''CREATE TABLE IF NOT EXISTS photos(id INTEGER PRIMARY KEY, imageweburl TEXT,
		                       imagelocalurl TEXT, imagetext TEXT , imageowner TEXT, imagedate TEXT)''')
 		connection.commit()

 	def closedb(conn):
 		conn.close()

 	def getAllPhotos(conn):
 		cursor = conn.cursor()
 		query = '''SELECT * FROM photos'''
 		cursor.execute(query)
 		all_rows = cursor.fetchall()
 		return all_rows

 	def getColumnName(conn):
 		cursor = conn.cursor()
 		query = '''SELECT * FROM photos'''
 		cursor.execute(query)
 		return cursor.description

 	def insert_photo(conn,task):
	    sql = '''INSERT INTO photos(imageweburl,imagelocalurl,imagetext,imageowner,imagedate) VALUES(?,?,?,?,?)'''
	    cur = conn.cursor()
	    cur.execute(sql, task)
	    return cur.lastrowid

