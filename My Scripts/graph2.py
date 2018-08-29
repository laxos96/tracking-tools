# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 16:13:15 2018

@author: Abraham
"""

import numpy as np
import matplotlib.pyplot as plt

#file = open("/home/abraham/Downloads/1",'r')
#a = file.readlines()
#data=[]
#c=[[],[],[],[]]
#matlab=[[],[],[],[]]
#python=[[],[],[],[]]
#for element in a:
#    element=element[:-1]
#    data.append(element.split(" "))
#    element=element.split(" ")
#    eao=float(element[2])
#    accuracy=float(element[3])
#    robustness=float(element[4])
#    if element[-3] == '-':
#        continue
#    speed=float(element[-3])
#
#    #orden (eao, accuracy, robustness, speed)
#    if element[-1] == 'M':
#        matlab[0].append([eao])
#        matlab[1].append([accuracy])
#        matlab[2].append([robustness])
#        matlab[3].append([speed])
#    elif element[-1] == 'P':
#        python[0].append([eao])
#        python[1].append([accuracy])
#        python[2].append([robustness])
#        python[3].append([speed])
#    else:
#        c[0].append([eao])
#        c[1].append([accuracy])
#        c[2].append([robustness])
#        c[3].append([speed])
c=[]
c.append([2850, 3000, 3300, 4050, 4500, 4950, 5400, 
          6000,6750, 7050, 7650, 8250, 8850, 9450, 
          10050, 10200, 10350, 10950, 11550, 12150, 12750])
c.append([24.81, 27.75, 24.26, 24.79, 24.83, 27.84, 26.72,
          26.16,29.82, 31.42, 33.68, 35.01, 35.59, 35.54, 
          36.38, 36.55, 36.15, 36.45, 36.39, 36.14, 35.41])
cnp = np.array(c, dtype=np.float16)
#pnp = np.array(python, dtype=np.float16)         
#mnp = np.array(matlab, dtype=np.float16)  
# red dashes, blue squares and green triangles
#plt.plot(python[3], python[1], 'r--'), c[3], c[1], 'bs', matlab[3], matlab[1], 'go')
ploty = 1
plt.figure(figsize=(18,10))
plt.rcParams.update({'font.size': 26})
cplot=plt.plot(cnp[0],cnp[ploty], lw=2)
#mplot=plt.plot(mnp[3],mnp[ploty],'r^',markersize=14, label="MATLAB")
#pplot=plt.plot(pnp[3],pnp[ploty],'go',markersize=14, label="Python")
plt.xlabel('Step',labelpad=20)
plt.ylabel('mAP (%)',labelpad=20)
plt.title('Validation set mAP',y=1.02)
plt.grid()

#plt.legend()
#plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
plt.axis([2800, 13000, 24, 40])
#plt.show()
plt.savefig("C:/Users/Abraham/Datasets/validation_map.png",format='png',bbox_inches='tight')