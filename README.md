# Volume calculator
Tool to calculate the volume of each label in a labeled volume image.
Intended for use with https://github.com/labode/genana_py id assignment

## How does it work?
- Takes .mha volume image and converts it to .nrrd
- reads .nrrd into numpy array
- counts distinct labels in array
- counts number of occurrences (= number of voxels) per label
- writes the measurements into .csv

## Input
- .mha volume file

## Output
- .csv containing id and number voxels

## Usage
`python main.py volume.mha outputfile`