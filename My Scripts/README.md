Placeholder

- Dataset_Visualizer.py - A script that lets you visualize dataset sequences with ground 
truth and tracking results.

        Input: 
        Sequence (folder with images .jpg)
        Ground truth (folder with annotations in Pascal VOC .xml)
        Tracking results (.csv file such as produced by darkflow)
        
        Output:
        Visualization

- UAV123toPascalVOC.py - Converts an annotation file for a sequence in .txt format (as in the 
UAV123 dataset) to PascalVOC format.

        Input:
        Ground truth (file with annotations in yolo format .txt)
        
        Output:
        Ground truth (folder with annotations in Pascal VOC .xml)