import sys
import os
import Config
def tokenizeAllFiles(listOfFiles):
    allFilesTokens = []
    for filePath in listOfFiles:
        fileTokens = tokenizeFileMethodLevel(filePath)        
        allFilesTokens.append({filePath : fileTokens})
    return allFilesTokens

def tokenizeFileMethodLevel(filePath) :
    #This function will take 1 filepath
    #And return all tokens made from that file
    #Uses method level

    allCodeBlocks = []
    bracketSeen = 0
    file = open(filePath, "r")
    lineNumber = 0
    startLine = -1
    endLine = -1
    currentCodeBlock = []
    inString = False
    inComment = False
    for line in file.readlines():
        lineNumber += 1
        # Get next line from file
        line = line.strip()
        # if line is empty
        # end of file is reached
        if line.startswith("//") :
            continue
        currentCodeBlock.append(line)
        if not line:
            continue
        currLineEffectiveStart = 0
        for idx in range(currLineEffectiveStart, len(line)):
            char = line[idx]
            if char == "\"":
                inString = inString ^ True
            elif inComment == False and inString == False and char =="/" and line[idx + 1] == "*":
                currentCodeBlock.pop()
                inComment = True
            elif inComment == True and inString == False and char == "*" and line[idx + 1] == "/":
                inComment = False
                currLineEffectiveStart = idx + 2
                currentCodeBlock.pop()
            elif inComment == False and inString == False and char == "/" and line[idx + 1] == "/" : 
                # Checks if current line contains any comment
                idx += 1
                print(idx, line)
                currentCodeBlock.pop()
                currentCodeBlock.append(line[currLineEffectiveStart : idx - 1])
                break
            if inString == False and inComment == False:
                if char == "{" :
                    bracketSeen += 1
                    if bracketSeen == 1:
                        startLine = lineNumber
                        currentCodeBlock = [line]
                elif char == "}" :
                    bracketSeen += -1
                    if bracketSeen == 0:
                        endLine = lineNumber
                        allCodeBlocks.append({"Start" : startLine, "End" : endLine, "Code" : currentCodeBlock})   
                        break
    file.close()
    return allCodeBlocks
