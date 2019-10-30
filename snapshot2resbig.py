import cv2 
cap1 = cv2.VideoCapture(1)
ret=cap1.set(3,1280)#width
ret=cap1.set(4,480)#height
cap1.set(cv2.CAP_PROP_FPS, 60);# 帧率 帧/秒
fps =cap1.get(cv2.CAP_PROP_FPS) #获取视频帧数
print(fps)
framecnt=0
while (cap1.isOpened()):
    ret1, frame1 = cap1.read()
    
    imgL = frame1[0:480,0:640]# 坐标：[Ly:Ry , Lx:Rx]
    imgR = frame1[0:480,640:1280]# 裁剪坐标为[y0:y1, x0:x1]
    cv2.imshow("left", imgL)
    cv2.imshow("right", imgR)
        
    key = cv2.waitKey(1)

    if key & 0x00FF  == ord('q'):
        break
    if key & 0x00FF == ord('s'):
        str1='snapshot/video1left_frame'+str(framecnt)+'.bmp'
        str2='snapshot/video1right_frame'+str(framecnt)+'.bmp'
        cv2.imwrite(str1, imgL)
        cv2.imwrite(str2, imgR)
        framecnt+=1
        print(framecnt)
        
cap1.release()
cv2.destroyAllWindows()
