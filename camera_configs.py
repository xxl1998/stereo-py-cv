# filename: camera_configs.py
import cv2
import numpy as np

left_camera_matrix = np.array([[427.794765373576, 0., 345.316879362880],
                               [0., 427.523078909675,248.042320744550],
                               [0., 0., 1.]])
left_distortion = np.array([[0.1203, -0.3813, 0.0, 0.0, 0.00000]])



right_camera_matrix = np.array([[428.460031706320, 0., 345.577140366428],
                                [0., 428.182342124927, 253.893691879974],
                                [0., 0., 1.]])
right_distortion = np.array([[0.1146, -0.3773, 0.0, 0.00, 0.00000]])

om = np.array([0.01911, 0.03125, -0.00960]) # 旋转关系向量
R   = np.array([[0.999951195950026, 0.00365550158381214, -0.00917839998493453],
                                [-0.00363800747921088, 0.999991535409192, 0.00192198115182608],
                                [0.00918534809867894, -0.00188849626356949, 0.999956030514426]])
T = np.array([-59.9526388908344, -0.295725876726042, 0.398543708588111]) # 平移关系向量

size = (640, 480) # 图像尺寸

# 进行立体更正
R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(left_camera_matrix, left_distortion,
                                                                  right_camera_matrix, right_distortion, size, R,
                                                                  T)
# 计算更正map
left_map1, left_map2 = cv2.initUndistortRectifyMap(left_camera_matrix, left_distortion, R1, P1, size, cv2.CV_16SC2)
right_map1, right_map2 = cv2.initUndistortRectifyMap(right_camera_matrix, right_distortion, R2, P2, size, cv2.CV_16SC2)
