import GetFiles
import CodeBlockExtractor
import CloneDetector
import CloneSave
import time
import tracemalloc

tracemalloc.start()
time_start = time.process_time()
#run your code

# allFilesData is list which have all files with specific extension
print("Getting all file info from folder")
allFilesData = GetFiles.getAllFilesUsingFolderPath()
time_elapsed = (time.process_time() - time_start)
print("Time elapsed till Getting File info:", time_elapsed)

print("Extracting methods from files")
codeBlocks = CodeBlockExtractor.extractCodeBlocksAllFiles(allFilesData)
time_elapsed = (time.process_time() - time_start)
# codeBlocksWithClonePairsType1 = TypeOneDetector.detectClone(allFilesMethods)
# print(codeBlocksWithClonePairsType1)
print("Total Code Blocks : ", len(codeBlocks))
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
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
tracemalloc.stop()
