# -*- coding: utf-8 -*-
"""
Resize a batch of images
"""

from PIL import Image
import os

def resizeImages(directory, scalingFactor=1.0):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    print("Files to be resized: " + str(files))
    print("Scaling factor: " + str(scalingFactor))
    
    workingDir = os.getcwd()
    os.chdir(directory)
    if (not os.path.exists("scaled")):
        os.mkdir("scaled")
    
    for file in files:
        image = Image.open(file)
        width, height = image.size
        fileType = image.format
        imageName = str(file)
        outputFile = "scaled/" + imageName
        
        #print("width: %d, height %d" % (width, height))
        #print("fileType: %s" % fileType)
        #print("imageName: %s" % imageName)
        #print("outputFileName: %s" % outputFile)
        
        newWidth = int(width * scalingFactor)
        newHeight = int(height * scalingFactor)
        
        resized = image.resize((newWidth, newHeight), Image.ANTIALIAS)
        resized.save(outputFile, fileType)
    
    print("Resized images saved to: " + directory + "/scaled/")
    
    os.chdir(workingDir)


if (__name__ == "__main__"):
    directory = input("Enter a directory (subdirectory of the current working directory): ")
    scalingFactor = float(input("Enter a scaling factor (1.0 for 100%): "))
    
    resizeImages(directory, scalingFactor)