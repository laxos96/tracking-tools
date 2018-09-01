Placeholder

- Dataset_Visualizer.py - A script that lets you visualize dataset sequences with ground 
truth and tracking results.

        Input: 
        Sequence (folder with images .jpg)
        Ground truth (folder with annotations in PascalVOC .xml)
        Tracking results (.csv file such as produced by darkflow)
        
        Output:
        Visualization

- UAV123toPascalVOC.py - Converts an annotation file for a sequence in .txt format (as in the 
UAV123 dataset) to PascalVOC format.

        Input:
        Ground truth (file with annotations in yolo format .txt)
        
        Output:
        Ground truth (folder with annotations in PascalVOC .xml)
        
- Interpolate.py - Generates a linear interpolation between two given annotations. Use in conjunction
with an annotation software like [labelImg](https://github.com/tzutalin/labelImg) for maximum productivity, and
the script Dataset_Visualizer.py to keep track of ID numbers. Input and output path are intended to be the same.
    
        Input:
        Ground truth (folder with annotations in PascalVOC .xml)
        Interpolation start, end, and ID numbers to be interpolated.
        
        Output:
        Ground truth (folder with annotations in PascalVOC .xml)