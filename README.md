# Volume calculator
Tool to calculate the volume of each label in a labeled volume image.
Intended for use with https://github.com/labode/genana_py id assignment

## How does it work?
- Takes .mha volume image and converts it to .nrrd
- reads .nrrd into numpy array
- counts distinct labels in array
- counts number of occurrences (= number of voxels) per label
- writes the measurements into .csv

## Requirements
Required packages are listed in requirements.txt and can be installed using pip as follows:\
`pip3 install -r requirements.txt`

## Input
- .mha volume file
- Output Filename
- Optional: voxel size x, y, z

## Output
- .csv containing id and number voxels (rounded down to two positions after decimal point, use appropriate voxel size unit)

## Usage
`python3 volume.py volume.mha outputfile 2 2 2`
