def manipulate_data():
    for index in range(len(data_to_manipulate)):
        data_to_manipulate[index] = data_to_manipulate[index] + 1
        backup[str(index)] = "Modified"