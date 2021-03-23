import sys
import os
import Config
import re
def tokenizeAllFiles(listOfFiles, granularity):
    allFilesTokens = []
    for filePath in listOfFiles:
        file = open(filePath, 'r')
        originalCode = file.readlines()
        file.close()
        if granularity == 1:
            codeBlocks = methodLevelBlocks(originalCode)
        else:
            codeBlocks = fileLevelBlocks(originalCode)  

        allFilesTokens.append({filePath : codeBlocks})
    return allFilesTokens
def fileLevelBlocks(originalCode):
    """
    input : originalCode
    output : blocks using file level
    """

    allCodeBlocks = []
    commentsRemovedCode = removeCommentsFromCode(originalCode)
    startLine = 1
    endLine = len(commentsRemovedCode)
    allCodeBlocks.append({"Start" : startLine, "End" : endLine, "Code" : commentsRemovedCode})
    return allCodeBlocks   

def methodLevelBlocks(originalCode):
    """
    input : originalCode
    output : blocks using method level
    """

    allCodeBlocks = []
    bracketStack = 0
    commentsRemovedCode = removeCommentsFromCode(originalCode)
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

def removeCommentsFromCode(originalCode):
    """
    input : original Code
    output : code without comments 
    """
    
    DEFAULT = 1
    ESCAPE = 2
    STRING = 3
    ONE_LINE_COMMENT = 4
    MULTI_LINE_COMMENT = 5

    mode = DEFAULT
    strippedCode = []
    for line in originalCode:
        strippedLine = ""
        idx = 0
        while idx < len(line):
            subString = line[idx: min(idx + 2, len(line))]
            c = line[idx]
            if mode == DEFAULT : 
                mode = MULTI_LINE_COMMENT if subString == "/*" else ONE_LINE_COMMENT if subString == "//" else STRING if c == '\"' else DEFAULT
            elif mode == STRING :
                mode = DEFAULT if c == '\"' else ESCAPE if c == '\\' else STRING
            elif mode == ESCAPE :
                mode = STRING
            elif mode == ONE_LINE_COMMENT :
                mode = DEFAULT if c == '\n' else ONE_LINE_COMMENT
                idx += 1
                continue
            elif mode == MULTI_LINE_COMMENT :
                mode = DEFAULT if subString == "*/" else MULTI_LINE_COMMENT
                idx += 2 if mode == DEFAULT else 1
                continue
            strippedLine += c if mode < 4 else "" 
            idx += 1
        if len(strippedLine) > 0 and strippedLine[-1] == '\n' :
            strippedLine = strippedLine[:-1] 
        strippedCode.append(strippedLine)
    return strippedCode
