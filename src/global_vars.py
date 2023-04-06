# -*- coding: utf-8 -*-
"""
Created on Fri Jun 7 19:37:01 2019

Constants files
@author: delgallegon
"""

"""
DIRECTORY FOR PC
"""
#SAVE_PATH_RGB = 'E:/NN_Dataset/warp_rgb_orig/'
SAVE_PATH_WARP = '/home/darrencai/Documents/Projects/NeuralNets-ImageCorrection/train/pers/'
SAVE_PATH_RGB_GT = '/home/darrencai/Documents/Projects/NeuralNets-ImageCorrection/train/gt/'

#SAVE_PATH_RGB_VAL = 'E:/NN_Dataset/warp_rgb_orig_val/'
SAVE_PATH_WARP_VAL = '/home/darrencai/Documents/Projects/NeuralNets-ImageCorrection/validate/pers/'
SAVE_PATH_RGB_GT_VAL = '/home/darrencai/Documents/Projects/NeuralNets-ImageCorrection/validate/gt/'

RRL_RESULTS_PATH = ['E:/NN_Dataset/KITTI_Result/1/',
                    'E:/NN_Dataset/KITTI_Result/2/',
                    'E:/NN_Dataset/KITTI_Result/3/',
                    'E:/NN_Dataset/KITTI_Result/4/']

SAVE_PATH_UNSEEN_DATA = 'E:/Places Dataset/'
SAVE_PATH_UNSEEN_DATA_RGB_GT = '/home/darrencai/Documents/Projects/NeuralNets-ImageCorrection/test/gt/'
SAVE_PATH_UNSEEN_DATA_WARP = '/home/darrencai/Documents/Projects/NeuralNets-ImageCorrection/test/pers/'

SAVE_PATH_PREDICT = '/home/darrencai/Documents/Projects/NeuralNets-ImageCorrection/predict/'
IMAGE_PATH_PREDICT = '/home/darrencai/Documents/Projects/NeuralNets-ImageCorrection/predict/predictions/'
SAVE_PATH_FIGURES = '/home/darrencai/Documents/Projects/NeuralNets-ImageCorrection/predict/figures/'
IMAGE_PATH_EDGES = '/home/darrencai/Documents/Projects/NeuralNets-ImageCorrection/predict/img_edges/'

IMAGE_RGB_DIR = "D:/Datasets/Raw KITTI Dataset/"

"""
DIRECTORY FOR LAPTOP
"""
#SAVE_PATH_RGB = 'D:/NN_Dataset/warp_rgb_orig/'
#SAVE_PATH_WARP = 'D:/NN_Dataset/warp_rgb_mod/'
#SAVE_PATH_RGB_CROPPED = 'D:/NN_Dataset/warp_rgb_cropped/'

#
#SAVE_PATH_RGB_VAL = 'D:/NN_Dataset/warp_rgb_orig_val/'
#SAVE_PATH_WARP_VAL = 'D:/NN_Dataset/warp_rgb_mod_val/'
#SAVE_PATH_UNSEEN_DATA = 'D:/NN_Dataset/unseen_data_orig/'
#SAVE_PATH_UNSEEN_DATA_RGB = 'D:/NN_Dataset/unseen_data_rgb/'
#SAVE_PATH_UNSEEN_DATA_WARP = 'D:/NN_Dataset/unseen_data_warp/'

#SAVE_PATH_PREDICT = 'D:/Documents/GithubProjects/NeuralNets-ImageDepthExperiment/dataset/warp_rgb_predict/'
#IMAGE_PATH_PREDICT = 'D:/Documents/GithubProjects/NeuralNets-ImageDepthExperiment/dataset/warp_img_predictions/'

#IMAGE_RGB_DIR = "D:/Documents/GithubProjects/NeuralNets-ImageDepthExperiment/dataset/train_rgb/" #LAPTOP dir

IMAGE_W = 1242; IMAGE_H = 375
WARP_W = 1442; WARP_H = 575

#IMAGE_W = 769; IMAGE_H = 512

PLACES_W = 969; PLACES_H = 712

PADDING_CONSTANT = 100

if __name__== "__main__": #FIX for broken pipe num_workers issue.
    print()
