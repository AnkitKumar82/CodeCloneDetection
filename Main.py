import GetFiles
import Tokenizer
dirPath = "E:\CPPFiles"

allFilesData = GetFiles.getAllFilesUsingFolderPath(dirPath)
# print(allFilesData)
allFilesTokens = Tokenizer.tokenizeAllFiles(allFilesData)
print(allFilesTokens)
# for file in allFilesTokens:
#     for blocks in file:
#         for block in file[blocks]:
#             for idx in range(len(block)):
#                 print("start : ", block['Start'], "end: ", block["End"])
#                 for code in block["Code"]:
#                     print(code)