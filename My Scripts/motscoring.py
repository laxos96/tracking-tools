# -*- coding: utf-8 -*-
"""
Created on Fri May 25 12:38:26 2018

@author: Abraham
"""
import motmetrics as mm
import numpy as np
import os
import glob
import xml.etree.ElementTree as ET

def parse_xml(ANN, pick, exclusive = False):

    dumps = list()
       
    in_file = open(ANN)
    tree=ET.parse(in_file)
    root = tree.getroot()
    jpg = str(root.find('filename').text)
    imsize = root.find('size')
    w = int(imsize.find('width').text)
    h = int(imsize.find('height').text)
    all = list()

    for obj in root.iter('object'):
            current = list()
            name = obj.find('name').text
            idnumber = int(obj.find('idnumber').text)
            if name not in pick:
                    continue
            xmlbox = obj.find('bndbox')
            xn = int(float(xmlbox.find('xmin').text))
            xx = int(float(xmlbox.find('xmax').text))
            yn = int(float(xmlbox.find('ymin').text))
            yx = int(float(xmlbox.find('ymax').text))
            current = [name,xn,yn,xx,yx,idnumber]
            all += [current]

    dumps = [jpg, [w, h, all]]
    in_file.close()

    return dumps


def get_output(output_file, img_num, file_pointer): 
    display_outputbbox = False    
    output_file.seek(file_pointer)
    file_pointer = output_file.tell()
    coord=[]
    string = output_file.readline()
    string = string.rstrip('\n')
    string = string.split(",")
    if string[0] == '':
        file_pointer = output_file.tell()
        coord.append([0,0,0,0,0,0])
        return display_outputbbox, coord, file_pointer
    coord.append([int(i) for i in string])
    
    coord[0][4] += coord[0][2] # el segundo punto del rectangulo tiene coordenadas relativas
    coord[0][5] += coord[0][3] # el segundo punto del rectangulo tiene coordenadas relativas
    j = 0   
    while coord[j][0] == img_num:
        display_outputbbox = True
        file_pointer = output_file.tell()
        string = output_file.readline()
        if string == '':
            break
        string = string.rstrip('\n')
        if string == '':
            file_pointer = output_file.tell()
            string = output_file.readline()
            string = string.rstrip('\n')
        if string == '':
            break
        string = string.split(",")

        if int(string[0]) == img_num:
            coord.append([int(i) for i in string])
            j+=1
            coord[j][4] += coord[j][2] # el segundo punto del rectangulo tiene coordenadas relativas
            coord[j][5] += coord[j][3] # el segundo punto del rectangulo tiene coordenadas relativas
        else:
            break
    return display_outputbbox, coord, file_pointer

def motscore_video(ds_path, video, videonumber, anno_path, results_file, output_path, max_iou):

    image_paths = sorted(glob.glob(os.path.join(ds_path, video, '*.jpg'))) 
    output_file = open(os.path.join(output_path, 'output_' + video + '.csv'))
    
    file_pointer = 0
    acc = mm.MOTAccumulator(auto_id=True)
    for ii,image_path in enumerate(image_paths):
        xml_path = os.path.join(anno_path, str(videonumber).zfill(2) + str(ii).zfill(4) + '.xml')
        
        display_annobbox = False
        if os.path.isfile(xml_path):
            display_annobbox = True
            dumps = parse_xml(xml_path, pick='person', exclusive = False)
            object_list = dumps[1][2]
            
        display_outputbbox, output_coord, file_pointer = get_output(output_file= output_file, 
                                                              img_num = ii, 
                                                              file_pointer = file_pointer)
        

        ####################################
        # DISTANCE NORMA
        ####################################
        # put gt coord in required format, such as  o = np.array([[100., 200.],[200., 200.]])
#        if display_annobbox:
#            o = np.array([[anno_coord[0]+(anno_coord[2]-anno_coord[0])/2,anno_coord[1]+(anno_coord[3]-anno_coord[1])/2]])
#        else:
#            o = []
#        idlist=[]
#        if display_outputbbox:    
#            h_temp=[]
#            for j in output_coord:
#                h_temp.append( [ j[2] + (j[4]-j[2])/2 , j[3] + (j[5]-j[3])/2 ] )
#                idlist.append(j[1])
#            h = np.array(h_temp) # hypohtesis array
#        else:
#            h=[]
#        C = mm.distances.norm2squared_matrix(o, h, max_d2=np.power(50,2)) # Distance matrix
        ####################################
        # DISTANCE IOU
        ####################################
        # put gt coord in required format, such as  o = np.array([[100., 200.],[200., 200.]])
        oidlist=[]
        if display_annobbox:
            anno_coord = []
            for j in object_list:
                anno_coord.append(j[1:5])
                oidlist.append(j[5])
            o = np.array(anno_coord) # object array
        else:
            o = []
            
        hidlist=[]
        if display_outputbbox:    
            h_temp=[]
            for j in output_coord:
                h_temp.append( [ j[2], j[3], j[4], j[5] ] )
                hidlist.append(j[1])
            h = np.array(h_temp) # hypohtesis array
        else:
            h=[]
            
        C = mm.distances.iou_matrix(o, h, max_iou) # Distance matrix
        ####################################
        # COMPUTE
        ####################################
        acc.update(
        oidlist,                 # Ground truth objects in this frame
        hidlist, C)              # Detector hypotheses in this frame, and distance matrix
        
    mh = mm.metrics.create()
    summary = mh.compute(acc, metrics = mm.metrics.motchallenge_metrics, name=str(max_iou))
    #summary.at['MyDet', 'motp'] = 1 - summary.iloc[0]['motp']/100
    strsummary = mm.io.render_summary(summary, 
                                      formatters = mh.formatters, 
                                      namemap = mm.io.motchallenge_metric_names)
    #strsummary=strsummary[:-5]+strsummary[-3:-1]+'.'+strsummary[-1]+'%' #this may break if there are more than 1 rows
    print(strsummary)
    output_file.close()
    
    return strsummary

if __name__ == '__main__':
    ds_path = "C:/Users/Abraham/Datasets/UAV123_10fps/data_seq/UAV123_10fps"
    video = 'person20'
    videonumber = 20
    
    anno_path = "C:/Users/Abraham/Datasets/TheVeryGoodDataset"
    results_path = "C:/Users/Abraham/Datasets/Results/Tracking evaluation/Trained"  #adonde van
    output_path = "C:/Users/Abraham/Datasets/Results/Tracking output/Trained" #de donde vienen
    
    iou_list = [0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    
    results_file = open(os.path.join(results_path, video + '_results.csv'),'w+') 
    for max_iou in iou_list:
        strsummary = motscore_video(ds_path, video, videonumber, anno_path, results_file, output_path, max_iou)
        results_file.write(strsummary + '\n')
    
    results_file.close()