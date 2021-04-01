import re
import TokensMapping
def detectClone(codeBlocks, threshold = 1):
    for codeBlockId in codeBlocks:
        codeBlock = codeBlocks[codeBlockId]
        code = codeBlock['Code']  
        list_tokens = []
        for line in code:
            line = re.sub(r"(\".*?\"|\'.*?\')", " STRING_LITERAL ", line)
            line = re.sub(r"[+-]?((\d+(\.\d+)?)|(\.\d+))", " INTEGER_LITERAL ", line)
            list_line = re.split('(\W)', line)
            # Now considering : ; as well
            # lst_line = re.findall(r"[\w']+", line)
            # Now will remove delimiters

            for unit in list_line:
                unit = unit.strip()
                if unit in TokensMapping.delimiters:
                    continue
                elif unit in TokensMapping.mapping.keys():
                    list_tokens.append(TokensMapping.mapping[unit])
                else:
                    list_tokens.append(unit)
        
        dict_tokens = {}
        for token in list_tokens:
            if token in dict_tokens.keys():
                dict_tokens[token] = dict_tokens[token] + 1
            else:
                dict_tokens[token] = 1
        codeBlock.update({"Tokens": dict_tokens})

    for codeBlockId in codeBlocks:
        codeBlock = codeBlocks[codeBlockId]
        tokens = codeBlock["Tokens"]
        codeCloneIds = []
        for codeCandidateId in codeBlocks:
            if codeCandidateId == codeBlockId:
                continue
            sim = similarity(tokens, codeBlocks[codeCandidateId]["Tokens"])
            if sim >= threshold:
                codeCloneIds.append({"Similarity" : sim, "codeCandidateId" : codeCandidateId})
        codeBlock.update({"CodeClones" :codeCloneIds})
    return codeBlocks

def similarity(Tokens1, Tokens2):
    """
    input : two list of code
    output : similarity between two list of tokens(decimal between 0 and 1)
    """
    tokensIntersect = 0
    tokens1 = 0
    tokens2 = 0
    tokensUnion = 0
    Tokens1Keys = Tokens1.keys()
    Tokens2Keys = Tokens2.keys()
    for key in Tokens1Keys:
        if key in Tokens2Keys:
            tokensIntersect += min(Tokens1[key], Tokens2[key])
    for key in Tokens1Keys:
        tokens1 += Tokens1[key]
    for key in Tokens2Keys:
        tokens2 += Tokens2[key]
    return (tokensIntersect)/(tokens1 + tokens2 - tokensIntersect)

