import os
import sys
def getAllFilesUsingFolderPath(folderPath):
    allFilesInFolder = []
    fileCount = 0
    maxCount = 100
    if os.path.exists(folderPath):
        fileNames = os.listdir(folderPath)
        for fileName in fileNames:
            fileCount += 1
            if fileName.split(".")[-1] != "java":
                continue
            fileFullPath = os.path.join(folderPath, fileName)
            allFilesInFolder.append(fileFullPath)
            if fileCount > maxCount:
                break
    return allFilesInFolder