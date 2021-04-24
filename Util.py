import math


def getFrequencyFromList(lst):
    dict_freq = {}
    for token in lst:
        if token in dict_freq.keys():
            dict_freq[token] = dict_freq[token] + 1
        else:
            dict_freq[token] = 1

    return dict_freq


def getMostFrequent(dict_freq, threshold=1):
    lst_token_freq = sorted(
        dict_freq.items(), key=lambda kv: kv[1], reverse=True)
    lst_token = []
    for idx in range(math.ceil(len(lst_token_freq)*threshold)):
        if idx >= len(lst_token_freq):
            break
        lst_token.append(lst_token_freq[idx][0])
    return lst_token

def compareTwoBlocksInfo(info_lst = []):
    firstFileInfo = info_lst[0]
    firstStart = info_lst[1]
    firstEnd = info_lst[2]

    secondFileInfo = info_lst[3]
    secondStart = info_lst[4]
    secondEnd = info_lst[5]
    if firstFileInfo < secondFileInfo:
        return True
    elif firstFileInfo == secondFileInfo and firstStart < secondStart:
        return True
    elif firstFileInfo == secondFileInfo and firstStart == secondStart and firstEnd < secondEnd:
        return True
    return False