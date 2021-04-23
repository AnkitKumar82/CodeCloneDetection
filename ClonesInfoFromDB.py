import jaydebeapi
import os
import sys
import csv


def getAllFilesUsingFolderPath(folderPath):
    allFilesInFolder = []
    maxCount = 100
    currentCount = 0
    if os.path.exists(folderPath):
        fileNames = os.listdir(folderPath)
        for fileName in fileNames:
            currentCount += 1

            if fileName.split(".")[-1] != "java":
                continue
            allFilesInFolder.append(fileName)
            if(currentCount > maxCount):
                break
    return allFilesInFolder


path = "F:/8th-Sem-Project/BigCloneEval/ijadataset/bcb_reduced/4/sample"
allFilesInFolder = getAllFilesUsingFolderPath(path)
allFilesString = "("
for i in range(len(allFilesInFolder)):
    file = allFilesInFolder[i]
    allFilesString += "'" + str(file) + "'"
    if i != len(allFilesInFolder)-1:
        allFilesString += ", "

allFilesString += ')'
conn = jaydebeapi.connect("org.h2.Driver",  # driver class
                          "jdbc:h2:file:F:/8th-Sem-Project/BigCloneEval/bigclonebenchdb/bcb",  # JDBC url
                          ["sa", ""],  # credentials
                          "F:\8th-Sem-Project\src\CodeCloneDetection\h2-1.4.200.jar",)  # location of H2 jar

curs = conn.cursor()
query = """SELECT T1.NAME , T1.STARTLINE, T1.ENDLINE, T2.NAME, T2.STARTLINE, T2.ENDLINE
FROM CLONES AS C1 , FUNCTIONS AS T1, FUNCTIONS AS T2
WHERE T1.ID = C1.FUNCTION_ID_ONE
AND T1.NAME IN {fileList}
AND T2.NAME IN {fileList}
AND T2.ID = C1.FUNCTION_ID_TWO;""".format(fileList=allFilesString)
print("Query executing")
curs.execute(query)
print("Saving to CSV")
with open('clonesFromDB.csv', 'w', newline='') as csv_f:
    csv_writer = csv.writer(csv_f)
    for value in curs.fetchall():
        # the values are returned as wrapped java.lang.Long instances
        # invoke the toString() method to print them
        csv_writer.writerow(value)
csv_f.close()
