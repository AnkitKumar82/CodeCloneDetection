import os
import Config
import csv
def writeToFile(codeBlocks):
    mode = 'a' if os.path.exists(Config.outputPath) else 'w'
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
            writeToFile += tokensList + "\n"
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
    mode = 'a' if os.path.exists(Config.outputCSVPath) else 'w'
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
                csv_writer.writerow([currCodeBlockFileName, currCodeBlockStart, currCodeBlockEnd, codeCloneBlockFileName, codeCloneBlockStart, codeCloneBlockEnd])
        
        f.close()