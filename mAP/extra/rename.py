# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 12:01:42 2018

Script que cambia el nombre de los .txt a otro tipo 210002.txt

@author: Abraham
"""
import os
import glob
path="C:/Users/Abraham/Code/mAP-master/predicted"
image_paths = sorted(glob.glob(os.path.join(path, '*.txt')))
for ii, image_path in enumerate(image_paths):
    f=open(image_path)
    text=f.readlines()
    fa=open(os.path.join(a, str(21)+str(ii+1).zfill(4)+'.txt'), 'w+')
    for j in text:    
        fa.write(j)
    f.close()
    fa.close()