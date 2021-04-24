import GetFiles
import MethodExtractor
import CloneDetector
import CloneSave
import time

time_start = time.process_time()
#run your code

# allFilesData is list which have all files with specific extension
print("Getting all file info from folder")
allFilesData = GetFiles.getAllFilesUsingFolderPath()
time_elapsed = (time.process_time() - time_start)
print("Time elapsed till Getting File info:", time_elapsed)

print("Extracting methods from files")
codeBlocks = MethodExtractor.extractMethodsAllFiles(allFilesData)
time_elapsed = (time.process_time() - time_start)
# codeBlocksWithClonePairsType1 = TypeOneDetector.detectClone(allFilesMethods)
# print(codeBlocksWithClonePairsType1)
print("Time elapsed till Method Extraction:", time_elapsed)
print("Detecting clones")
CloneDetector.detectClone(codeBlocks)
time_elapsed = (time.process_time() - time_start)
print("Time elapsed till Clone detection:", time_elapsed)
print("Saving to CSV")
# CloneSave.writeToFile(codeBlocks)
CloneSave.writeToCSV(codeBlocks)
time_elapsed = (time.process_time() - time_start)
print("Completion Time:", time_elapsed)
