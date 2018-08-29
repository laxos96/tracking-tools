# -*- coding: utf-8 -*-
"""
Changes ID number on given frames. Refer to Operation, below.
"""
import os
import xml.etree.ElementTree as ET

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
    # Formato: coord = [xmin, ymin, xmax, ymax]
    
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
            writeObject(clase, coord, f, objeto[5])
        f.write('</annotation>\n')
        
def parse_xml(ANN, pick, exclusive = False):
    """
    Esta version solo lee UN archivo. En esta version dumps es solo UN objeto.
    Lee un archivo xml y carga en dumps la informacion.
    dumps es una lista de objetos con el siguiente formato (ejemplo):
    [ ['000880.jpg'] [ [1280][720][ ['person', 1, 689, 409, 710, 490] ] ] ]
    [ [img name (str)] [ [img width][img height][ [class (str), id, x1, y1, x2, y2] ] ] ]
    Puede haber mas de un objeto 'person'.
    Esta version SI lee ID.
    """  
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

def frame_index_in_dumps(idnumber, dumps):
    """
    Si hay frames con oclusion (frames sin xml) el numero de frame
    no se corresponde con el indice de dumps. Asi que hay que encontrarlo.
    """    
    for element in dumps[1][2]:
        if element[5] == idnumber:
            return dumps[1][2].index(element)
    assert (False), "ID not found in dumps. Something weird is happening"

if __name__ == '__main__':
    ###############################################
    # OPERATION:
    
    # Path de origen
    ANN = 'C:/Users/Abraham/Datasets/temp/'
    # Path de destino
    xml_path = "C:/Users/Abraham/Datasets/temp/"
    # Indica numero de video
    videonumber=24
    # Retocar IDs desde frame
    frame1 = 368
    # Hasta frame
    frame2 = 590
    # Cambiar ID 
    id1 = 4
    # Por ID
    id2 = 6
    ###############################################
    
    clase='person'
    print('Remaping ID {} into {} for frames between {} and {} for video {}'.
          format(id1,id2, frame1, frame2, videonumber))
    
    for i_file in range(frame1, frame2+1):
        full_path = os.path.join(ANN, str(videonumber).zfill(2) + str(i_file).zfill(4) + '.xml')
        dumps = parse_xml(full_path, pick = 'person', exclusive = False) # Parse
        index = frame_index_in_dumps(id1, dumps) # Find where is ID to change in dumps
        dumps[1][2][index][5] = id2 # Change it
        
        coord=dumps[1][2] # Carga lista con cada objeto: [clase,x1,y1,x2,y2,id]
        image_name = dumps[0] # Carga nombre
        path = os.path.join(xml_path, str(videonumber).zfill(2) + str(i_file).zfill(4) + '.xml')
        res=(dumps[1][0],dumps[1][1]) # Carga resolucion
    
        writePascal(coord, path, image_name, res, clase)
    print('Done')