import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('ebite-6d50b-firebase-adminsdk-4fwm8-f5e00f38e1.json')

class FirebaseDB():
	def __init__(self):
		# Initialize the app with a service account, granting admin privileges
		firebase_admin.initialize_app(cred, {
		    'databaseURL': 'https://ebite-6d50b.firebaseio.com/'
		})

		self.dbref = db.reference('ebitedb')

	def insertTweet(self,node,tweet):
		self.dbref.child(node).set(tweet)