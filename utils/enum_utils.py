def group_by_n(input_list, n):
    grouped = []
    for i in range(0, len(input_list), n):
        grouped.append(input_list[i:i + n])
    return grouped