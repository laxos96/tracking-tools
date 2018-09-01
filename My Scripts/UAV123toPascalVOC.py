import os


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


def writePascal(coord, xml_path, image_name, res, clase):
    """
    Input:
        coord: PascalVOC format (xmin, ymin, xmax, ymax)
        xml_path: Path to file
        image_name: Name of the file, should be the same as the image of which is ground truth
        res: Tuple (image_width, image_height)
        clase: Class (default 'person')
    Output:
        Writes file
    """

    assert (coord[2] > coord[0] and coord[3] > coord[1]), "Bbox dimension error. Input must be in the format: (xmin, ymin, xmax, ymax)"
    with open(xml_path, 'w+') as f:
        f.write('<annotation>\n')
        f.write('\t <filename>' + image_name + '</filename>\n')
        f.write('\t <size>\n')
        f.write('\t' + '\t' + '<width>'+str(res[0])+'</width>\n')
        f.write('\t' + '\t' + '<height>'+str(res[1])+'</height>\n')
        f.write('\t' + '</size>\n')
        writeObject(clase, coord, f,'1')
        f.write('</annotation>\n')


if __name__ == '__main__':
    """
    Converts an annotation file for a sequence in .txt format (as in the UAV123 dataset) to PascalVOC format.
    Input annotation should be in format xmin, ymin, width, height. Note: This script only supports one bounding box per
    image.
    
    If converting UAV123 dataset, beware that each sequence usually has several annotation .txt. These should me merged,
    and the resulting file is what this script will convert. Some sequences may have one or two lines missing or in excess.
    
    anno_path: Path to anno folder, containing annotation of the sequence in a single .txt.
     
    output_path: Path to anno folder where the .xml of the sequence will be written.
    
    image_name: Path of the image that the .xml is ground truth of. Relative to FLAGS.dataset attribute of darkflow.
    If FLAGS.dataset is set directly to the folder containing the images, image_name is simply the image name. 
    """
    # Name of the file to convert
    sequence_name = "person1.txt"
    sequence_number = 1
    anno_path = "D:/Datasets/UAV123_10fps/anno/UAV123_10fps"
    output_path = "D:/Datasets/UAV123_10fps/anno/UAV123_10fpsVOC/person1"

    #########################################
    # Info in the .xml
    # Image resolution
    res=[1280,720]
    # Class, default 'person'
    clase = 'person'
    #########################################

    path = os.path.join("D:/Datasets/UAV123_10fps/anno/UAV123_10fps", sequence_name)
    ii = 0
    with open(path, 'r') as anno_file:
        for line in anno_file:
            ii += 1
            ################
            display_annobbox = True
            coord = line.split(",")
            # Check occlusions (occlusions is NaN in UAV123 dataset)
            if coord[0] != 'NaN':
                for i in range(len(coord)): # String to integer
                    coord[i] = int(coord[i])
                coord[2] += coord[0]  # xmin, ymin, width, height to xmin, ymin, xmax, ymax
                coord[3] += coord[1]  # xmin, ymin, width, height to xmin, ymin, xmax, ymax
            else:
                display_annobbox = False
            ###################
            if display_annobbox:
                path = os.path.join(output_path, str(ii).zfill(6) + '.xml')
                image_name = os.path.join(str(ii).zfill(6) + '.jpg')
                writePascal(coord, path, image_name, res, clase)

