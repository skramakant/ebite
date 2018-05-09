import argparse
import cv2
from skimage import feature
import numpy as np
from imutils import paths
from sklearn.externals import joblib

numPoints = 24 
radius = 8


class ImageClS():
	def __init__(self,LBPmodelfile,HOGmodelfile):
		self.LBPmodel = joblib.load(LBPmodelfile)
		self.HOGmodel = joblib.load(HOGmodelfile)
		print("ImageClS Initialize")
		# store the number of points and radius
		self.numPoints = numPoints
		self.radius = radius

	def hasTextLBP(self,imagePath):
		image = cv2.imread(imagePath)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		hist = self.describe(gray)
		hist = hist.reshape(1,26)
		#print(hist.shape)
		prediction = self.LBPmodel.predict(hist)[0]
		return prediction

	def hasTextHOG(self,imagePath):
		image = cv2.imread(imagePath)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		logo = cv2.resize(gray, (200, 100))
		(H, hogImage) = feature.hog(logo, orientations=9, pixels_per_cell=(10, 10),
			cells_per_block=(2, 2), transform_sqrt=True, block_norm="L1", visualise=True)
		pred = self.HOGmodel.predict(H.reshape(1, -1))[0]
		return pred

	def describe(self, image, eps=1e-7):
		# compute the Local Binary Pattern representation
		# of the image, and then use the LBP representation
		# to build the histogram of patterns
		lbp = feature.local_binary_pattern(image, self.numPoints,
			self.radius, method="uniform")
		(hist, _) = np.histogram(lbp.ravel(),
			bins=np.arange(0, self.numPoints + 3),
			range=(0, self.numPoints + 2))

		# normalize the histogram
		hist = hist.astype("float")
		hist /= (hist.sum() + eps)

		# return the histogram of Local Binary Patterns
		return hist	
