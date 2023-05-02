import itertools
import os
import numpy as np
import converter
import csv_writer
import nrrd
import sys
import time
from multiprocessing.dummy import Pool as ThreadPool


def analyze(file, size_x, size_y, size_z, threads):
    # Read .nrrd
    data, header = nrrd.read(file)
    entries = np.unique(data)

    number_entries = len(entries)
    print(str(number_entries - 1) + ' labels found (excluding background label)')

    entries = np.delete(entries, np.where(entries == 0))

    # https://stackoverflow.com/questions/2846653/how-can-i-use-threading-in-python
    pool = ThreadPool(threads)
    volumes = pool.starmap(calculate_volume, zip(entries, itertools.repeat(data), itertools.repeat(size_x),
                                                 itertools.repeat(size_y), itertools.repeat(size_z)))

    pool.close()
    pool.join()

    return volumes


def calculate_volume(label, data, size_x, size_y, size_z):
    occurrences = np.count_nonzero(data == label)
    volume = round(occurrences * (size_x * size_y * size_z), 2)
    print([label, volume])

    return [label, volume]


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
    analysis = analyze(nrrd_file, voxel_size_x, voxel_size_y, voxel_size_z, 16)

    # Cleanup
    print('Removing temp file')
    os.remove(nrrd_tmpfile + '.nrrd')

    # Write .csv with the results
    print('Writing analysis to .csv')
    csv_writer.write(analysis, output)
