import jaydebeapi
import os
import sys
import csv


def getAllFilesUsingFolderPath(folderPath):
    allFilesInFolder = []
    maxCount = 1000
    currentCount = 0
    if os.path.exists(folderPath):
        fileNames = os.listdir(folderPath)
        for fileName in fileNames:
            currentCount += 1
            if(currentCount >= maxCount):
                break
            if fileName.split(".")[-1] != "java":
                continue
            allFilesInFolder.append(fileName)
    return allFilesInFolder


path = "F:/8th-Sem-Project/BigCloneEval/ijadataset/bcb_reduced/4/selected"
print("getting all files")
allFilesInFolder = getAllFilesUsingFolderPath(path)
print("all files accesed")
allFilesString = "("
for i in range(len(allFilesInFolder)):
    file = allFilesInFolder[i]
    allFilesString += "'" + str(file) + "'"
    if i != len(allFilesInFolder)-1:
        allFilesString += ", "

allFilesString += ')'
print("string created")
print("Connecting to DB")
conn = jaydebeapi.connect("org.h2.Driver",  # driver class
                          "jdbc:h2:file:F:/8th-Sem-Project/BigCloneEval/bigclonebenchdb/bcb",  # JDBC url
                          ["sa", ""],  # credentials
                          "F:\8th-Sem-Project\src\CodeCloneDetection\h2-1.4.200.jar",)  # location of H2 jar

print("Connection successful")
curs = conn.cursor()
query = """SELECT T1.NAME , T1.STARTLINE, T1.ENDLINE, T2.NAME, T2.STARTLINE, T2.ENDLINE
FROM CLONES AS C1 , FUNCTIONS AS T1, FUNCTIONS AS T2
WHERE T1.ID = C1.FUNCTION_ID_ONE
AND T1.NAME IN {fileList}
AND T2.NAME IN {fileList}
AND T2.ID = C1.FUNCTION_ID_TWO
AND C1.FUNCTIONALITY_ID = 4
AND C1.SIMILARITY_TOKEN > 0.6;""".format(fileList=allFilesString)

# print(query)
print("Query execution initiated")
curs.execute(query)
print("Query execution successful")

with open('clones.csv', 'w', newline='') as csv_f:
    csv_writer = csv.writer(csv_f)
    for value in curs.fetchall():
        # the values are returned as wrapped java.lang.Long instances
        # invoke the toString() method to print them
        csv_writer.writerow(value)
