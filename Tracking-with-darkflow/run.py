from darkflow.darkflow.defaults import argHandler #Import the default arguments
import os
from darkflow.darkflow.net.build import TFNet


FLAGS = argHandler()
FLAGS.setDefaults()

#FLAGS.demo = "camera" # video file to use, or if camera just put "camera"
FLAGS.demo = "C:/Users/Abraham/Datasets/UAV123_10fps/videos/person9.mp4"
#el 8 esta chido
#checkar id switchs del 10

#FLAGS.config = "C:/Users/Abraham/Models/yolo-person" # tensorflow model

#FLAGS.load = "C:/Users/Abraham/Models/yolo-person/yolo.weights" # tensorflow weights
#FLAGS.model = "darkflow/cfg/yolo.cfg" # tensorflow model

FLAGS.load = 10950
FLAGS.model = "C:/Users/Abraham/Models/yolo-person/yolo2.cfg" # tensorflow model
FLAGS.labels = "C:/Users/Abraham/Models/yolo-person/labels3.txt"

# FLAGS.pbLoad = "tiny-yolo-voc-traffic.pb" # tensorflow model
# FLAGS.metaLoad = "tiny-yolo-voc-traffic.meta" # tensorflow weights
FLAGS.threshold = 0.6 # threshold of decetion confidance (detection if confidance > threshold )
FLAGS.gpu = 1 #how much of the GPU to use (between 0 and 1) 0 means use cpu
FLAGS.track = True # wheither to activate tracking or not
#FLAGS.trackObj = ['Bicyclist','Pedestrian','Skateboarder','Cart','Car','Bus'] # the object to be tracked
FLAGS.trackObj = ["person"]
FLAGS.saveVideo = False  #whether to save the video or not
FLAGS.BK_MOG = False # activate background substraction using cv2 MOG substraction,
                        #to help in worst case scenarion when YOLO cannor predict(able to detect mouvement, it's not ideal but well)
                        # helps only when number of detection < 3, as it is still better than no detection.
FLAGS.tracker = "deep_sort" # wich algorithm to use for tracking deep_sort/sort (NOTE : deep_sort only trained for people detection )
FLAGS.skip = 0 # how many frames to skipp between each detection to speed up the network
FLAGS.csv = False #whether to write csv file or not(only when tracking is set to True)
FLAGS.display = True # display the tracking or not

tfnet = TFNet(FLAGS)

# https://github.com/bendidi/Tracking-with-darkflow/issues/36

tfnet.camera()
exit('Demo stopped, exit.')
