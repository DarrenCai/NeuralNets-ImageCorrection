# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 13:36:50 2019

Own "trial-and-error" version of CNN training
@author: NeilDG
"""

import numpy as np
import tensorflow as tf
from model import read_depth as rd
from model import conv_util
from model import fcrn_model as fcrn
from matplotlib import pyplot as plt

KITTI_REDUCED_H = 125; KITTI_REDUCED_W = 414;

class CNN(object):
    
    def __init__(self, dataset):
        self.dataset = dataset
        self.epoch = 500
        self.learning_rate = 0.001
        self.batch_size = 64
        self.session = tf.Session()
        
        
    def parse_function(self, filenameRGB, fileNameDepth):
        image_string = tf.read_file(filenameRGB)
    
        # Don't use tf.image.decode_image, or the output shape will be undefined
        image = tf.image.decode_png(image_string, channels=3)
    
        # This will convert to float values in [0, 1]
        image = tf.image.convert_image_dtype(image, tf.float32)
    
        resizedRGB = tf.image.resize_images(image, [KITTI_REDUCED_H, KITTI_REDUCED_W])
        
        image_string = tf.read_file(fileNameDepth)
        image = tf.image.decode_png(image_string, channels = 3)
        image = tf.image.convert_image_dtype(image, tf.float32)

        resizedDepth = tf.image.resize_images(image, [KITTI_REDUCED_H, KITTI_REDUCED_W])
        return resizedRGB, resizedDepth
    
    def create_convNet(self, inputImage):
        conv1 = fcrn.conv_default(input=inputImage,name='conv1',stride=2,kernel_size=(7,7),num_filters=64)
        bn_conv1 = fcrn.batch_norm_default(input=conv1,name='bn_conv1',relu=True)
        pool1 = tf.nn.max_pool(bn_conv1, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME',name='pool1')
    
        shape = pool1.get_shape()
        print("Pool shape: ",shape, " Conv shape: ", conv1[0][0].get_shape())
        
        return pool1
    
    def train(self):
        
        trainData = self.dataset.map(map_func = self.parse_function, num_parallel_calls=4)
        trainData = trainData.batch(self.batch_size)
        trainData = trainData.prefetch(1)
        
        iterator = trainData.make_initializable_iterator()
        initOp = iterator.initializer
        nextElement = iterator.get_next()
        print("Finished pre-processing train data with iterator: ", iterator)
        
        weights = {
            'wc1': tf.get_variable('W0', shape=(3,3,3,32), initializer=tf.contrib.layers.xavier_initializer()), 
            'wc2': tf.get_variable('W1', shape=(3,3,32,64), initializer=tf.contrib.layers.xavier_initializer()), 
            'wc3': tf.get_variable('W2', shape=(3,3,64,128), initializer=tf.contrib.layers.xavier_initializer()),
            }
        biases = {
            'bc1': tf.get_variable('B0', shape=(32), initializer=tf.contrib.layers.xavier_initializer()),
            'bc2': tf.get_variable('B1', shape=(64), initializer=tf.contrib.layers.xavier_initializer()),
            'bc3': tf.get_variable('B2', shape=(128), initializer=tf.contrib.layers.xavier_initializer())
            }
    
        
        inputImage = tf.placeholder("float", [None, KITTI_REDUCED_H,KITTI_REDUCED_W,3], name = "input_image")
        outputImage = tf.placeholder("float", [None, KITTI_REDUCED_H,KITTI_REDUCED_W,3], name = "output_image")
        
        globalVar = tf.global_variables_initializer()
        
        pred = self.create_convNet(inputImage)
        #loss = tf.losses.mean_squared_error(pred, outputImage) #TODO: dimensions must be equal. use UPCONV from RRL
        #optimizer = tf.train.AdamOptimizer(self.learning_rate)
        #optimizer.minimize(loss)
        
        with self.session as sess:
            sess.run(globalVar) #init weights, biases and other variables
            for i in range(self.epoch):
                sess.run(initOp)
                try:
                    while True:
                      elemInstance = sess.run(nextElement)
                      print("Input image shape: ", np.shape(elemInstance[0][0]))
                      sess.run(pred, feed_dict = {inputImage: elemInstance[0]})
                      #opt = sess.run(optimizer, feed_dict = {x: nextElement[0], y: nextElement[1]})
                      print("epoch: ", (i+1))
                      #print("epoch ", (i+1)," Max epoch: ", self.epoch, " First elem shape: ", np.shape(elemInstance), "Shape of image: ", np.shape(elemInstance[0][0]))
                      #plt.imshow(elemInstance[0][0])
                      #plt.show()
#            
#                      plt.imshow(elem[1][0])
#                      plt.show()
                except tf.errors.OutOfRangeError:
                    pass
                
                

            
        
        

