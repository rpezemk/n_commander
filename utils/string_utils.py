def group_by_n(input_list, n):
    grouped = []
    for i in range(0, len(input_list), n):
        grouped.append(input_list[i:i + n])
    return grouped

def list_to_columns(maxH: int, maxW: int, list) -> list[str]:
    groups = group_by_n(list, max(1, maxH))
    nGroups = len(groups)
    if nGroups == 0:
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