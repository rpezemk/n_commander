def wrap_lines(input_str: str, max_first_width, max_others_width):
    first = input_str[:max_first_width]
    others = input_str[max_first_width:]

    grouped = [first]

    for i in range(0, len(others), max_others_width):
        grouped.append(others[i : i + max_others_width])
    return grouped


def split_by_n_chars(input_str, maxWidth):
    grouped = []
    for i in range(0, len(input_str), maxWidth):
        grouped.append(input_str[i : i + maxWidth])
    return grouped


def group_by_n(input_list, n):
    grouped = []
    for i in range(0, len(input_list), n):
        grouped.append(input_list[i : i + n])
    return grouped

def group_elements_by_n(input_list, n):
    grouped = []
    for i in range(0, len(input_list), n):
        sub = list(input_list[i : i + n])
        t = type(sub)
        grouped.append(sub)
    return grouped

def list_to_columns(maxH: int, maxW: int, list) -> list[str]:
    groups = group_by_n(list, max(1, maxH))
    nGroups = len(groups)
    if not nGroups:
        return []

    firstGroupLen = len(groups[0])
    lastGroupLen = len(groups[-1])
    resList = []
    groupWidths = [max([len(s) for s in lst]) + 2 for lst in groups]
    for i in range(lastGroupLen):
        subRes = ""
        subResList = []
        for groupCnt in range(nGroups):
            subResList.append(groups[groupCnt][i])

        for groupCnt in range(nGroups):
            subRes += subResList[groupCnt].ljust(groupWidths[groupCnt])
        resList.append(subRes)

    for i in range(lastGroupLen, firstGroupLen):
        subRes = ""
        subResList = []
        for groupCnt in range(nGroups - 1):
            subResList.append(groups[groupCnt][i])

        for groupCnt in range(nGroups - 1):
            subRes += subResList[groupCnt].ljust(groupWidths[groupCnt])
        resList.append(subRes)
    return resList
