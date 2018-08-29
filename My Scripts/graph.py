#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 10:58:33 2018

@author: abraham
"""

import numpy as np
import matplotlib.pyplot as plt

file = open("/home/abraham/Downloads/1",'r')
a = file.readlines()
data=[]
c=[[],[],[],[]]
matlab=[[],[],[],[]]
python=[[],[],[],[]]
for element in a:
    element=element[:-1]
    data.append(element.split(" "))
    element=element.split(" ")
    eao=float(element[2])
    accuracy=float(element[3])
    robustness=float(element[4])
    if element[-3] == '-':
        continue
    speed=float(element[-3])

    #orden (eao, accuracy, robustness, speed)
    if element[-1] == 'M':
        matlab[0].append([eao])
        matlab[1].append([accuracy])
        matlab[2].append([robustness])
        matlab[3].append([speed])
    elif element[-1] == 'P':
        python[0].append([eao])
        python[1].append([accuracy])
        python[2].append([robustness])
        python[3].append([speed])
    else:
        c[0].append([eao])
        c[1].append([accuracy])
        c[2].append([robustness])
        c[3].append([speed])
 
cnp = np.array(c, dtype=np.float16)
pnp = np.array(python, dtype=np.float16)         
mnp = np.array(matlab, dtype=np.float16)  
# red dashes, blue squares and green triangles
#plt.plot(python[3], python[1], 'r--'), c[3], c[1], 'bs', matlab[3], matlab[1], 'go')
ploty = 1
plt.figure(figsize=(18,10))
plt.rcParams.update({'font.size': 26})
cplot=plt.plot(cnp[3],cnp[ploty],'bs', markersize=14, label="C++")
mplot=plt.plot(mnp[3],mnp[ploty],'r^',markersize=14, label="MATLAB")
pplot=plt.plot(pnp[3],pnp[ploty],'go',markersize=14, label="Python")
plt.xlabel('Speed [EFO]',labelpad=20)
plt.ylabel('Accuracy',labelpad=20)
plt.title('VOT16 trackers',y=1.02)
plt.grid()

plt.legend()
#plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
#plt.axis([40, 160, 0, 0.03])
#plt.show()
plt.savefig("/home/abraham/Downloads/language_comparison1.png",format='png',bbox_inches='tight')