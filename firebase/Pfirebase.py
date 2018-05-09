import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# cred = credentials.Certificate("path/to/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)


# Fetch the service account key JSON file contents
cred = credentials.Certificate('firebase/ebite-6d50b-firebase-adminsdk-4fwm8-f5e00f38e1.json')

class FirebaseDB():
	def __init__(self):
		print("FirebaseDB")

	def initializeFirebase(self):
		firebase_admin.initialize_app(cred, {
		    'databaseURL': 'https://ebite-6d50b.firebaseio.com/'
		})
		self.dbref = db.reference('ebitedb')


	def insertTweet(self, node, data):
		self.dbref.child(node).set(data)

# As an admin, the app has access to read and write all data, regradless of Security Rules
# dbref = db.reference('ebitedb')
# print(dbref.get())

# for i in range(0,10):
# 	dbref.push().set({'thandle': 'bjpindia', 'itime': 437476346466, 'imageurl': 'https://www.google.com/',
# 	 'categeory': 1, 'ttext': 'bjp karnataka', 'ttime': 563636633633, 'lflag': 2})
