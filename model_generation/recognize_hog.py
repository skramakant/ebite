# import the necessary packages
from sklearn.neighbors import KNeighborsClassifier
from skimage import exposure
from skimage import feature
from imutils import paths
import argparse
import imutils
import cv2
from sklearn.externals import joblib
 
# construct the argument parse and parse command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--training", required=True, help="Path to the logos training dataset")
ap.add_argument("-t", "--test", required=True, help="Path to the test dataset")
args = vars(ap.parse_args())
 
# initialize the data matrix and labels
print ("[INFO] extracting features...")
data = []
labels = []
i=0
# loop over the image paths in the training set
for imagePath in paths.list_images(args["training"]):
	# extract the make of the car
	make = imagePath.split("/")[-2]
 
	# load the image, convert it to grayscale, and detect edges
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	logo = cv2.resize(gray, (200, 100))
 
	# extract Histogram of Oriented Gradients from the logo
	H = feature.hog(logo, orientations=9, pixels_per_cell=(10, 10),
		cells_per_block=(2, 2), transform_sqrt=True, block_norm="L1")
 
	# update the data and labels
	data.append(H)
	labels.append(make)

	# "train" the nearest neighbors classifier
	print("[INFO] training classifier...")
	model = KNeighborsClassifier(n_neighbors=1)
	model.fit(data, labels)
	i=i+1
	print(i)

joblib.dump(model, 'tmc_hog_model.pkl')
# model = joblib.load('tmc_hog_model.pkl')

# loop over the test dataset
for (i, imagePath) in enumerate(paths.list_images(args["test"])):
	# load the test image, convert it to grayscale, and resize it to
	# the canonical size
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	logo = cv2.resize(gray, (200, 100))
 
	# extract Histogram of Oriented Gradients from the test image and
	# predict the make of the car
	(H, hogImage) = feature.hog(logo, orientations=9, pixels_per_cell=(10, 10),
		cells_per_block=(2, 2), transform_sqrt=True, block_norm="L1", visualise=True)
	pred = model.predict(H.reshape(1, -1))[0]
 
	# visualize the HOG image
	hogImage = exposure.rescale_intensity(hogImage, out_range=(0, 255))
	hogImage = hogImage.astype("uint8")
	cv2.imshow("HOG Image #{}".format(i + 1), hogImage)
 
	# draw the prediction on the test image and display it
	cv2.putText(image, pred.title(), (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
		(0, 255, 0), 3)
	cv2.imshow("Test Image #{}".format(i + 1), image)
	cv2.waitKey(0)