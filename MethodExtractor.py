import sys
import os
import Config
import re
import GetFunctions


def extractMethodsAllFiles(listOfFiles, granularity):
    allFilesMethodsBlocks = {}
    blocksSoFar = 0
    for filePath in listOfFiles:
        file = open(filePath, 'r', encoding='utf-8')
        originalCode = file.readlines()
        file.close()
        if granularity == 1:
            codeBlocks = methodLevelBlocks(originalCode)
        else:
            codeBlocks = fileLevelBlocks(originalCode)
        for codeBlock in codeBlocks:
            codeBlock.update({"FileInfo": filePath})
            blocksSoFar += 1
            allFilesMethodsBlocks["CodeBlock" + str(blocksSoFar)] = codeBlock
    return allFilesMethodsBlocks


def fileLevelBlocks(originalCode):
    """
    input : originalCode
    output : blocks using file level
    """

    allCodeBlocks = []
    commentsRemovedCode = removeCommentsFromCode(originalCode)
    startLine = 1
    endLine = len(commentsRemovedCode)
    allCodeBlocks.append(
        {"Start": startLine, "End": endLine, "Code": commentsRemovedCode})
    return allCodeBlocks


def methodLevelBlocks(originalCode):
    """
    input : originalCode
    output : blocks using method level
    """
    commentsRemovedCode = removeCommentsFromCode(originalCode)
    codeInSingleLine = "\n".join(commentsRemovedCode)

    output = GetFunctions.method_extractor(codeInSingleLine)

    allCodeBlocks = []
    for i in range(len(output[0])):
        allCodeBlocks.append(
            {"Start": output[0][i][0], "End": output[0][i][1], "Code": output[1][i].split('\n')})
        # print("==================================================")
        # print(output[1][i])

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
            if mode == DEFAULT:
                mode = MULTI_LINE_COMMENT if subString == "/*" else ONE_LINE_COMMENT if subString == "//" else STRING if c == '\"' else DEFAULT
            elif mode == STRING:
                mode = DEFAULT if c == '\"' else ESCAPE if c == '\\' else STRING
            elif mode == ESCAPE:
                mode = STRING
            elif mode == ONE_LINE_COMMENT:
                mode = DEFAULT if c == '\n' else ONE_LINE_COMMENT
                idx += 1
                continue
            elif mode == MULTI_LINE_COMMENT:
                mode = DEFAULT if subString == "*/" else MULTI_LINE_COMMENT
                idx += 2 if mode == DEFAULT else 1
                continue
            strippedLine += c if mode < 4 else ""
            idx += 1
        if len(strippedLine) > 0 and strippedLine[-1] == '\n':
            strippedLine = strippedLine[:-1]
        # strippedLine = re.sub('\t| +', ' ', strippedLine)
        strippedCode.append(strippedLine)
    return strippedCode
