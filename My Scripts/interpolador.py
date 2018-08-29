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
    # example: coord = [xmin, ymin, xmax, ymax]
    
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
    [ ['000880.jpg'] [ [1280][720][ ['person', 689, 409, 710, 490] ] ] ]
    [ [img name (str)] [ [img width][img height][ [class (str), x1, y1, x2, y2] ] ] ]
    Puede haber mas de un objeto 'person'.
    Esta version NO lee ID.
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

def frame_index_in_dumps(frame, dumps):
    """
    Si hay frames con oclusion (frames sin xml) el numero de frame
    no se corresponde con el indice en dumps. 
    Buscamos en dumps el indice que corresponde con el frame.
    """    
    name = str(frame).zfill(6)+'.jpg'
    for element in dumps:
        if name in element:
            return dumps.index(element)
    return -1 # For raising an error with an assert

def interpolate(ANN, xml_path, clase, interpol1, interpol2, interpolid):
    
    assert (interpol2>interpol1), "interpol2 should be greater than interpol1"
    
    dumps=pascal_voc_clean_xml(ANN, pick=clase, exclusive = False)
    
    # Cargamos objetos iniciales y finales de interpolacion
    # Lista de listas: [ ['person',x1,y1,x2,y2] , ['person',x1,y1,x2,y2] ]
    i1 = frame_index_in_dumps(interpol1, dumps)
    i2 = frame_index_in_dumps(interpol2, dumps)
    assert (len(dumps[i1][1][2])>=interpolid[-1]), "ID not found in frame interpol1"
    assert (len(dumps[i2][1][2])>=interpolid[-1]), "ID not found in frame interpol2"
    start=list()
    end=list()
    for idnumber in interpolid:
        start.append( dumps[i1][1][2][idnumber-1] )
        end.append( dumps[i2][1][2][idnumber-1] )
                
    # Calculamos la 'pendiente' de la recta de interpolacion de cada coordenada
    interpol=[]
    for idnumber in interpolid:
        interpol.append([(end[interpolid.index(idnumber)][j+1] - start[interpolid.index(idnumber)][j+1]) /
                         (interpol2 - interpol1)for j in range(4)])

    
    ii = interpol1    
    miss = 0
    for element in dumps[i1+1:i2]:
        ii+=1
        if os.path.isfile(os.path.join(ANN, str(ii).zfill(6) + '.xml')):
            image_name = os.path.join(element[0])
            path = os.path.join(xml_path, str(ii).zfill(6) + '.xml')
            res=(element[1][0],element[1][1]) # Carga resolucion
            coord=element[1][2] # Carga lista con cada objeto: [clase,x1,y1,x2,y2]
            
            # Calculamos las nuevas coordenadas del objeto interpolado
            # Si ya existe objeto con esa id, sobrescribimos, sino append
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
            res=(element[1][0],element[1][1]) #carga resolucion
            coord=element[1][2] #carga lista con cada objeto: [clase,x1,y1,x2,y2]

            # Calculamos las nuevas coordenadas del objeto interpolado
            # Si ya existe objeto con esa id, sobrescribimos, sino append
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
    
    ###############################################
    # OPERATION:
    # ANN 
    # XML 
    # (la idea es que ANN y xml_path sean el mismo)
    
    # ANN es donde estan las anotaciones hechas con labelimg
    ANN = 'C:/Users/Abraham/Datasets/UAV123_10fps/data_seq/UAV123_10fps/group3'
    # Path de destino
    xml_path = 'C:/Users/Abraham/Datasets/UAV123_10fps/data_seq/UAV123_10fps/group3'
    
    clase='person'
    
    # INTERPOLA DESDE FRAME:
    interpol1 = 1823
    # HASTA FRAME:
    interpol2 = 1831
    
    # INTERPOLA OBJETOS CON ID
    interpolid=[4,5]
    ###############################################
    
    interpolate(ANN, xml_path, clase, interpol1, interpol2, interpolid)

