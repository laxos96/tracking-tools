# -*- coding: utf-8 -*-
"""
Created on Mon May 28 12:24:04 2018
Coge anotaciones hechas en directorio ANN y las pasa a formato PASCAL VOC valido para training en darkflow
en el path indicado en xml_path. Input en formato PASCAL VOC xml con o sin identidad.
@author: Abraham

MODUS OPERANDI:
    Voy a hacer el video 10.
    Voy a UAV123toPascalVOC.
    Si es necesario, comento donde pone #standard y descomento donde pone
    #labelimg purposes
    Cambio videonumber y xmlpath a 10
    Ahora tengo las anotaciones junto a los frames.
    Voy a labelImg. Selecciono Open Dir y Change Save Dir a ese directorio.
    Anoto. Quiero interpolar. Voy a Interpolador.
    Cambio ANN, xml_path y videonumber a 10.
    Cambio interpol1 y 2 a las frames que quiero, pongo las id que quiero
    en el orden en el que las he anotado en labelimg.
    He terminado de interpolar.
    Voy a labelImgtoPascalVOC, cambio ANN y videonumber a 10,
    selecciono destino en xmlpath. Done.
    Luego pego a TheVeryGoodDataset
    Si no hace falta anotar copio directamente de TheGoodDataset
"""

import os
import sys
import xml.etree.ElementTree as ET
import glob

def writeObject(clase, coord, file, idnumber):
    """
    Escribe un objeto en el xml
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
    Input:
        coordinates: PASCAL format (x1, y1, x2, y2)
        Lista con cada objeto
        xml_path: path de destino incluido
        image_path (relativo a FLAGS.dataset) (typically person/000003.jpg por ejemplo)
        res: tuple (image_width, image_height)
        clase: 'person'
    Output:
        Writes file
    """
    # coord = [xmin, ymin, xmax, ymax]

    #assert (coord[2] >  coord[0] and coord[3] > coord[1]),"Bbox dimension error. Input must be in the format: (xmin, ymin, xwidth, yheight)"
    with open(xml_path,'w+') as f:
        f.write('<annotation>\n')
        f.write('\t <filename>' + image_name + '</filename>\n')
        f.write('\t <size>\n')
        f.write('\t' + '\t' + '<width>'+str(res[0])+'</width>\n')
        f.write('\t' + '\t' + '<height>'+str(res[1])+'</height>\n')
        f.write('\t' + '</size>\n')
        jj=0
        for objeto in coordinates:
            jj+=1
            coord=[]
            # coord = [xmin, ymin, xmax, ymax]
            coord.append(objeto[1])
            coord.append(objeto[2])
            coord.append(objeto[3])
            coord.append(objeto[4])
            writeObject(clase, coord, f, jj)
        f.write('</annotation>\n')


def _pp(l): # pretty printing
    for i in l: print('{}: {}'.format(i,l[i]))


def pascal_voc_clean_xml(ANN, pick, exclusive = False):
    """
    Lee todos los archivos xml de un directorio y carga en dumps la informacion.
    dumps es una lista de objetos con el siguiente formato (ejemplo):
    [ ['000880.jpg'] [ [1280][720][ ['person', 1, 689, 409, 710, 490] ] ] ]
    [ [img name (str)] [ [img width][img height][ [class (str), id, x1, y1, x2, y2] ] ] ]
    Puede haber mas de un objeto 'person'.
    Esta version SI lee ID.
    """
    print('Parsing for {} {}'.format(
            pick, 'exclusively' * int(exclusive)))

    dumps = list()
    cur_dir = os.getcwd()
    os.chdir(ANN)
    annotations = os.listdir('.')
    annotations = glob.glob(str(annotations)+'*.xml')
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
                if name not in pick:
                        continue
                xmlbox = obj.find('bndbox')
                xn = int(float(xmlbox.find('xmin').text))
                xx = int(float(xmlbox.find('xmax').text))
                yn = int(float(xmlbox.find('ymin').text))
                yx = int(float(xmlbox.find('ymax').text))
                current = [name,xn,yn,xx,yx]
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
                    stat[current[0]]+=1
                else:
                    stat[current[0]] =1

    print('\nStatistics:')
    _pp(stat)
    print('Dataset size: {}'.format(len(dumps)))

    os.chdir(cur_dir)
    return dumps


if __name__ == '__main__':
    ###############################################
    # OPERATION:
    # ANN LAST NUMBER
    # XML PATH
    # VIDEONUMBER

    # ANN es donde estan las anotaciones hechas con labelimg
    ANN = 'C:/Users/Abraham/Datasets/UAV123_10fps/data_seq/UAV123_10fps/group3/'
    # Path de destino
    xml_path = "C:/Users/Abraham/Datasets/temp/"
    # Indica numero de video
    videonumber=24
    ###############################################

    dumps = pascal_voc_clean_xml(ANN, pick='person', exclusive = False)
    clase ='person'
    print('Converting LabelImg to PascalVOC for annotations in \n{} \nto {}'.format
          (ANN,xml_path))
    videostr = str(videonumber).zfill(2)
    ii = 0
    for element in dumps:
        ii += 1
        if os.path.isfile(os.path.join(ANN, str(ii).zfill(6) + '.xml')):
            image_name = os.path.join('group'+str(3)+ '/',element[0])
            path = os.path.join(xml_path, videostr + str(ii).zfill(4) + '.xml')
            res = (element[1][0],element[1][1])  # carga resolucion
            coord = element[1][2]  # carga lista con cada objeto: [clase,x1,y1,x2,y2]
            writePascal(coord, path, image_name, res, clase)
        else:
            # if there is occlusion for all targets, dont write xml
            while os.path.isfile(os.path.join(ANN, str(ii).zfill(6) + '.xml')) is not True:
                ii += 1
            image_name = os.path.join('group'+str(3) + '/', element[0])
            path = os.path.join(xml_path, videostr + str(ii).zfill(4) + '.xml')
            res = (element[1][0], element[1][1])  # carga resolucion
            coord = element[1][2]  # carga lista con cada objeto: [clase,x1,y1,x2,y2]
            writePascal(coord, path, image_name, res, clase)
    print('Done')