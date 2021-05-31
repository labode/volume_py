def write(data, target_file):
    # Initiate File
    filename = str(target_file) + ".csv"
    output_file = open(filename, "w")

     # Write header
    output_file.write("id; size;\n")

    for i in data:
        output_file.write(str(i[0]) + '; ' + str(i[1]) + ';\n')
