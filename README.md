# LibGDX image tools

A collection of python scripts to manipulate images to use them in libGDX (or other engines)

## Scripts

- **cropImages.py**: Crops an image into pieces of defined size, offsets, names, ... (to put them a texture atlas)
- **resizeImages.py**: Resizes all images in a directory
- **addImagePadding.py**: Adds a padding to all images in a directory, so that the padding pixesl are a copy of the edge pixels
- **combineImages.py**: Combines all images in a directory into one image
- **reArrangeTileset.py**: All of the above: Crop the tileset into pieces, scale it and put it back together

## Config files

- **crop.config**: A demo configuration file for the **cropImages.py** script
- **rearrange_tileset.config**: A demo configuration file for the **reArrangeTileset.py** script

## Demos

- **dwarf.config**: A demo configuration to crop the image file 'Dwarf_Sprite_Sheet1.2v.png'
- **items.config**: A demo configuration to crop the image file 'rpgItems.png'
- **rearrange_tileset.config**: A demo configuration to rearrange the image file 'rpg_nature_tileset.png'

(All of the images used here are available (for free) on itch.io)
