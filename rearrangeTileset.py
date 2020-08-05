# -*- coding: utf-8 -*-
"""
Re-arrange a tileset image:
    - cut the tileset into pieces
    - (optionally) scale the tiles
    - put the tiles back together with a optional margin
"""

import cropImages
import resizeImages
import combineImages

import sys

def readConfigFile(configFileName="tileset.config"):
    ############################################################################################################
    #                                                                                                          #
    # This config file contains the crop configuration for an image.                                           #
    # The first lines, starting with a comment char '#' will be ignored and can be used for comments           #
    # The following lines need to stay in the correct order                                                    #
    # All lines can include comments after the inputs. These comments have to start with the comment char '#'  #
    #                                                                                                          #
    ##### Crop images configuration ############################################################################
    #                                                                                                          #
    #    # 1. crop configuration file                                                                          #
    #                                                                                                          #
    ### Resize images configuration ############################################################################
    #                                                                                                          #
    #    # 2. tiles directory                                                                                  #
    #    # 3. scale factor                                                                                     #
    #                                                                                                          #
    ### Combine images configuration ###########################################################################
    #                                                                                                          #
    #    # 4. images per line                                                                                  #
    #    # 5. margin between images (in pixels)                                                                #
    #    # 6. combined image name                                                                              #
    #                                                                                                          #
    ############################################################################################################
    
    configFile = open(configFileName, 'r')
    configLines = configFile.read().splitlines()
    configFile.close()
    
    config = []
    
    intConfigs = [3, 4]
    floatConfigs = [2]
    
    # remove comments
    while len(configLines) > 0:
        if (configLines[0].strip().startswith('#') or len(configLines[0]) == 0):
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
        if (i in intConfigs):
            parsedConfigEntry = int(configEntry)
        elif (i in floatConfigs):
            parsedConfigEntry = float(configEntry)
        else:
            parsedConfigEntry = configEntry
        
        # add to config list
        config.append(parsedConfigEntry)
    
    return config

def createDefaultConfigFile():
    configText = """############################################################################################################
#                                                                                                          #
# This config file contains the crop configuration for an image.                                           #
# The first lines, starting with a comment char '#' will be ignored and can be used for comments           #
# The following lines need to stay in the correct order                                                    #
# All lines can include comments after the inputs. These comments have to start with the comment char '#'  #
#                                                                                                          #
##### Crop images configuration ############################################################################
#                                                                                                          #
#    # 1. crop configuration file                                                                          #
#                                                                                                          #
### Resize images configuration ############################################################################
#                                                                                                          #
#    # 2. tiles directory                                                                                  #
#    # 3. scale factor                                                                                     #
#                                                                                                          #
### Combine images configuration ###########################################################################
#                                                                                                          #
#    # 4. images per line                                                                                  #
#    # 5. margin between images (in pixels)                                                                #
#    # 6. combined image name                                                                              #
#                                                                                                          #
############################################################################################################

crop.config   # 1. crop configuration file
tiles         # 2. tiles directory
1             # 3. scale factor
10            # 4. images per line
2             # 5. margin between images (in pixels)
tileset       # 6. combined image name"""
    outputFile = open('tileset_default.config', 'w')
    outputFile.write(configText)
    outputFile.close()


if (__name__ == "__main__"):
    configFile = input("Enter the name of the config file: ")
    
    try:
        cropConfigFile, teilesDirectory, scaleFactor, imagesPerLine, margin, combinedImageName = readConfigFile(configFile)
    except Exception as e:
        print("error while loading the configuration: " + str(e))
        createDefaultConfig = input("Do you want to create a default config file in 'tileset_default.config'? (y/N) ")
        createDefaultConfig = True if createDefaultConfig == "y" or createDefaultConfig == "Y" else False
        if (createDefaultConfig):
            createDefaultConfigFile()
        sys.exit(1)
    
    print("\n\n ### Cropping images #########################################################################\n")
    try:
        print("reading config file...")
        inputImageFile, width, height, outputNamesPerLine, outputDirName, continuousIndices, xOffset, yOffset, xOffsetStartsBeforeImage, yOffsetStartsBeforeImage, numImages = cropImages.readConfigFile(cropConfigFile)
        print("cropping image...")
        cropImages.cropImageToPieces(inputImageFile, width, height, outputNamesPerLine, outputDirName, continuousIndices, xOffset, yOffset, xOffsetStartsBeforeImage, yOffsetStartsBeforeImage, numImages)
        print("\ndone")
    except Exception as e:
        print("errors occured while trying to crop the image: " + str(e))
        sys.exit(1)
    
    print("\n\n ### Resizing images #########################################################################\n")
    try:
        print("resizing images...")
        resizeImages.resizeImages(outputDirName, scaleFactor)
        print("\ndone")
    except Exception as e:
        print("errors occured while trying to scale the images: " + str(e))
        sys.exit(1)
        
    print("\n\n ### Combining images ########################################################################\n")
    try:
        print("combining images...")
        combineImages.combineImages(outputDirName + "/scaled", imagesPerLine, margin, combinedImageName)
        print("\ndone")
    except Exception as e:
        print("errors occured while trying to combine the images: " + str(e))
        sys.exit(1)
        
    print("\n\nRearranging tileset done\n")
    