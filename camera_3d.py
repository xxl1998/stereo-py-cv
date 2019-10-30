import numpy as np
import cv2
import camera_configs
import time
cv2.namedWindow("left")
cv2.namedWindow("right")
cv2.namedWindow("depth")
cv2.moveWindow("left", 0, 0)
cv2.moveWindow("right", 600, 0)
cv2.createTrackbar("num", "depth", 0, 10, lambda x: None)
cv2.createTrackbar("blockSize", "depth", 5, 255, lambda x: None)

camera = cv2.VideoCapture(1)#640*240
ret=camera.set(3,1280)#width
ret=camera.set(4,480)#height
camera.set(cv2.CAP_PROP_FPS, 60);# 帧率 帧/秒

# 添加点击事件，打印当前点的距离
def callbackFunc(e, x, y, f, p):
    if e == cv2.EVENT_LBUTTONDOWN:        
        print (threeD[y][x])

cv2.setMouseCallback("depth", callbackFunc, None)
framecnt=0
start = 0
end=0
while True:
    if framecnt ==0:
        start=time.time()
    if framecnt ==50:
        end=time.time()
        dt=end-start
        fps=50/dt
        print('fps:')
        print(fps)
        framecnt=0
        start=time.time()
    ret, frame = camera.read()
 #  1  47
    if not ret:
        break 
    imgL =  frame[0:480,0:640]# 坐标：[Ly:Ry , Lx:Rx]
    imgR =  frame[0:480,640:1280]# 裁剪坐标为[y0:y1, x0:x1]
    
    # 根据更正map对图片进行重构
    img1_rectified = cv2.remap(imgL, camera_configs.left_map1, camera_configs.left_map2, cv2.INTER_LINEAR)
    img2_rectified = cv2.remap(imgR, camera_configs.right_map1, camera_configs.right_map2, cv2.INTER_LINEAR)
    
    # 将图片置为灰度图，为StereoBM作准备
    imgGrayL = cv2.cvtColor(img1_rectified, cv2.COLOR_BGR2GRAY)
    imgGrayR = cv2.cvtColor(img2_rectified, cv2.COLOR_BGR2GRAY)

    # 两个trackbar用来调节不同的参数查看效果
    num = cv2.getTrackbarPos("num", "depth")
    blockSize = cv2.getTrackbarPos("blockSize", "depth")
    if blockSize % 2 == 0:
        blockSize += 1
    if blockSize < 5:
        blockSize = 5

    cv2.imshow("left", imgGrayL)
    cv2.imshow("right", imgGrayR)
    
    # 根据Block Maching方法生成差异图（opencv里也提供了SGBM/Semi-Global Block Matching算法，有兴趣可以试试）
    stereo = cv2.StereoBM_create(numDisparities=16*num, blockSize=blockSize)
    disparity = stereo.compute(imgGrayL, imgGrayR)

    disp = cv2.normalize(disparity, disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    # 将图片扩展至3d空间中，其z方向的值则为当前的距离
    threeD = cv2.reprojectImageTo3D(disparity.astype(np.float32)/16., camera_configs.Q)


    cv2.imshow("depth", disp)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    elif key == ord("s"):
        print("save")
        cv2.imwrite("snapshot/left.png", imgL)
        cv2.imwrite("snapshot/right.png", imgR)
        cv2.imwrite("snapshot/depth.png", disp)
    framecnt+=1
camera.release()
cv2.destroyAllWindows()
