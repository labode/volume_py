import os
import numpy as np
import converter
import csv_writer
import nrrd
import sys
import time


def analyze(file, size_x, size_y, size_z):
    # Read .nrrd
    data, header = nrrd.read(file)
    entries = np.unique(data)

    number_entries = len(entries)
    print(str(number_entries) + ' labels found (excluding background label)')

    volumes = calculate_volume(entries, data, size_x, size_y, size_z)

    return volumes


def calculate_volume(labels, data, size_x, size_y, size_z):
    volumes = []
    for label in labels:
        if label == 0:
            continue

        occurrences = np.count_nonzero(data == label)
        volume = round(occurrences * (size_x * size_y * size_z), 2)
        volumes.append([label, volume])

    return volumes


if __name__ == '__main__':
    # Get volume to analyze
    try:
        mha_file = sys.argv[1]
        output = sys.argv[2]
    except IndexError:
        sys.exit('Missing parameters \nPlease supply: volume file, output file name')

    # If the user supplies the voxel size, we use it to calculate the volume.
    # Otherwise, we use 1
    # We accommodate non-symmetrical voxel sizes
    try:
        voxel_size_x = float(sys.argv[3])
        voxel_size_y = float(sys.argv[4])
        voxel_size_z = float(sys.argv[5])
    except IndexError:
        print('No voxel size supplied, output will be given as voxel count')
        voxel_size_x = voxel_size_y = voxel_size_z = 1

    # create name for .nrrd that is unique enough not to cause accidental conflicts
    nrrd_tmpfile = 'volume_' + str(int(time.time()))

    # Convert volume to .nrrd
    print('Converting .mha to .nrrd')
    nrrd_file = converter.convert(mha_file, nrrd_tmpfile)
    print('Temp .nrrd file written to ' + nrrd_tmpfile + '.nrrd')

    # Analyze .nrrd
    print('Analysing .nrrd')
    analysis = analyze(nrrd_file, voxel_size_x, voxel_size_y, voxel_size_z)

    # Cleanup
    print('Removing temp file')
    os.remove(nrrd_tmpfile + '.nrrd')

    # Write .csv with the results
    print('Writing analysis to .csv')
    csv_writer.write(analysis, output)
