import csv

def compareTwoBlocksInfo(info_lst = []):
    firstFileInfo = info_lst[0]
    if len(info_lst) > 2:
        firstStart = info_lst[1]
        firstEnd = info_lst[2]

        secondFileInfo = info_lst[3]
        secondStart = info_lst[4]
        secondEnd = info_lst[5]
    else:
        secondFileInfo = info_lst[1]

    if firstFileInfo < secondFileInfo:
        return True
    elif len(info_lst) <= 2:
        return False
    elif firstFileInfo == secondFileInfo and firstStart < secondStart:
        return True
    elif firstFileInfo == secondFileInfo and firstStart == secondStart and firstEnd < secondEnd:
        return True
    return False

clonesDetectedSet = set()
clonesFromDBSet = set()


# E:/DataSetExtractor/clonesFromDBOnlyFunctions4.csv
# E:/CodeCloneDetection/clonesFromDB7.csv
ClonesFromDBfile = open('E:/DataSetExtractor/clonesFromDB.csv', 'r', encoding='utf-8')


ClonesDetectedfile = open('clonesDetected.csv', 'r', encoding='utf-8')

for line in ClonesDetectedfile.readlines():
    line = line.rstrip()

    lst_line = line.split(",")
    if compareTwoBlocksInfo(lst_line) == True:
        key = line
    else:
        if len(lst_line) > 2:
            key = str(lst_line[3]) + "," + str(lst_line[4]) + "," + str(lst_line[5]) + "," + str(lst_line[0]) + "," + str(lst_line[1]) + "," + str(lst_line[2])
        else:
            key = str(lst_line[1]) + "," + str(lst_line[0])

    clonesDetectedSet.add(key)
ClonesDetectedfile.close()



for line in ClonesFromDBfile.readlines():
    line = line.rstrip()
    lst_line = line.split(",")
    if compareTwoBlocksInfo(lst_line) == True:
        key = line
    else:
        if len(lst_line) > 2:
            key = str(lst_line[3]) + "," + str(lst_line[4]) + "," + str(lst_line[5]) + "," + str(lst_line[0]) + "," + str(lst_line[1]) + "," + str(lst_line[2])
        else:
            key = str(lst_line[1]) + "," + str(lst_line[0])

    clonesFromDBSet.add(key)        
ClonesFromDBfile.close()

intersectionSet = clonesDetectedSet.intersection(clonesFromDBSet)

if len(clonesDetectedSet) == 0 or len(clonesFromDBSet) == 0:
    print("Wrong")
else:
    print("Precision : ", (len(intersectionSet)/len(clonesDetectedSet))*100)
    print("Recall : " , (len(intersectionSet)/len(clonesFromDBSet))*100)