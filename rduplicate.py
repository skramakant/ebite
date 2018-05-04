from __future__ import print_function
import json
import urllib.request
import os
# import the necessary packages
from PIL import Image
import imagehash
import argparse
import shelve
import glob


os.chdir(r"/home/ramakant/Desktop/Twitter_GovWok/")



# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--images", required = True,
    help = "path to input dataset of images")
ap.add_argument("-s", "--database", required = True,
    help = "output shelve database")
args = vars(ap.parse_args())

# open the shelve database
db = shelve.open(args["database"], writeback = True)
i=0
# loop over the image dataset
for imagePath in glob.glob(args["images"] + "/*.jpg"):

    # load the image and compute the difference hash

   	image = Image.open(imagePath)
   	filename = imagePath[imagePath.rfind("/") + 1:]
   	h = str(imagehash.dhash(image))
   	
   	if(h in db):
   		filenames = db[h]
   		if(len(filenames) != 0):
   			print("file names present size")
   		print("duplicate image")
   		print(filenames)
   		os.remove(imagePath)
   		print(i)
   		i=i+1
   	else:
   		db[h] = db.get(h,[]) + [filename]

   	# if(len(filenames) == 0):
   	# 	db[h] = db.get(h,[]) + [filename]
   	# else:
   	# 	print("duplicate image found")
   	# 	print(filename)
   	# 	print(i)
   	# 	i=i+1

# close the shelf database
db.close()