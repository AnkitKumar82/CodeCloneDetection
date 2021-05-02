import os
import sys
import Config


def getAllFilesUsingFolderPath():
    folderPath = Config.dirPath
    allFilesInFolder = []
    if os.path.exists(folderPath):
        fileNames = os.listdir(folderPath)
        for fileName in fileNames:
            if fileName.split(".")[-1] != "java":
                continue
            fileFullPath = os.path.join(folderPath, fileName)
            allFilesInFolder.append(fileFullPath)
    return allFilesInFolder
