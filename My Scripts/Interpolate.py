# -*- coding: utf-8 -*-
"""
Created on Tue May 29 09:41:07 2018
EL Interpolador. Interpola.
Sï, en cada script hay una versión ligeramente distinta de writePascal, y pascal_voc_clean_xml. 
Sorry.
@author: Abraham
"""
import os
import sys
import xml.etree.ElementTree as ET
import glob


def writeObject(clase, coord, file, idnumber):
    """
    Writes an object to the .xml
    """
    f = file
    f.write('\t' + '<object>\n')
    f.write('\t' + '\t' + '<name>' + clase + '</name>\n')
    f.write('\t' + '\t' + '<idnumber>' + str(idnumber) + '</idnumber>\n')
    f.write('\t' + '\t' + '<bndbox>\n')
    f.write('\t' + '\t' + '\t' + '<xmin>' + str(coord[0]) + '</xmin>\n')
    f.write('\t' + '\t' + '\t' + '<ymin>' + str(coord[1]) + '</ymin>\n')
    f.write('\t' + '\t' + '\t' + '<xmax>' + str(coord[2]) + '</xmax>\n')
    f.write('\t' + '\t' + '\t' + '<ymax>' + str(coord[3]) + '</ymax>\n')
    f.write('\t' + '\t' + '</bndbox>\n')
    f.write('\t' + '</object>\n')


def writePascal(coordinates, xml_path, image_name, res, clase):
    """
    This version of writePascal supports multiple objects
    Input: 
        coordinates: PascalVOC format (xmin, ymin, xmax, ymax)
        List of objects (bounding boxes)
        xml_path: Path to file
        image_name: Name of the file, should be the same as the image of which is ground truth
        res: Tuple (image_width, image_height)
        clase: Class (default 'person')
    Output:
        Writes file
    """

    with open(xml_path, 'w+') as f:
        f.write('<annotation>\n')
        f.write('\t <filename>' + image_name + '</filename>\n')
        f.write('\t <size>\n')
        f.write('\t' + '\t' + '<width>'+str(res[0])+'</width>\n')
        f.write('\t' + '\t' + '<height>'+str(res[1])+'</height>\n')
        f.write('\t' + '</size>\n')
        jj = 0
        for objeto in coordinates:
            jj += 1
            coord = []
            # coord = [xmin, ymin, xmax, ymax]
            coord.append(objeto[1])
            coord.append(objeto[2])
            coord.append(objeto[3])
            coord.append(objeto[4])
            writeObject(clase, coord, f, jj)
        f.write('</annotation>\n')


def _pp(l):  # Pretty printing
    for i in l: print('{}: {}'.format(i, l[i]))


def pascal_voc_clean_xml(path, pick, exclusive=False):
    """
    Reads all .xml files in path folder and loads the information in "dumps"
    dumps is a list of objects with the following format (example):
    [ ['000880.jpg'] [ [1280][720][ ['person', 689, 409, 710, 490] ] ] ]
    [ [img_name(str)] [ [img_width][img_height][ [class(str), x1, y1, x2, y2] ] ] ]
    It is possible for multiple objects to appear.

    This version does not read ID number,
    """  
    print('Parsing for {} {}'.format(
            pick, 'exclusively' * int(exclusive)))

    dumps = list()
    cur_dir = os.getcwd()
    os.chdir(path)
    annotations = os.listdir('.')
    annotations = glob.glob(str(annotations) + '*.xml')
    size = len(annotations)

    for i, file in enumerate(annotations):
        # progress bar      
        sys.stdout.write('\r')
        percentage = 1. * (i+1) / size
        progress = int(percentage * 20)
        bar_arg = [progress*'=', ' '*(19-progress), percentage*100]
        bar_arg += [file]
        sys.stdout.write('[{}>{}]{:.0f}%  {}'.format(*bar_arg))
        sys.stdout.flush()
        
        # actual parsing 
        in_file = open(file)
        tree = ET.parse(in_file)
        root = tree.getroot()
        jpg = str(root.find('filename').text)
        imsize = root.find('size')
        w = int(imsize.find('width').text)
        h = int(imsize.find('height').text)
        all = list()

        for obj in root.iter('object'):
                current = list()
                name = obj.find('name').text
                if name not in pick:
                        continue
                xmlbox = obj.find('bndbox')
                xn = int(float(xmlbox.find('xmin').text))
                xx = int(float(xmlbox.find('xmax').text))
                yn = int(float(xmlbox.find('ymin').text))
                yx = int(float(xmlbox.find('ymax').text))
                current = [name, xn, yn, xx, yx]
                all += [current]

        add = [[jpg, [w, h, all]]]
        dumps += add
        in_file.close()

    # gather all stats
    stat = dict()
    for dump in dumps:
        all = dump[1][2]
        for current in all:
            if current[0] in pick:
                if current[0] in stat:
                    stat[current[0]] += 1
                else:
                    stat[current[0]] = 1

    print('\nStatistics:')
    _pp(stat)
    print('Dataset size: {}'.format(len(dumps)))

    os.chdir(cur_dir)
    return dumps


def frame_index_in_dumps(frame, dumps):
    """
    If there are frames with occlusions (images without .xml) , frame number
    does not correlate to index in dumps variable.
    We search dumps for the index that corresponds to the frame.
    """    
    name = str(frame).zfill(6)+'.jpg'
    for element in dumps:
        if name in element:
            return dumps.index(element)
    return -1  # For raising an error with an assert


def interpolate(ANN, xml_path, clase, interpol1, interpol2, interpolid):
    
    assert (interpol2 > interpol1), "interpol2 should be greater than interpol1"
    
    dumps = pascal_voc_clean_xml(ANN, pick=clase, exclusive=False)
    
    # Initial and final objects loading
    # List of lists: [ ['person',x1,y1,x2,y2] , ['person',x1,y1,x2,y2] ]
    i1 = frame_index_in_dumps(interpol1, dumps)
    i2 = frame_index_in_dumps(interpol2, dumps)
    assert (len(dumps[i1][1][2]) >= interpolid[-1]), "ID not found in frame interpol1"
    assert (len(dumps[i2][1][2]) >= interpolid[-1]), "ID not found in frame interpol2"
    start = list()
    end = list()
    for idnumber in interpolid:
        start.append(dumps[i1][1][2][idnumber-1])
        end.append(dumps[i2][1][2][idnumber-1])
                
    # We calculate the 'slope' of the line that
    # interpolates each coordinate
    interpol = []
    for idnumber in interpolid:
        interpol.append([(end[interpolid.index(idnumber)][j+1] - start[interpolid.index(idnumber)][j+1]) /
                         (interpol2 - interpol1)for j in range(4)])

    ii = interpol1    
    miss = 0
    for element in dumps[i1+1:i2]:
        ii += 1
        if os.path.isfile(os.path.join(ANN, str(ii).zfill(6) + '.xml')):
            image_name = os.path.join(element[0])
            path = os.path.join(xml_path, str(ii).zfill(6) + '.xml')
            res = (element[1][0], element[1][1])  # Loads resolution
            coord = element[1][2]  # Loads a list with each object: [clase,x1,y1,x2,y2]

            # New coordinates for interpolated object. If object with such ID
            # already exists, overwrite, else append

            for idnumber in interpolid:
                if len(coord) < idnumber:
                    coord.append(['person'] + [int(start[interpolid.index(idnumber)][i+1] + 
                                 interpol[interpolid.index(idnumber)][i]*(ii-interpol1)) for i in range(4)])
                else:
                    coord[idnumber-1] = ['person'] + [int(start[interpolid.index(idnumber)][i+1] + 
                         interpol[interpolid.index(idnumber)][i]*(ii-interpol1)) for i in range(4)]
            writePascal(coord, path, image_name, res, clase)
        else:
            while os.path.isfile(os.path.join(ANN, str(ii).zfill(6) + '.xml')) is not True:
                ii += 1
                miss += 1
            image_name = os.path.join(element[0])
            path = os.path.join(xml_path, str(ii).zfill(6) + '.xml')
            res = (element[1][0], element[1][1])  # Loads resolution
            coord = element[1][2]  # Loads a list with each object: [clase,x1,y1,x2,y2]

            # New coordinates for interpolated object. If object with such ID
            # already exists, overwrite, else append

            for idnumber in interpolid:
                if len(coord) < idnumber:
                    coord.append(['person'] + [int(start[interpolid.index(idnumber)][i+1] + 
                                 interpol[interpolid.index(idnumber)][i]*(ii-interpol1)) for i in range(4)])
                else:
                    coord[idnumber-1] = ['person'] + [int(start[interpolid.index(idnumber)][i+1] + 
                         interpol[interpolid.index(idnumber)][i]*(ii-interpol1)) for i in range(4)]
            writePascal(coord, path, image_name, res, clase)

    print('Interpolated video from frame {} to {} for object id: {}'.format
          (interpol1, interpol2, interpolid))
    print('{} files written'.format(interpol2-interpol1-miss-1))

    if miss > 0:
        print('{} frames were not interpolated because there is no object.\nDraw something in them.'.format(miss))   


if __name__ == '__main__':
    """
    ANN: where annotations are
    xml_path: where interpolation will write to
    You probably want ANN and xml_path to be the same
    """
    # Source path
    ANN = 'C:/Users/Abraham/Datasets/UAV123_10fps/data_seq/UAV123_10fps/group3'
    # Output path
    xml_path = 'C:/Users/Abraham/Datasets/UAV123_10fps/data_seq/UAV123_10fps/group3'
    
    clase = 'person'
    
    # INTERPOLATE FROM FRAME:
    interpol1 = 1823
    # TO FRAME:
    interpol2 = 1831
    
    # INTERPOLATE OBJECTS WITH ID
    interpolid = [4, 5]
    # interpolid = [4]
    
    interpolate(ANN, xml_path, clase, interpol1, interpol2, interpolid)

