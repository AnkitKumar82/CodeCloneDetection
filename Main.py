import GetFiles
import MethodExtractor
import CloneDetector
import CloneSave

# allFilesData is list which have all files with specific extension
print("Getting all file info from folder")
allFilesData = GetFiles.getAllFilesUsingFolderPath()
print("Extracting methods from files")
codeBlocks = MethodExtractor.extractMethodsAllFiles(allFilesData)
# codeBlocksWithClonePairsType1 = TypeOneDetector.detectClone(allFilesMethods)
# print(codeBlocksWithClonePairsType1)
print("Detecting clones")
CloneDetector.detectClone(codeBlocks)
print("Saving to CSV")
# CloneSave.writeToFile(codeBlocks)
CloneSave.writeToCSV(codeBlocks)
