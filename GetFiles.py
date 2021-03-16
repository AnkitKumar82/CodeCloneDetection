import os
import sys
def getAllFilesUsingFolderPath(folderPath):
    allFilesInFolder = []
    if os.path.exists(folderPath):
        fileNames = os.listdir(folderPath)
        for fileName in fileNames:
            if fileName.split(".")[-1] != "cpp":
                continue
            fileFullPath = os.path.join(folderPath, fileName)
            allFilesInFolder.append(fileFullPath)
    return allFilesInFolder