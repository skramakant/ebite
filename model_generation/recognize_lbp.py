# USAGE
# python recognize.py --training images/training --testing images/testing

# import the necessary packages
from pyimagesearch.localbinarypatterns import LocalBinaryPatterns
from sklearn.svm import LinearSVC
from imutils import paths
import argparse
import cv2
from sklearn.externals import joblib

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--training", required=True,
	help="path to the training images")
ap.add_argument("-e", "--testing", required=True, 
	help="path to the tesitng images")
args = vars(ap.parse_args())

# initialize the local binary patterns descriptor along with
# the data and label lists
desc = LocalBinaryPatterns(24, 8)
data = []
labels = []
i=0
# loop over the training images
for imagePath in paths.list_images(args["training"]):
	# load the image, convert it to grayscale, and describe it
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	hist = desc.describe(gray)

	# extract the label from the image path, then update the
	# label and data lists
	labels.append(imagePath.split("/")[-2])
	data.append(hist)
	i=i+1
	print(i)
	# if(i==960):
	# 	break

# train a Linear SVM on the data
model = LinearSVC(C=100.0, random_state=42)
print(labels)
model.fit(data, labels)
joblib.dump(model, 'tmc_lbp_model.pkl') 
# loop over the testing images
for imagePath in paths.list_images(args["testing"]):
	# load the image, convert it to grayscale, describe it,
	# and classify it
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	hist = desc.describe(gray)
	hist = hist.reshape(1,26)
	#print(hist.shape)
	prediction = model.predict(hist)[0]

	# display the image and the prediction
	cv2.putText(image, prediction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
		1.0, (0, 0, 255), 3)
	cv2.imshow("Image", image)
	cv2.waitKey(0)