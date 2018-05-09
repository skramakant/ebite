from __future__ import print_function
import json
import urllib.request
import urllib3
from urllib.parse import urlparse
import os
import twitter
from http.client import IncompleteRead
from dbop import SQLiteDB as db
from sklearn.externals import joblib
from imageclssification import ImageClS
import shutil
from firebase.Pfirebase import FirebaseDB
import time
import datetime

os.chdir(r"/home/ramakant/Desktop/Twitter_GovWok/")

current_milli_time = lambda: int(round(time.time() * 1000))

classifier = ImageClS("tmc_lbp_model.pkl","tmc_hog_model.pkl")

conn = db.create_connection('ebite.sqlite')

#firebase initialization 
fdb = FirebaseDB()
fdb.initializeFirebase()

def getfilename(url):
	url_path = urlparse(url).path
	filename = os.path.basename(url_path)
	return filename


# //https://github.com/bear/python-twitter
# https://python-twitter.readthedocs.io/en/latest/rate_limits.html

api = twitter.Api(consumer_key='TpECOVMlBvIJFKrqgIO85wN9h',
                  consumer_secret='bLhuvRueRqbF4Ay3DP8g0E3PacAonVO21OFzF4exi6o18nCSdD',
                  access_token_key='391328480-nzMffB2eAUJCPTtaYtmc0RmNgqg6zJc9uBo2QueU',
                  access_token_secret='8qtH2fGLY2r7JoFk2vLXuRuTULUqhuqzyFwM6kZV7L0Sq',
                  sleep_on_rate_limit=True)

# users = api.GetFriends()

# # print([u.screen_name for u in users])

# for user in users:
# 	#parsed = json.loads(str(user))
# 	#print(json.dumps(parsed,indent=4, sort_keys=True))
# 	print(user.screen_name)


USERS = ['@narendramodi','@BJP4India', '@BJP4UP', '@UPGovt', '@narendramodi_in', 
'@PiyushGoyal', '@PiyushGoyalOffc', '@myogiadityanath','@RailMinIndia','@MoHFW_INDIA',
'@TexMinIndia','@HRDMinistry','@HMOIndia',
'@CimGOI','@manojsinhabjp','@Rao_InderjitS','@DVSBJP','@shripadynaik','@rsprasad',
'@RadhamohanBJP','@arunjaitley','@dpradhanbjp',
'@Gen_VKSingh','@MVenkaiahNaidu','@umasribharti','@rajnathsingh',
'@PiyushGoyal','@PrakashJavdekar','@jualoram','@PMOIndia',
'@KalrajMishra','@AnanthKumar_BJP','@PIB_India','@SushmaSwaraj',
'@DrJitendraSingh','@sureshpprabhu','@smritiirani','@nitin_gadkari',
'@drharshvardhan','@Kiren_Rijiju','@Ra_THORe','@nsitharaman',
'@tourismgoi','@MinOfCultureGoI','@incredibleindia','@incredibleindia',
'@uptourismgov','@GujaratTourism','@APTDCofficial','@startupindia',
'@makeinindia','@mygovindia','@NITIAayog','@rashtrapatibhvn','@MIB_India',
'@MinistryWCD','@MinOfPower','@minmsme','@investindia','@MSDESkillIndia',
'@NSDCINDIA','@grameenvidyut','@mnreindia','@GoI_MeitY','@UIDAI','@DoT_India','@CSCegov_',
'@PMGDISHA','@NIELITIndia','@NICMeity','@DIPPGOI','@MinOfCultureGoI','@AgriGoI',
'@YASMinistry','@DIPPGOI','@MSJEGOI','@MORTHIndia','@LabourMinistry','@Electronics_GoI','@MOFPI_GOI',
'@IncomeTaxIndia','@moefcc','@DRDO_India','@IndiaPostOffice',
'@DataPortalIndia','@SwachhBharatGov','@DoC_GoI','@dgftindia','socialpwds','@MinistryWCD']

myuser_id = '391328480'
MYUSER_ID = ['391328480']


# Languages to filter tweets by is a list. This will be joined by Twitter
# to return data mentioning tweets only in the english language.
LANGUAGES = ['en']

# UserListIDs = open("../output.txt").readlines()

UserListIDs = []

for ids in api.GetFriendIDs():
	UserListIDs.append(str(ids))

UserListIDs.append(myuser_id)
print(len(UserListIDs))
# print(UserListIDs)


i=0

# for line in api.GetFriendIDs():#GetFriends(),GetFriendIDs()
# 	parsed = json.loads(str(line))
# 	print(json.dumps(parsed,indent=4, sort_keys=True))


UserListName = []
for user in api.GetFriends():
	UserListName.append(user.screen_name)

while(1):
	try:	
		for line in api.GetStreamFilter(track=None,follow = UserListIDs, languages=None):
			# print(line)
			screenName = ''
			if 'user' in line:
				screenName = line['user']['screen_name']
				# print(screenName) 

			if 'retweeted_status' in line:
				# print(line['extended_entities'])
				tweet = line['retweeted_status']
				screenName = tweet['user']['screen_name']

				if 'user' in tweet:
					# if retweet['user']['screen_name'] in UserListName:
					if 'extended_tweet' in tweet:
						retweet = line['retweeted_status']['extended_tweet']
						if 'extended_entities' in retweet:
							# print(line['extended_entities'])
							print("HAVE MEDIA in extended_tweet")
							medias = retweet['extended_entities']['media']
							for media in medias:
								url = media['media_url_https']
								# print(url)
								# urllib.request.urlretrieve(url,'images/'+screenName + "_" + str(i) + ".jpg")

								if(media['type'] == 'video'):
									print("VIDEO FOUND")
									videoInfo = media['video_info']

									bitrate = -100
									for vurl in videoInfo['variants']:
										if 'bitrate' in vurl:
											if(bitrate < vurl['bitrate']):
												bitrate = vurl['bitrate']

									for vurl in videoInfo['variants']:
										if 'bitrate' in vurl:
											if(bitrate == vurl['bitrate']):
												video_url = vurl['url']
												filename = getfilename(video_url)
												path = 'videos/'+screenName + "_" + filename
												if(os.path.exists(path) == True):
													print("Video File Already Exists {} {}".format(screenName,filename))
												else:
													print("video downloding")
													# urllib.request.urlretrieve(video_url,'videos/'+screenName + "_" + filename)

									# video_url = videoInfo['variants'][3]['url']
									# urllib.request.urlretrieve(video_url,'videos/'+screenName + "_" + str(i) + ".mp4")
								else:
									filename = getfilename(url)
									path = 'images/positive/'+screenName + "_" + filename
									nagativepath = 'images/negative/'+screenName + "_" + filename
									if(os.path.exists(path) == True or os.path.exists(nagativepath) == True):
										print("Image File Already Exists {} {}".format(screenName,filename))
									else:
										db.create_photos_table(conn)
										localurl = 'images/'+screenName + "_" + filename
										ttext = retweet['full_text']
										date = tweet['created_at']
										photo = (str(url),localurl,str(ttext),screenName,date)
										# rowid = db.insert_photo(conn,photo)
										# print("rowid",rowid)
										urllib.request.urlretrieve(url,"temp.jpg")#localurl
										# print(photo)
										# lbpresult = classifier.hasTextLBP("temp.jpg")
										hogresult = classifier.hasTextHOG("temp.jpg")
										print(hogresult)
										if(hogresult == 'positive'):
											# os.rename('temp.jpg',path)
											shutil.copy('temp.jpg', path)
											firebase_item = {}
											firebase_item['imageTweet'] = ttext
											firebase_item['imageTweetHandle'] = screenName
											firebase_item['imageUrl'] = url
											firebase_item['tweetTime'] = date
											firebase_item['systemTime'] = str(datetime.datetime.now())
											nodename = ((screenName + '_' + filename).split('.'))[0]
											# print(firebase_item)
											fdb.insertTweet(nodename,firebase_item)
										else:
											# os.rename('temp.jpg',nagativepath)
											#shutil.copy('temp.jpg', nagativepath)
											print("negative image")

								
								i=i+1
						else:
							print("no media extended_tweet")		


			elif 'extended_entities' in line:
				# print(line['extended_entities'])
				print(line)
				print("HAVE MEDIA in extended_entities")
				medias = line['extended_entities']['media']
				for media in medias:
					url = media['media_url_https']
					# print(url)
					# urllib.request.urlretrieve(url,'images/'+screenName + "_" + str(i) + ".jpg")

					if(media['type'] == 'video'):
						print("VIDEO FOUND")
						videoInfo = media['video_info']

						bitrate = -100
						for vurl in videoInfo['variants']:
							if 'bitrate' in vurl:
								if(bitrate < vurl['bitrate']):
									bitrate = vurl['bitrate']

						for vurl in videoInfo['variants']:
							if 'bitrate' in vurl:
								if(bitrate == vurl['bitrate']):
									video_url = vurl['url']
									filename = getfilename(video_url)
									path = 'videos/'+screenName + "_" + filename
									if(os.path.exists(path) == True):
										print("Video File Already Exists {} {}".format(screenName,filename))
									else:
										print("video downloding")
										# urllib.request.urlretrieve(video_url,'videos/'+screenName + "_" + filename)


						# video_url = videoInfo['variants'][3]['url']
						# urllib.request.urlretrieve(video_url,'videos/'+screenName + "_" + str(i) + ".mp4")
					else:
						filename = getfilename(url)
						path = 'images/'+screenName + "_" + filename
						if(os.path.exists(path) == True):
							print("Image File Already Exists {} {}".format(screenName,filename))
						else:
							# urllib.request.urlretrieve(url,'images/'+screenName + "_" + filename)
							db.create_photos_table(conn)
							localurl = 'images/'+screenName + "_" + filename
							ttext = ''
							if "full_text" in line['extended_entities']:
								ttext = line['extended_entities']['full_text']
							if "text" in line['extended_entities']:
								ttext = line['extended_entities']['text']
							date =''
							if 'user' in line['extended_entities']:
								date = line['extended_entities']['user']['created_at']
							if 'created_at' in line['extended_entities']:
								date = line['extended_entities']['created_at']
							photo = (str(url),localurl,str(ttext),screenName,date)
							# rowid = db.insert_photo(conn,photo)
							# print("rowid",rowid)
							# urllib.request.urlretrieve(url,localurl)					

					i=i+1
			else:
				print("no extended_entities")


			print(i)
	except urllib.IncompleteRead as err:
		print(err)
	except urllib.HTTPError as err:
		if(err.code == 404):
			print("NOT FOUND 404")
	except urllib3.ProtocolError as err:
		print(err)
	except urllib.ChunkedEncodingError as err:
		print(err)
db.closedb(conn)


