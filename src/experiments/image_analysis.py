# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 16:15:17 2020

@author: delgallegon
"""
from utils import tensor_utils as tu
from utils import generate_misaligned as gm
from random import randrange
import numpy as np
import cv2
import os
import global_vars as gv
from matplotlib import pyplot as plt

def identify_z(img):
    f, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True)
    f.set_size_inches(20,25)
    
    result, M, inverse_M = gm.perform_warp(img)
    threshold = 1
    gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,threshold,255,cv2.THRESH_BINARY)
    #plt.imshow(cv2.cvtColor(thresh,cv2.COLOR_GRAY2RGB)); plt.show()
    
    _,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x,y,w,h = cv2.boundingRect(cnt)
    
    crop = result[y:y+h,x:x+w]

    crop = gm.polish_border(crop)
    crop_img = cv2.resize(crop, (gv.WARP_W, gv.WARP_H)) 
    
    print("SHAPES. Cropped: " ,np.shape(crop), " Resized: ", np.shape(crop_img))
    
    #compute z ratio
    x_ratio = (np.shape(crop)[0] + gv.PADDING_CONSTANT) / np.shape(crop_img)[0]
    y_ratio = (np.shape(crop)[1] + gv.PADDING_CONSTANT) / np.shape(crop_img)[1]
    z_ratio = ((x_ratio * 0.5) + (y_ratio * 0.5)) / 1.0
    print("Ratio X:", x_ratio, " Ratio Y: ", y_ratio, "Ratio Z: ", z_ratio)
    
    M[0,0] = x_ratio; M[1,1] = y_ratio
    inverse_M = np.linalg.inv(M)
    padded_image = cv2.copyMakeBorder(img, gv.PADDING_CONSTANT, gv.PADDING_CONSTANT, gv.PADDING_CONSTANT, gv.PADDING_CONSTANT, cv2.BORDER_CONSTANT,
    value=[0,0,0])
    padded_dim = np.shape(padded_image)
    test_img = cv2.warpPerspective(crop_img, inverse_M, (padded_dim[1], padded_dim[0]), borderValue = (255,255,255))
    test_img = cv2.resize(test_img, (gv.WARP_W, gv.WARP_H)) 
    border_fill = gm.resize_by_border_filling(crop)
    
    ax1.imshow(img)
    ax2.imshow(crop_img)
    ax3.imshow(border_fill)
    ax4.imshow(test_img)
    plt.show()

def check_sensitivity(warp_img, ground_truth_M):
    predict_M = np.ndarray.copy(ground_truth_M)
    #do some manipulation
    predict_M[0,0] = predict_M[0,0] + 0.023451124
    predict_M[0,1] = predict_M[0,1] + 0.008827271
    predict_M[1,0] = predict_M[1,0] + 0.002156656
    predict_M[1,1] = predict_M[1,1] + 0.04398492
    predict_M[2,0] = predict_M[2,0] + 0.0000458847
    predict_M[2,1] = predict_M[2,1] + 0.0000353552

    predict_img = cv2.warpPerspective(warp_img, np.linalg.inv(predict_M), (np.shape(warp_img)[1], np.shape(warp_img)[0]),borderValue = (255,255,255))
    ground_truth_img = cv2.warpPerspective(warp_img, np.linalg.inv(ground_truth_M), (np.shape(warp_img)[1], np.shape(warp_img)[0]),borderValue = (255,255,255))
    f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
    f.set_size_inches(20,15)
    
    ax1.imshow(warp_img)
    ax2.imshow(predict_img)
    ax3.imshow(ground_truth_img)
    plt.show()
    
def main():
    # image_path = "E:/Raw KITTI Dataset/2011_09_26_drive_0001_sync/image_02/data/0000000096.png"
    # img = tu.load_image(image_path)
    # identify_z(img)
    
    lower = 105
    bounds = 1
    for i in range(lower, lower + bounds):
        warp_img_path = "E:/NN_Dataset/warp_rgb_train/warp_"+str(i)+".png"
        transform_img_path = "E:/NN_Dataset/warp_rgb_train/warp_"+str(i)+".txt"
        
        warp_img = tu.load_image(warp_img_path)
        ground_truth_M = np.loadtxt(transform_img_path)
        
        check_sensitivity(warp_img, ground_truth_M)
    
    
    

main()
