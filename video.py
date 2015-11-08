import cv2

def createvideo():
    image = cv2.imread('video0.png')
    height , width , layers =  image.shape

    video = cv2.VideoWriter('video.avi',-1,1,(width,height))

    video.write(image)

    for i in range(1 , 100):
        image = cv2.imread('video' + `i` + '.png')
        video.write(image)
    

    cv2.destroyAllWindows()
    video.release()


createvideo()
