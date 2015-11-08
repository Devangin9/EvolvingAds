# http://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/

import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import math

class Hsvcolors:

    def findcolorclusters(self, image, clustercount):
        #hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        hsv = image    
	
        # reshape the image to be a list of pixels
        image = hsv.reshape((hsv.shape[0] * hsv.shape[1], 3))

        # cluster the pixel intensities
        clt = KMeans(n_clusters = clustercount)
        clt.fit(image)

        hist = self.centroid_histogram(clt)
        bar = self.plot_colors(hist, clt.cluster_centers_)
        return clt.cluster_centers_


    def centroid_histogram(self, clt):
	    # grab the number of different clusters and create a histogram
	    # based on the number of pixels assigned to each cluster
	    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	    (hist, _) = np.histogram(clt.labels_, bins = numLabels)
     
	    # normalize the histogram, such that it sums to one
	    hist = hist.astype("float")
	    hist /= hist.sum()
     
	    # return the histogram
	    return hist

    def plot_colors(self, hist, centroids):
	    # initialize the bar chart representing the relative frequency
	    # of each of the colors
	    bar = np.zeros((50, 300, 3), dtype = "uint8")
	    startX = 0
     
	    # loop over the percentage of each cluster and the color of
	    # each cluster
	    for (percent, color) in zip(hist, centroids):
		    # plot the relative percentage of each cluster
		    endX = startX + (percent * 300)
		    cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
			    color.astype("uint8").tolist(), -1)
		    startX = endX
	
	    # return the bar chart
	    return bar

    def findColorDistance(self, centers1, centers2):
        #take each pair of centers
        maxdist = 0    
        for i in range( 1, len(centers1)):
            mindist = 100000
            for j in range( 1 , len(centers2)):
                diff1  = abs(centers1[i][0] - centers2[j][0])
                diff2 = abs(centers1[i][1] - centers2[j][1])
                diff3 = abs(centers1[i][2] - centers2[j][2])
                distance = math.sqrt( diff1*diff1 + diff2*diff2 + diff3*diff3)
                if distance < mindist:
                    mindist = distance

            if mindist > maxdist:
                maxdist = mindist
        print maxdist
        return maxdist


    def findOptimalClusters(self, image):
        lastcenters = self.findcolorclusters(image, 2)
        closedistance = 50 #50
        for i in range(3,  8):
            centers = self.findcolorclusters(image, i)
            distance = self.findColorDistance(lastcenters, centers)
            if distance <= closedistance:
                break

            lastcenters = centers

        return lastcenters



    def getColorlists(self, image, clusters = -1):
        if clusters == -1:
            centers = self.findOptimalClusters(image)
        else:
            centers = self.findcolorclusters(image, clusters)
        colors = []
        for i in range( 1 , len(centers)):
            colors.append((centers[i][0], centers[i][1], centers[i][2]))
        return colors

#image = cv2.imread('image7.png')
#print Hsvcolors().findOptimalClusters(image)
