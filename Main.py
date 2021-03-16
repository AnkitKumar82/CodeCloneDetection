import GetFiles
import Tokenizer
dirPath = "E:\CPPFiles\Single"

granularity = 1 #Block level can be 0 = (file level) or 1 = (method level)

allFilesData = GetFiles.getAllFilesUsingFolderPath(dirPath)
allFilesTokens = Tokenizer.tokenizeAllFiles(allFilesData, granularity)
print(allFilesTokens)
