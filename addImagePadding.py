# -*- coding: utf-8 -*-
"""
Add a padding to images (by extending it with copies of the edge pixels).
This can be usefull when using tile maps.
"""

from PIL import Image
import os

def addPaddingToImage(imagePath, paddingPixels, imageDestinationPath):
    image = Image.open(imagePath)
    
    width, height = image.size
    newWidth = width + (2 * paddingPixels)
    newHeight = height + (2 * paddingPixels)
    
    paddingImage = Image.new('RGBA', (newWidth, newHeight), (0, 0, 0, 0))
    
    # WARNING: the crop function takes the parameters (left, upper, right, lower) instead of (left, upper, width, height)
    # edge lines
    imageEdgeLeft = image.crop((0, 0, 1, height))
    imageEdgeRight = image.crop((width - 1, 0, width, height))
    imageEdgeTop = image.crop((0, 0, width, 1))
    imageEdgeBottom = image.crop((0, height - 1, width, height))
    
    # WARNING: the crop function takes the parameters (left, upper, right, lower) instead of (left, upper, width, height)
    # corner pixels
    imageCornerTopLeft = image.crop((0, 0, 1, 1))
    imageCornerTopRight = image.crop((width - 1, 0, width, 1))
    imageCornerBottomLeft = image.crop((0, height - 1, 1, height))
    imageCornerBottomRight = image.crop((width - 1, height - 1, width, height))
    
    # add a copy of the old image in the middle of the new image
    imageRegion = image.crop((0, 0, width, height))
    paddingImage.paste(imageRegion, (paddingPixels, paddingPixels))
    
    for i in range(paddingPixels):
        # left edge
        paddingImage.paste(imageEdgeLeft, (i, paddingPixels))
        # right edge
        paddingImage.paste(imageEdgeRight, (newWidth - i - 1, paddingPixels))
        # top edge
        paddingImage.paste(imageEdgeTop, (paddingPixels, i))
        # bottom edge
        paddingImage.paste(imageEdgeBottom, (paddingPixels, newHeight - i - 1))
        
        for j in range(paddingPixels):
            # top left corner
            paddingImage.paste(imageCornerTopLeft, (i, j))
            # top right corner
            paddingImage.paste(imageCornerTopRight, (newWidth - i - 1, j))
            # bottom left corner
            paddingImage.paste(imageCornerBottomLeft, (i, newHeight - j - 1))
            # bottom right corner
            paddingImage.paste(imageCornerBottomRight, (newWidth - i - 1, newHeight - j - 1))
            
    # save the result image
    paddingImage.save(imageDestinationPath, image.format)


def addPaddingToImagesInDir(directory, paddingPixels=2, outputDir="padding"):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    print("Files to be resized: " + str(files))
    print("Padding pixels: " + str(paddingPixels))
    
    workingDir = os.getcwd()
    os.chdir(directory)
    if (not os.path.exists(outputDir)):
        os.mkdir(outputDir)
        
    for file in files:
        addPaddingToImage(file, paddingPixels, outputDir + "/" + str(file))
        
    print("Wrote padding images to output directory: " + outputDir)
    
    os.chdir(workingDir)


if (__name__ == "__main__"):
    directory = input("Enter a directory (subdirectory of the current working directory): ")
    paddingPixels = int(input("Enter the number of padding pixels to use: "))
    
    addPaddingToImagesInDir(directory, paddingPixels, "padding")
    
    
    