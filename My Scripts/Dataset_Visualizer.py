import cv2
import os
import time
import glob
import xml.etree.ElementTree as ET


def show_text(text, img, coord, color=(255,255,255)):
    """
    Prints text in location for image img
    """
    if coord[2]>30:
        location = (coord[1], coord[2]-5)
    else:
        location = (coord[1], coord[4]+25)
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.7
    fontColor = color
    lineType = 2
    
    cv2.putText(img, text, location, font,
        fontScale, fontColor, lineType)


def parse_xml(ann, pick, exclusive = False):

    dumps = list()
       
    in_file = open(ann)
    tree = ET.parse(in_file)
    root = tree.getroot()
    jpg = str(root.find('filename').text)
    imsize = root.find('size')
    w = int(imsize.find('width').text)
    h = int(imsize.find('height').text)
    temp = list()

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
            current = [name, xn, yn, xx, yx, idnumber]
            temp += [current]

    dumps = [jpg, [w, h, temp]]
    in_file.close()

    return dumps


def get_output(output_file, img_num, file_pointer):

    display_outputbbox = False    
    output_file.seek(file_pointer)
    file_pointer = output_file.tell()
    coord = []
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
            j += 1
            coord[j][4] += coord[j][2] # el segundo punto del rectangulo tiene coordenadas relativas
            coord[j][5] += coord[j][3] # el segundo punto del rectangulo tiene coordenadas relativas
        else:
            break
    return display_outputbbox, coord, file_pointer


def watch_video(paths, options, videonumber):

    global terminate

    output_bool = options[0]
    anno_bool = options[1]
    ds_class = options[2]
    windowname = options[3]
    speed = options[4]

    terminate = False
    folder = ds_class + str(video_number)
    # List all images in folder 
    image_paths = sorted(glob.glob(os.path.join(paths[1], folder, '*.jpg')))
    # Load output
    if output_bool:
        output_file = open(os.path.join(paths[0], 'output_' + folder + '.csv'))
    
    file_pointer = 0
    
    for ii, image_path in enumerate(image_paths):
        img = cv2.imread(image_path)
        show_text('Sequence ' + folder,img, [0, 1050, 30, 0, 0])
        xml_path = os.path.join(paths[2], folder, str(ii).zfill(6) + '.xml')
        # If there are annotations, parse and paint
        if os.path.isfile(xml_path) and anno_bool:
            dumps = parse_xml(xml_path, pick='person', exclusive = False)
            object_list = dumps[1][2]
            for coord in object_list:
                cv2.rectangle(img,
                                (coord[1], coord[2]),
                                (coord[3], coord[4]),
                                (50,205,50),2)
                show_text(str(coord[5]),img, coord)
                
        if output_bool:        
            display_outputbbox, output_coord, file_pointer = get_output(output_file= output_file, 
                                                                  img_num = ii, 
                                                                  file_pointer = file_pointer)
            if display_outputbbox:         
                # Paint results 
                for tracked_object in output_coord: 
                    cv2.rectangle(img,
                                    (tracked_object[2], tracked_object[3]),
                                    (tracked_object[4], tracked_object[5]),
                                    (0, 0, 255),2)
                    textcoord = tracked_object[1:]
                    textcoord[1] -= 30
                    textcoord[2] += 25
                    textcoord[3] += 20
                    textcoord[4] -= 25
                    show_text(str(tracked_object[1]),img, textcoord, color=(0, 0, 0))
        # Show
        cv2.imshow(windowname, img)
        time.sleep(0.02 / speed)
        # cv2 necessary commands
        keyPressed = cv2.waitKey(1)      
        if keyPressed == 113:
            if output_bool:
                output_file.close()
            break  # q to next      
        if keyPressed == 27:
            terminate = True
            if output_bool:
                output_file.close()
            break  # esc to quit
    if output_bool:
        output_file.close()


if __name__ == '__main__':
    """
    Visualize a dataset with its annotations and tracking results. Press Esc to quit.
    
    Variables:
    output_path: Path to tracking results in .csv format as given by darkflow.
    If you do not want to visualize tracking results, make boolean output_bool = False
    
    ds_path: Path to dataset folder, containing each sequence in a folder. Images should be .jpg
    ds_class: Name of the class to visualize (person, group, etc)
    
    multi_video: True to visualize multiple sequences of a class (person, group, etc), False to only visualize
    sequence specified in video_number. If True, indicate start and finish number in multi_start and multi_end. Press q
    to see next sequence.
    
    anno_path: Path to anno folder, containing annotations of each sequence in a folder named the same
    as the sequence folder. In .xml format with a file for each image. Use script UAV123toPascalVOC.py to transform 
    yolo annotations to desired Pascal VOC format. If you do not want to visualize annotations, make boolean 
    output_bool = False.
    
    """
    output_path = "C:/Users/Abraham/Datasets/UAV123_10fps/output/original"
    # True to visualize tracking results, False otherwise
    output_bool = False

    ds_path = "D:/Datasets/UAV123_10fps/data_seq/UAV123_10fps"
    ds_class = "person"
    # True to visualize multiple sequences, False otherwise
    multi_video = False
    # If multi_video = False, indicate sequence number
    video_number = 1
    # If multi_video = True, indicate start and end
    multi_start = 1
    multi_end = 21

    anno_path = "D:/Datasets/UAV123_10fps/anno/UAV123_10fpsVOC"
    # True to visualize ground truth, False otherwise
    anno_bool = True

    # Speed, 1 is default
    speed = 1
    #########################################
    windowname = 'Dataset_Visualizer'
    options = [output_bool, anno_bool, ds_class, windowname, speed]
    paths = [output_path, ds_path, anno_path]
    
    cv2.namedWindow(windowname, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(windowname, 1280, 720)
    if multi_video:
        for video_number in range(multi_start, multi_end + 1):
            watch_video(paths, options, video_number)
            if terminate:
                break
    else:
        watch_video(paths, options, video_number)

    cv2.destroyAllWindows()
