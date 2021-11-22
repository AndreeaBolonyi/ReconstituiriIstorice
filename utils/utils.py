def get_list_of_values(dictionary):
    values_list = []
    for value in dictionary.items():
        values_list.append(value[1])

    return values_list
