import os
import Config
import csv
def writeToFile(codeBlocks):
    mode = 'w'
    with open(Config.outputPath, mode) as f:
        for codeBlockId in codeBlocks:
            codeBlock = codeBlocks[codeBlockId]
            if len(codeBlock["CodeClones"]) == 0:
                continue
            writeToFile = ""
            writeToFile += "Block id : " + codeBlockId
            writeToFile += "\nFile path : " + codeBlock["FileInfo"]
            writeToFile += "\nStart : " + str(codeBlock["Start"]) + " End : " + str(codeBlock["End"])
            tokensList = "\nTokensList : "
            for tokenVar in codeBlock["Tokens"]:
                tokensList += tokenVar + ":" + str(codeBlock["Tokens"][tokenVar]) + ","
            # variablesList = "\nVariables List : "
            # for variable in codeBlock["Variables_Scope"]:
            #     variablesList +=  str(variable[0]) + ":" + str(variable[1]) + "\n"

            # methodList = "\nMethod List: "
            # for tokenVar in codeBlock["Method_Calls_Scope"]:
            #     methodList += str(tokenVar[0]) + ":" + str(tokenVar[1]) + "\n"

            writeToFile += tokensList + "\n"
            # writeToFile += variablesList + "\n"
            # writeToFile += methodList + "\n"
            if Config.outputLevel < 2:
                writeToFile += "\nCode : \n"+ "\n".join(codeBlock["Code"])
            writeToFile += "\n" + "="*150 + "\n"
            writeToFile += "\nCodeClones : \n"
            for codeCloneBlockData in codeBlock["CodeClones"]:
                codeCloneBlockId = codeCloneBlockData["codeCandidateId"]
                codeCloneBlock = codeBlocks[codeCloneBlockId]
                codeCloneSimilarity = codeCloneBlockData["Similarity"]
                writeToFile += "Block id : " + codeCloneBlockId
                writeToFile += "\nSimilarity Tokens : " + str(codeCloneSimilarity[0])
                writeToFile += "\nSimilarity Variable Flow : " + str(codeCloneSimilarity[1])
                writeToFile += "\nSimilarity Methods Call Flow : " + str(codeCloneSimilarity[2])

                writeToFile += "\nFile path : " + codeCloneBlock["FileInfo"]
                writeToFile += "\nStart : " + str(codeCloneBlock["Start"]) + " End : " + str(codeCloneBlock["End"])
                if Config.outputLevel < 1:
                    writeToFile += "\nCode : \n"+ "\n".join(codeCloneBlock["Code"])
                writeToFile += "\n" + "-"*150 + "\n"
            writeToFile += "\n" + "#"*150 + "\n\n"
            f.write(writeToFile)
        f.close()
def writeToCSV(codeBlocks):
    mode = 'w'
    with open(Config.outputCSVPath, mode, newline='') as f:
        csv_writer = csv.writer(f)

        for codeBlockId in codeBlocks:
            codeBlock = codeBlocks[codeBlockId]
            if len(codeBlock["CodeClones"]) == 0:
                continue
            currCodeBlockFileName = codeBlock["FileInfo"].split("\\")[-1]
            currCodeBlockStart = str(codeBlock["Start"])
            currCodeBlockEnd = str(codeBlock["End"])
            for codeCloneBlockData in codeBlock["CodeClones"]:
                codeCloneBlockId = codeCloneBlockData["codeCandidateId"]
                codeCloneBlock = codeBlocks[codeCloneBlockId]
                codeCloneBlockFileName = codeCloneBlock["FileInfo"].split("\\")[-1]
                codeCloneBlockStart = str(codeCloneBlock["Start"])
                codeCloneBlockEnd = str(codeCloneBlock["End"])

                # codeCloneSimilarity = codeCloneBlockData["Similarity"]
                # simi = str(codeCloneSimilarity[0])
                # simi2 = str(codeCloneSimilarity[1])
                # simi3 = str(codeCloneSimilarity[2])
                csv_writer.writerow([currCodeBlockFileName, currCodeBlockStart, currCodeBlockEnd, codeCloneBlockFileName, codeCloneBlockStart, codeCloneBlockEnd])
        
        f.close()