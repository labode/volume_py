import itertools
import argparse
import os
import numpy as np
import converter
import csv_writer
import nrrd
import time
from multiprocessing.dummy import Pool as ThreadPool


def analyze(file, size_x, size_y, size_z, number_threads):
    # Read .nrrd
    data, header = nrrd.read(file)
    entries = np.unique(data)

    number_entries = len(entries)
    print(str(number_entries - 1) + ' labels found (excluding background label)')

    entries = np.delete(entries, np.where(entries == 0))

    # https://stackoverflow.com/questions/2846653/how-can-i-use-threading-in-python
    pool = ThreadPool(number_threads)
    volumes = pool.starmap(calculate_volume, zip(entries, itertools.repeat(data), itertools.repeat(size_x),
                                                 itertools.repeat(size_y), itertools.repeat(size_z)))

    pool.close()
    pool.join()

    return volumes


def calculate_volume(label, data, size_x, size_y, size_z):
    occurrences = np.count_nonzero(data == label)
    volume = round(occurrences * (size_x * size_y * size_z), 2)

    return [label, volume]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculates the volume of labels in a .mha file')
    parser.add_argument('input_file', action='store', type=str, help='.mha file to analyze')
    parser.add_argument('-o', '--output_file', action='store', type=str, default='analysis.csv', required=False,
                        help='Name of output file; Default: analysis.csv')
    parser.add_argument('-x', '--size_x', action='store', type=float, default=1, required=False,
                        help='Voxel size X; If not supplied, 1 is used')
    parser.add_argument('-y', '--size_y', action='store', type=float, default=1, required=False,
                        help='Voxel size Y; If not supplied, 1 is used')
    parser.add_argument('-z', '--size_z', action='store', type=float, default=1, required=False,
                        help='Voxel size Z; If not supplied, 1 is used')
    parser.add_argument('-t', '--threads', action='store', type=int, default=1, required=False,
                        help='Number of threads to use; Default: 1')

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    voxel_size_x = args.size_x
    voxel_size_y = args.size_y
    voxel_size_z = args.size_z
    threads = args.threads

    # create name for .nrrd that is unique enough not to cause accidental conflicts
    nrrd_tmpfile = 'volume_' + str(int(time.time()))

    # Convert volume to .nrrd
    print('Converting .mha to .nrrd')
    nrrd_file = converter.convert(input_file, nrrd_tmpfile)
    print('Temp .nrrd file written to ' + nrrd_tmpfile + '.nrrd')

    # Analyze .nrrd
    print('Analysing .nrrd')
    analysis = analyze(nrrd_file, voxel_size_x, voxel_size_y, voxel_size_z, threads)

    # Cleanup
    print('Removing temp file')
    os.remove(nrrd_tmpfile + '.nrrd')

    # Write .csv with the results
    print('Writing analysis to .csv')
    csv_writer.write(analysis, output_file)
