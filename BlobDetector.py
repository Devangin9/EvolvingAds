# http://www.learnopencv.com/blob-detection-using-opencv-python-c/

import cv2
import numpy as np

def detectblobs(image):

    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()
     
    # Change thresholds
    #params.minThreshold = 10;
    #params.maxThreshold = 200;
     
    # Filter by Area.
    params.filterByArea = True
    params.minArea = 300
     
    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.5
     
    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.5
     
    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.01
     
    # Create a detector with the parameters
    #ver = (cv2.__version__).split('.')
    #if int(ver[0]) < 3 :
    detector = cv2.SimpleBlobDetector(params)
    #else : 
    #    detector = cv2.SimpleBlobDetector_create(params)
    #detector = cv2.SimpleBlobDetector()
 
    # Detect blobs.
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    keypoints = detector.detect(gray_image)
     
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    return im_with_keypoints
     
# http://docs.opencv.org/master/da/df5/tutorial_py_sift_intro.html
def detectSIFTblobs(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    sift = cv2.xfeatures2d.SIFT_create()
    kp = sift.detect(gray,None)
    
    img=cv2.drawKeypoints(gray,kp)
    return img


def detectContours(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)   

    #blur
    gray = cv2.GaussianBlur(gray, (5, 5), 1)
 
    thrs1 = 10
    thrs2 = 100
    edge = cv2.Canny(gray, thrs1, thrs2, apertureSize=5)
    cv2.imwrite('edges.png', edge) 

    contours0, hierarchy = cv2.findContours( edge.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in contours0]

    print len(contours)
        
    return len(contours)
    

#image = cv2.imread('image2.png')
#image2 = detectblobs(image)
#image2 = detectSIFTblobs(image)
#blobs = detectContours(image)
#cv2.imwrite('blobs.png', image2) 
