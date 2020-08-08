# -*- coding: utf-8 -*-
"""
Combine a batch of images (of the same size) in a directory to one image
"""

from PIL import Image
import os

def combineImages(imageDir, imagesPerLine, margin, combinedImageName):
    files = [f for f in os.listdir(imageDir) if os.path.isfile(os.path.join(imageDir, f))]
    files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    
    print("Files to be combined: " + str(files))
    
    workingDir = os.getcwd()
    os.chdir(imageDir)
    if (not os.path.exists("combined")):
        os.mkdir("combined")
        
    if (combinedImageName is None or len(combinedImageName) == 0):
        combinedImageName = os.path.basename(os.getcwd()) + ".png"
    
    # load the first image to get the meta information    
    firstImage = Image.open(files[0])
    
    width, height = firstImage.size
    
    combinedWidth = (width + margin) * imagesPerLine;
    combinedHeight = (height + margin) * int(len(files) / imagesPerLine)
    
    # create a new transparent image that fits all other images
    combined = Image.new('RGBA', (combinedWidth, combinedHeight), (0, 0, 0, 0))
    
    for i, file in enumerate(files):
        image = Image.open(file)
        
        position = (((width + margin) * (i % imagesPerLine)), ((height + margin) * int(i / imagesPerLine)))
        combined.paste(image, position)
    
    combined.save("combined/" + combinedImageName, 'PNG')
    
    print("Combined image saved to: " + imageDir + "/combined/" + combinedImageName)
    
    os.chdir(workingDir)
    

if (__name__ == "__main__"):
    directory = input("Enter a directory (subdirectory of the current working directory): ")
    imagesPerLine = int(input("Enter the number of images per line: "))
    margin = int(input("Enter a margin that is kept between the images: "))
    combinedImageName = input("Enter the name of the combined image (leave empty to use the directory name): ")
    
    combineImages(directory, imagesPerLine, margin, combinedImageName)