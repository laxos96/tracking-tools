# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 11:13:50 2018
FORMATO
MAXIOU IDF1 IDP IDR Rcll Prcn GT MT PT ML FP FN IDs FM MOTA MOTP
@author: Abraham
"""

results_path = "C:/Users/Abraham/Datasets/Results/Tracking evaluation/Trained/group3_results.csv"
f=open(results_path)
data = f.readlines()

results=[]
i=0
for j in data:
    if i % 2 != 0:
        string = j.rstrip('\n').split(' ')
        string2 = []
        for element in string:
            if element != '':
                if '%' in element:
                    element = str(format(float(element.rstrip('%'))/100, '.4f'))
                string2.append(element.rstrip('%')) 
        results.append(string2)
    i+=1
for j in results:
    print(j)

f.close()