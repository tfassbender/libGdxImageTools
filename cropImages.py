# -*- coding: utf-8 -*-
"""
Crop an image into pieces
"""

from PIL import Image
import os


def cropImageToPieces(inputImageFile, width, height, outputNamesPerLine=None, outputDirName="crop", continuousIndices=False, xOffsets=[0], yOffsets=[0], xOffsetStartsBeforeImage=False, yOffsetStartsBeforeImage=False, numImages=[-1], createDirectoryPerLine=True):
    # load the image
    image = Image.open(inputImageFile)
    imageWidth, imageHeight = image.size
    
    # calculate the starting positions
    startX = xOffsets[0] if xOffsetStartsBeforeImage else 0
    startY = yOffsets[0] if yOffsetStartsBeforeImage else 0
    
    # if no output name is defined, make the ouput name the name of the input image
    if outputNamesPerLine is None:
        outputNamesPerLine = [inputImageFile[:-4]] # without file ending
    
    # count the images for a continued index
    imageCount = 0
    
    # loop over the image to crop the pieces
    for row, y in enumerate(range(startY, imageHeight, height)):
        y += sum(yOffsets[:(row + 1 if yOffsetStartsBeforeImage else row)])
        imageCountPerLine = 0
        
        if (row >= len(outputNamesPerLine)):
            break
            
        for col, x in enumerate(range(startX, imageWidth, width)):
            x += sum(xOffsets[:(col + 1 if xOffsetStartsBeforeImage else col)])
            cropBox = (x, y, x+width, y+height)
            crop = image.crop(cropBox)
            imageCountPerLine += 1
            
            # name the croped image
            imageName = outputNamesPerLine[row];
            if (not continuousIndices and len(outputNamesPerLine) < row):
                imageName += "_" + str(row)
            
            # save the croped image
            try:
                if (not os.path.exists(outputDirName)):
                    os.mkdir(outputDirName)
                    
                if (createDirectoryPerLine):
                    if (not os.path.exists(outputDirName + "/" + imageName)):
                        os.mkdir(outputDirName + "/" + imageName)
                
                imageIndex = col + 1 if not continuousIndices else imageCount + 1
                imageCount += 1
                
                if (createDirectoryPerLine):
                    imagePath = outputDirName + "/" + imageName + "/" + imageName + "_" + str(imageIndex) + ".png"
                else:
                    imagePath = outputDirName + "/" + imageName + "_" + str(imageIndex) + ".png"
                    
                if (os.path.exists(imagePath)):
                    imagePath = imagePath[:-4] + "_1.png"
                crop.save(imagePath)
                
                if (imageCountPerLine >= numImages[row % len(numImages)] and numImages[row % len(numImages)] > 0):
                    break
            except Exception as e:
                print(e)


def readConfigFile(configFileName="crop.config"):
    # The crop.config file includes the following configuration fields:
    # 1. inputImageFile
    # 2. width
    # 3. height
    # 4. outputNamesPerLine
    # 5. outputDirName
    # 6. continuousIndices
    # 7. xOffsets
    # 8. yOffsets
    # 9. xOffsetStartsBeforeImage
    # 10. yOffsetStartsBeforeImage
    # 11. numImages
    
    configFile = open(configFileName, 'r')
    configLines = configFile.read().splitlines()
    configFile.close()
    
    intConfigs = [1, 2, 6, 7, 10]
    booleanConfigs = [5, 8, 9]
    listConfigs = [3, 6, 7, 10]
    
    config = []
    
    # remove comments
    while len(configLines) > 0:
        if (configLines[0].strip().startswith('#')):
            configLines = configLines[1:]
        else:
            break
    
    # read config enties
    for i, configEntry in enumerate(configLines):
        # remove inline comments and trim the entry
        commentIndex = configEntry.index('#')
        if (commentIndex != -1):
            configEntry = configEntry[:commentIndex]
        configEntry = configEntry.strip()
        
        # parse the entry
        if (i in listConfigs):
            parsedConfigEntry = configEntry.split(" ")
            if (i in intConfigs):
                parsedConfigEntry = [int(val) for val in parsedConfigEntry]
        elif (i in intConfigs):
            parsedConfigEntry = int(configEntry)
        elif (i in booleanConfigs):
            parsedConfigEntry = True if configEntry == "y" or configEntry == "Y" else False
        
        else:
            parsedConfigEntry = configEntry
        
        # add to config list
        config.append(parsedConfigEntry)
    
    return config
        
    
def createConfigFile():
    configText = """# This config file contains the crop configuration for an image.
# The first lines, starting with a comment char '#' will be ignored and can be used for comments
# The following lines need to stay in the correct order
# All lines can include comments after the inputs. These comments have to start with the comment char '#'
#
# The following lines are the config lines:
image.png                 # inputImageFile
32                        # width
32                        # height
imgs_line_1 imgs_line_2   # outputNamesPerLine (delimiter is a space character ' ')
crop                      # outputDirName
y                         # continuousIndices (y|n)
0                         # xOffsets (as list; delimiter is a space character ' ')
0                         # yOffsets (as list; delimiter is a space character ' ')
n                         # xOffsetStartsBeforeImage (y|n)
n                         # yOffsetStartsBeforeImage (y|n)
-1                        # numImages (-1 for 'count them yourself!')"""
    outputFile = open('crop.config', 'w')
    outputFile.write(configText)
    outputFile.close()
    
    
def readBooleanInput(outputText="", default=True):
    val = input(outputText)
    if (val == "y" or val == "Y" or (val == "" and default == True)):
        return True
    else:
        return False
    

def readIntListInput(outputText=""):
    values = input(outputText).split(" ")
    values = [int(val) for val in values]
    return values

    
if (__name__ == "__main__"):
    print("Crop images into pieces:\n\n    The input image needs to be in the same directory as the script\n    The output will be written in the 'crop' directory")
    
    useConfigFile = input("use config file? (Y/n) ")
    if (useConfigFile == "" or useConfigFile == "y" or useConfigFile == "Y"):
        useConfigFile = True
    else:
        useConfigFile = False
        
    if (useConfigFile):
        defaultConfigFileName = "crop.config"
        configFileName = input("enter the name of the config file: ")
        if (configFileName == ""):
            configFileName = defaultConfigFileName
        try:
            # read the config file
            config = readConfigFile(configFileName)
            print("\n    Configuration loaded from file: " + configFileName)
            configurations = ["inputImageFile", "width", "height", "outputNamesPerLine", "outputDirName", "continuousIndices", "xOffset", "yOffset", "xOffsetStartsBeforeImage", "yOffsetStartsBeforeImage", "numImages"]
            for i in range(len(config)):
                print("    " + configurations[i] + ": " + str(config[i]))
            
            try:
                inputImageFile, width, height, outputNamesPerLine, outputDirName, continuousIndices, xOffset, yOffset, xOffsetStartsBeforeImage, yOffsetStartsBeforeImage, numImages = config
                cropImageToPieces(inputImageFile, width, height, outputNamesPerLine, outputDirName, continuousIndices, xOffset, yOffset, xOffsetStartsBeforeImage, yOffsetStartsBeforeImage, numImages)
            except Exception as e:
                print(e)
            
        except Exception as e:
            print("The config file " + configFileName + " could not be interpreted\nThe error was:")
            print("    " + str(e))
            if (not os.path.exists(defaultConfigFileName)):
                print("No default file 'crop.config' found. Generating default config file")
                createConfigFile()
            else:
                print("The default config file " + defaultConfigFileName + " already exists. Rename or delete it to generate a new one")
        
    else: # no config file
        simpleCrop = readBooleanInput("use simple crop function? (Y/n) ", default=True)
        
        inputImageFile = input("Input image file: ")
        width = int(input("Crop width: "))
        height = int(input("Crop height: "))
        
        if (not simpleCrop):
            outputNamesPerLine = input("Output names per line (use space as delimiter): ").split(" ")
            outputDirName = input("output directory: ")
            continuousIndices = readBooleanInput("use continuous indices: (y/N) ", default=False)
            xOffset = readIntListInput("xOffset: ")
            yOffset = readIntListInput("yOffset: ")
            xOffsetStartsBeforeImage = readBooleanInput("does the x offset start before the first image? (y/N) ", default=False)
            yOffsetStartsBeforeImage = readBooleanInput("does the y offset start before the first image? (y/N) ", default=False)
            numImages = int(input("number of images (-1 for 'count them yourself!') "))
            
            cropImageToPieces(inputImageFile, width, height, outputNamesPerLine, outputDirName, continuousIndices, xOffset, yOffset, xOffsetStartsBeforeImage, yOffsetStartsBeforeImage, numImages)
            
        else: # simple crop
            cropImageToPieces(inputImageFile, width, height)
        
        
    print("\ndone")
        