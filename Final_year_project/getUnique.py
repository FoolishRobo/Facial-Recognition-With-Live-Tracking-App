def unique(list_name, noOfUsers):
    unique_list = []
    for a in list_name:
        if a not in unique_list:
            unique_list.append(a)
    unique_list.sort()
    return unique_list

# list_name = [25,2,3,56,5,25,2,25}
# unique = unique(list_name)
# print("Unique id: {}".format(unique))