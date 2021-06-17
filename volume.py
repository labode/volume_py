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

    count = []

    i = 0
    # For each label => Count number of pixels
    for entry in entries:
        print(str(round(i/(number_entries/100), 2)) + '% analysed')
        # We do not need the zeroes (= background label)
        if entry == 0:
            continue

        occurrences = np.count_nonzero(data == entry)
        volume = round(occurrences * (size_x * size_y * size_z), 2)
        count.append([entry, volume])

        i += 1

    return count


if __name__ == '__main__':
    # Get volume to analyze
    try:
        mha_file = sys.argv[1]
        output = sys.argv[2]
    except IndexError:
        sys.exit('Missing parameters \nPlease supply: volume file, output file name')

    # If the user supplies the voxel size, we use it to calculate the volume.
    # Otherwise we use 1
    # We accommodate non symmetrical voxel sizes
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
    print('Temporary converted file writte to ' + nrrd_tmpfile + '.nrrd')
    # Analyze .nrrd
    print('Analysing .nrrd')
    analysis = analyze(nrrd_file, voxel_size_x, voxel_size_y, voxel_size_z)
    # Cleanup
    print('Removing temporary file')
    os.remove(nrrd_tmpfile + '.nrrd')
    # Write .csv with the results
    print('Writing analysis to .csv')
    csv_writer.write(analysis, output)
