def write(data, target_file):
    # Initiate File
    output_file = open(target_file, "w")

    # Write header
    output_file.write("Id; Volume\n")

    for i in data:
        output_file.write(str(i[0]) + '; ' + str(i[1]) + '\n')

    output_file.close()
