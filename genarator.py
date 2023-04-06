# -*- coding: utf-8 -*-
"""
@author: DarrenCai

@date: 2021/10/19
"""

import os
import cv2
import numpy as np
from math import floor
from random import random
from random import sample
from shutil import copyfile
from shutil import move

if __name__ == '__main__':
    os.makedirs('tmp/pers', exist_ok=True)
    os.makedirs('tmp/gt', exist_ok=True)
    for dir in os.listdir('floorplans'):
        for item in os.listdir(f'floorplans/{dir}'):
            print(f'floorplans/{dir}/{item}')
            img = cv2.imread(f'floorplans/{dir}/{item}')
            img = cv2.resize(img, (512, 512))
            h, w, _ = img.shape

            x, y = floor(.5*w*random()), floor(.5*h*random())
            src = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]])
            dst = np.float32([[0, 0], [0, h-1], [w-x, h-y], [w-1, 0]])

            mtx = cv2.getPerspectiveTransform(src, dst)
            mtx[0][2] = mtx[1][2] = 0

            img_train = cv2.warpPerspective(img, mtx, (w,h))
            matrix = np.array(np.matrix(mtx).I)

            print(mtx)
            print(matrix)

            # cv2.imshow("train", img_train)
            # cv2.imshow("gt", img)
            # cv2.waitKey()

            name, ext = os.path.splitext(item)
            cv2.imwrite(f'tmp/pers/{name}.png', img_train)
            np.savetxt(f'tmp/pers/{name}.txt', matrix)
            cv2.imwrite(f'tmp/gt/{item}', img)
    
    gt = os.listdir('tmp/gt')
    train = set(sample(gt, len(gt)*11//12))
    os.makedirs('train/pers', exist_ok=True)
    os.makedirs('train/gt', exist_ok=True)
    os.makedirs('validate/pers', exist_ok=True)
    os.makedirs('validate/gt', exist_ok=True)
    for item in gt:
        name, ext = os.path.splitext(item)
        if item in train:
            move(f'tmp/gt/{item}', f'train/gt/{item}')
            move(f'tmp/pers/{name}.png', f'train/pers/{name}.png')
            move(f'tmp/pers/{name}.txt', f'train/pers/{name}.txt')
        else:
            move(f'tmp/gt/{item}', f'validate/gt/{item}')
            move(f'tmp/pers/{name}.png', f'validate/pers/{name}.png')
            move(f'tmp/pers/{name}.txt', f'validate/pers/{name}.txt')

    os.rmdir('tmp/pers')
    os.removedirs('tmp/gt')
