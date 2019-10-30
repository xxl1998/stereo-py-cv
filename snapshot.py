import numpy as np
import cv2

camera = cv2.VideoCapture(1)#
ret=camera.set(3,1280)#width
ret=camera.set(4,480)#height
fps =camera.get(cv2.CAP_PROP_FPS) #获取视频帧数
print(fps)
while True:
    ret, frame = camera.read()
    if not ret:
        break
    #frame = cv2.flip(frame,0,dst=None)
    imgL = frame[0:480,0:640]# 坐标：[Ly:Ry , Lx:Rx]
    imgR = frame[0:480,640:1280]# 裁剪坐标为[y0:y1, x0:x1]
    
    cv2.imshow("left", imgL)
    cv2.imshow("right", imgR)
    cv2.imshow('frame',frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    elif key == ord("s"):
        print("save")
        cv2.imwrite("snapshot/left.png", imgL)
        cv2.imwrite("snapshot/right.png", imgR)

camera.release()
cv2.destroyAllWindows()
