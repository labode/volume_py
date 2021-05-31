import itk


def convert(volume, filename):
    image = itk.imread(volume)
    filename = filename + '.nrrd'
    itk.imwrite(image, filename)

    return filename
