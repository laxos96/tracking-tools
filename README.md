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
They are pretty rough. Further instructions in the My scripts folder. WIP.

# 2. Installation

Each part of this repository has its own installation procedure, which you will find in their respective 
folders. However, I have elaborated a joint installation manual with in depth instructions for dependencies
such as OpenCV and Visual C++, which are overlooked in the other instructions. This manual is available in the file
'**Installation.pdf**' 
 
## License
Each fork has its own license, all of them allowing free reproduction and modification but under different conditions
and obligations. Refer to them one when reproducing or modifying each part of this repository. 
 
- py-motmetrics: MIT
- mAP: Apache
- Tracking-with-darkflow: GNU General Public 3.0
- My Scripts: GNU General Public 3.0