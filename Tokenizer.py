import sys
import os
import Config
def tokenizeAllFiles(listOfFiles, granularity):
    allFilesTokens = []
    for filePath in listOfFiles:
        if granularity == 1:
            fileTokens = methodLevelBlocks(filePath)
        else:
            fileTokens = fileLevelBlocks(filePath)  
        allFilesTokens.append({filePath : fileTokens})
    return allFilesTokens
def fileLevelBlocks(filePath):
    """
    input : filePath
    output : blocks using file level
    """
    allCodeBlocks = []
    commentsRemovedCode = removeCommentsFromCode(filePath)
    startLine = 1
    endLine = len(commentsRemovedCode)
    allCodeBlocks.append({"Start" : startLine, "End" : endLine, "Code" : commentsRemovedCode})
    return allCodeBlocks   

def methodLevelBlocks(filePath):
    """
    input : filepath
    output : blocks using method level
    """
    allCodeBlocks = []
    bracketStack = 0
    commentsRemovedCode = removeCommentsFromCode(filePath)
    lineNumber = 0
    startLine = -1
    endLine = -1
    currentCodeBlock = []
    quote = False
    for line in commentsRemovedCode:
        lineNumber += 1
        line = line.strip()
        currentCodeBlock.append(line)
        if not line:
            continue
        for idx in range(0, len(line)):
            char = line[idx]
            if char == "\"":
                quote = quote ^ True

            if quote == False:
                if char == "{" :
                    bracketStack += 1
                    if bracketStack == 1:
                        startLine = lineNumber
                        currentCodeBlock = [line]
                elif char == "}" :
                    bracketStack += -1
                    if bracketStack == 0:
                        endLine = lineNumber
                        allCodeBlocks.append({"Start" : startLine, "End" : endLine, "Code" : currentCodeBlock})   
                        break
    return allCodeBlocks

def removeCommentsFromCode(filePath):
    """
    input : filePath
    output: line by line code without comments 
    """
    strippedCode = []
    quote = 0
    comment = 0
    file = open(filePath, "r")
    for line in file.readlines():
        line = line.strip()
        strippedLine = []
        for idx in range(0, len(line)):
            ch = line[idx]
            if ch == '\\':
                if comment:
                    continue
                strippedLine.append(line[idx:idx + 2])
            elif ch  in ('\"', '\'') :
                if comment:
                    continue
                strippedLine.append(ch)
                if quote == 0:
                    quote = ch
                elif quote == ch:
                    quote = 0
            elif ch == '/':
                if quote:
                    strippedLine.append(ch)
                elif idx + 1 < len(line) and line[idx + 1] == '/':
                    strippedLine.append('\n')
                    break
                elif idx + 1 < len(line) and line[idx + 1] == '*':
                    comment = 1
                    idx += 1
                elif comment == 0:
                    strippedLine.append(line[idx])
            elif ch == '*':
                if quote:
                    strippedLine.append(ch)
                elif comment == 1 and idx + 1 < len(line) and line[idx + 1] == '/':
                    comment = 0
                    idx += 1
                    continue
                elif comment == 1:
                    continue
                strippedLine.append(line[idx])
            else:
                if comment == 0:
                    strippedLine.append(ch)
        strippedCode.append(''.join(strippedLine))
    file.close()
    return strippedCode