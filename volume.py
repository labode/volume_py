import numpy as np
import converter
import csv_writer
import nrrd
import sys


# TODO: supply voxel size and calculate volume here?
def analyze(file):
    # Read .nrrd
    data, header = nrrd.read(file)
    entries = np.unique(data)
    count = []

    # For each label => Count number of pixels
    for entry in entries:
        # We do not need the zeroes (= background label)
        if entry == 0:
            continue

        occurrence = np.count_nonzero(data == entry)
        count.append([entry, occurrence])

    return count


if __name__ == '__main__':
    # Get volume to analyze
    try:
        mha_file = sys.argv[1]
        output = sys.argv[2]
    except IndexError:
        sys.exit('Missing parameters \nPlease supply: volume file, output file name')

    # Convert volume to .nrrd
    nrrd_file = converter.convert(mha_file, 'volume')
    analysis = analyze(nrrd_file)
    # Write .csv with the results
    csv_writer.write(analysis, output)
