import GetFiles
import Tokenizer
dirPath = "E:\CodeFiles\Sample"

granularity = 0 #Block level can be 0 = (file level) or 1 = (method level)

allFilesData = GetFiles.getAllFilesUsingFolderPath(dirPath)
allFilesTokens = Tokenizer.tokenizeAllFiles(allFilesData, granularity)
print(allFilesTokens)
