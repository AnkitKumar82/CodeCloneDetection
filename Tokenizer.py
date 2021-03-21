import sys
import os
import Config
import re
def tokenizeAllFiles(listOfFiles, granularity):
    allFilesTokens = []
    for filePath in listOfFiles:
        
        if granularity == 1:
            codeBlocks = methodLevelBlocks(filePath)
        else:
            codeBlocks = fileLevelBlocks(filePath)  

        allFilesTokens.append({filePath : codeBlocks})
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
    output : code without comments 
    """
    file = open(filePath, "r")
    originalCode = open(filePath, "r").read()
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        if match.group(2) is not None:
            return ""
        else:
            return match.group(1)
    file.close()
    return regex.sub(_replacer, originalCode)