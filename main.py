import numpy as np
import converter
import csv_writer
import nrrd
import sys


def analyze(file):
    # TODO: Read .nrrd
    data = nrrd.read(file)
    entries = np.unique(data)
    count = []

    # TODO: For each label => Count number of pixels
    for entry in entries:
        # We do not need the zeroes (= background label)
        if entry == 0:
            continue

        occurrence = np.count_nonzero(data == entry)
        count.append([entry, occurrence])

    return count


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # TODO: Get volume to analyze
    mha_file = sys.argv[1]

    error = False
    if not mha_file:
        error = True

    if not error:
        # TODO: Convert volume to .nrrd
        nrrd_file = converter.convert(mha_file, 'volume')
        analysis = analyze(nrrd_file)
        # TODO: Write .csv with the results
        csv_writer.write(analysis, 'sizes')

    else:
        print('No volume file supplied')
