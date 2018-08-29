This is the repository for the code used in my Bachelor thesis '**UAV-based Object Tracker with a Convolutional
Neural Network Detector and a Kalman Filter-Dynamic Association Tracker**', developed in the 'Aeronaves y Vehículos
Espaciales' department of **Escuela Técnica Superior
de Ingeniería Aeroespacial** (ETSIAE), a faculty of **Universidad Politécnica de Madrid**. 

This repository is a collection of mostly open source code and some scripts developed by myself in order
to understand, integrate and modify a Neural Network based Object Tracker, specifically targeting autonomous UAV
person tracking.

The thesis is available in the file '**TFG.pdf**'

# 1. Structure

This repository contains the following different projects. While all of them are required to
work with a dataset, train and evaluate performance, Tracking-with-darkflow is the main part providing
the detection and tracking. Most of these projects were modified in some degree by me, so especific
instructions are provided in each folder above of the original ones.

- Tracking-with-darkflow - Forked from [bendidi](https://github.com/bendidi/Tracking-with-darkflow), 
this repository integrates a Convolutional Neural Network Object Detector 
([YOLO](https://pjreddie.com/darknet/yolo/), in its 
[darkflow](https://github.com/thtrieu/darkflow) implementation) and a Neural Network Object Tracker,
[Deep SORT](https://github.com/nwojke/deep_sort). Jointly, they provide amazingly fast multi object tracking
while being simple to install and manipulate thanks to the Python implementation. 

- mAP - Forked from [Cartucho](https://github.com/Cartucho/mAP), this repository offers a tool to compute the 
accuracy of the Object Detection part, the mAP (mean Average Precision).

- py-motmetrics - Forked from [cheind](https://github.com/cheind/py-motmetrics), this repository offers a tool to compute
the accuracy of the Multi Object Tracking part, with a series of metrics compatible with the [MOT Challenge](https://motchallenge.net/) 

- labelimg - From [tzutalin](https://github.com/tzutalin/labelImg), this software facilitates the manipulation of dataset annotations, and was extensively used in my thesis.
For ease of installation it is not incorporated directly into this repository.

- My scripts - A series of simple Python scripts designed to expedite handling of the large number of files typical from datasets.
They are pretty rough. Further instructions in the My scripts folder. CHANGE

# 2. Installation

Each of the tools has its own installation procedure, but some software is needed first.
- CUDA
- CUDNN
- Python 3.5
- Tensorflow
- OpenCV 3

Note that CUDA, CUDNN and Tensorflow are only required by Tracking-with-darflow, so if you intend
to only use the other tools (to manage datasets or evaluate performance, for example) you do not need to
install them.
#### 2.1 CUDA 
It is strongly recommended to use the GPU version of tensorflow, so first of all check that your GPU
has a CUDA compute capability of at least 3.0. [Check here.](https://developer.nvidia.com/cuda-gpus) If affirmative,
proceed to install CUDA following [NVIDIA official instructions](http://developer.download.nvidia.com/compute/cuda/9.0/Prod/docs/sidebar/CUDA_Quick_Start_Guide.pdf).
Download link [here](https://developer.nvidia.com/cuda-90-download-archive).

**IMPORTANT - CHECK THAT VERSION IS 9.0**

Some versions of tensorflow were not compatible with CUDA versions following 9.0. This version will not give compatibility
problems, as far as I know.

#### 2.2 CUDNN
Install CUDNN version 7.0 (again, for best compatibility) from [here](https://developer.nvidia.com/cudnn) (remember 
that you need NVIDIA Developer Program membership, registration is simple).

**IMPORTANT - CHECK THAT VERSION IS 7.0**

#### 2.3 Python
A Python 3.5 installation is required. This thesis was performed with an [Anaconda](https://www.anaconda.com/download/) 
environment, but can done without it. 

#### 2.4 Tensorflow
 
Tensorflow should be installed following [official instructions](https://www.tensorflow.org/install/). In short, 
if you are working with a conda environment named "tensorflow", only two commands are necessary.

Open a cmd (it may require administrator privileges) and execute:

    activate tensorflow
######
    pip install --ignore-installed --upgrade tensorflow-gpu 
 Remember to validate your installation before continuing.
 
#### 2.5 OpenCV 3
 
Again, assuming this is a conda environment, execute in the cmd:
 
    conda install --channel https://conda.anaconda.org/menpo opencv3
 Note that OpenCV installation can be tricky, so please validate your installation. This simple webcam demo is enough:

    import numpy as np
    import cv2

    cap = cv2.VideoCapture(0)
    
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
    
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    
No more libraries should be needed, since they have been installed as requisites of either Tensorflow or OpenCV 3.
#### 2.6 Code
Now, for the different parts of this repository, remember that each project has its own installation procedure. 

 
- Tracking-with-darkflow: Check installation instructions inside Tracking-with-darkflow folder.

- mAP: Check installation instructions inside mAP folder.

- py-motmetrics: Check installation instructions inside py-motmetrics folder.

- labelImg: Just download the latest version of this tool. Or stick 
with [version 1.7.0](https://github.com/tzutalin/labelImg/releases/tag/v1.7.0), the one I used.

- My Scripts: No installation is needed, they are simple scripts. 
 
## License
Each fork has its own license, all of them allowing free reproduction and modification but under different conditions
and obligations. Refer to them one when reproducing or modifying each part of this repository. 
 
- py-motmetrics: MIT
- mAP: Apache
- Tracking-with-darkflow: GNU General Public 3.0
- My Scripts: GNU General Public 3.0