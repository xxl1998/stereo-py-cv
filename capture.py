import cv2
import numpy as np
import pickle
import time
#import matplotlib.pyplot as plt

cap = cv2.VideoCapture(1)
ret=cap.set(3,1280)#width
ret=cap.set(4,480)#height
fps =cap.get(cv2.CAP_PROP_FPS) #获取视频帧数
print(fps)
while True:
    start = time.time()
    ret,frame = cap.read()
    frame = cv2.flip(frame,0,dst=None)
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv2.imshow('gray',gray)
    cv2.imshow('frame',frame)
    end = time.time()
    dt = end - start
    if(dt>0):
        fps = 1/dt
        #print(fps)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
