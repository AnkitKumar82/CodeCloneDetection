import os
def writeToFile(codeBlocks, outputPath, outputLevel):
    import os
    mode = 'a' if os.path.exists(outputPath) else 'w'
    with open(outputPath, mode) as f:
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
            if outputLevel < 2:
                writeToFile += "\nCode : \n"+ "\n".join(codeBlock["Code"])
            writeToFile += "\n" + "="*150 + "\n"
            writeToFile += "\nCodeClones : \n"
            for codeCloneBlockData in codeBlock["CodeClones"]:
                codeCloneBlockId = codeCloneBlockData["codeCandidateId"]
                codeCloneBlock = codeBlocks[codeCloneBlockId]
                codeCloneSimilarity = codeCloneBlockData["Similarity"]
                writeToFile += "Block id : " + codeCloneBlockId
                writeToFile += "\nSimilarity : " + str(codeCloneSimilarity)
                writeToFile += "\nFile path : " + codeCloneBlock["FileInfo"]
                writeToFile += "\nStart : " + str(codeCloneBlock["Start"]) + " End : " + str(codeCloneBlock["End"])
                if outputLevel < 1:
                    writeToFile += "\nCode : \n"+ "\n".join(codeCloneBlock["Code"])
                writeToFile += "\n" + "-"*150 + "\n"
            writeToFile += "\n" + "#"*150 + "\n\n"
            f.write(writeToFile)
        f.close()