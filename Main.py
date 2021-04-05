import GetFiles
import MethodExtractor
import CloneDetector
import CloneSave
dirPath = "E:\CodeFiles\Sample"
outputPath = "E:\CodeCloneDetection\output.txt"

#This will be used as level for output into file
#0 means everything
#1 means current block's code and only clone blocks info
#2 means only current block's and clone block's info
outputLevel = 1

# Threshhold for considering as code clones
#Threshhold = 1 for type 2 clones
threshold = 0.6

# Threshold for considering most frequent variables and methods 
variableAndMethodsThreshold = 0.8

# Block level can be 0 = (file level) or 1 = (method level)
granularity = 0


#allFilesData is list which have all files with specific extension
allFilesData = GetFiles.getAllFilesUsingFolderPath(dirPath)


codeBlocks = MethodExtractor.extractMethodsAllFiles(allFilesData, granularity)
# codeBlocksWithClonePairsType1 = TypeOneDetector.detectClone(allFilesMethods)
# print(codeBlocksWithClonePairsType1)

CloneDetector.detectClone(codeBlocks, threshold, variableAndMethodsThreshold)

CloneSave.writeToFile(codeBlocks, outputPath, outputLevel)

