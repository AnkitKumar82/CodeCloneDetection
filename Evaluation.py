import csv

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

clonesDetectedSet = set()
clonesFromDBSet = set()


ClonesDetectedfile = open('clonesDetected.csv', 'r', encoding='utf-8')
for line in ClonesDetectedfile.readlines():
    line = line.rstrip()
    clonesDetectedSet.add(line)
ClonesDetectedfile.close()



ClonesFromDBfile = open('clonesFromDB.csv', 'r', encoding='utf-8')

for line in ClonesFromDBfile.readlines():
    line = line.rstrip()
    lst_line = line.split(",")
    if compareTwoBlocksInfo(lst_line) == True:
        key = line
    else:
        key = str(lst_line[3]) + "," + str(lst_line[4]) + "," + str(lst_line[5]) + "," + str(lst_line[0]) + "," + str(lst_line[1]) + "," + str(lst_line[2])
    clonesFromDBSet.add(key)        
ClonesFromDBfile.close()

intersectionSet = clonesDetectedSet.intersection(clonesFromDBSet)

if len(clonesDetectedSet) == 0 or len(clonesFromDBSet) == 0:
    print("Wrong")
else:
    print("Precision : ", (len(intersectionSet)/len(clonesDetectedSet))*100)
    print("Recall : " , (len(intersectionSet)/len(clonesFromDBSet))*100)