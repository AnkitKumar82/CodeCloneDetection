import Mapping
import ControlElementsMapping
import ParenthesisBalancing
import re
threshold = 0.8


def getSimilarity(v1_scope=[], mc1_scope=[], v2_scope=[], mc2_scope=[]):
    return 1


def dataFlowGenerator(method_lines, identifiers, method_calls):
    identifier_scope = {}
    method_calls_scope = {}
    scope_stack, parenthesis_stack = [], []
    level = 0
    scope = "global"

    method_lines = ParenthesisBalancing.parenthesisBalancer(method_lines)

    # print(Mapping.delimiters)
    new_delimeters = Mapping.delimiters + ['.']
    # print(new_delimeters)
    for line in method_lines:
        line = re.sub(r"(\".*?\"|\'.*?\')", " STRING_LITERAL ", line)
        regexPattern = '|'.join(map(re.escape, new_delimeters))
        lst_line = re.sub('(?<=\W|\w)(' + regexPattern + ')',
                          r' \1 ', line).split()
        lst_line = [unit.strip() for unit in lst_line if unit.strip() != ""]

        for unit in lst_line:
            unit = unit.strip()
            unit = re.sub(r"^[+-]?((\d+(\.\d+)?)|(\.\d+))$",
                          "INTEGER_LITERAL", unit)

            for keyword in ControlElementsMapping.keywords:
                if(unit == keyword):
                    scope = ControlElementsMapping.cf_mapping[keyword]
                    break

            if unit == '{':
                scope_stack.append(scope)
                parenthesis_stack.append('{')
                level += 1

            if unit == '}':
                scope_stack.pop()
                if(len(scope_stack) > 0):
                    scope = scope_stack[-1]
                parenthesis_stack.pop()
                level -= 1

            for identifier in identifiers:
                if(identifier == unit):
                    if identifier in identifier_scope.keys():
                        identifier_scope[identifier].append([level, scope])

                    else:
                        identifier_scope[identifier] = [[level, scope]]

            for method_call in method_calls:
                if(method_call == unit):
                    if method_call in method_calls_scope.keys():
                        method_calls_scope[method_call].append([level, scope])

                    else:
                        method_calls_scope[method_call] = [[level, scope]]

    return identifier_scope, method_calls_scope


def lcs(num1, num2, m, n):
    dp = []
    for _ in range(m+1):
        dp.append([])
        for __ in range(n+1):
            dp[-1].append(0)

    for i in range(m+1):
        for j in range(n+1):
            if(i == 0 or j == 0):
                dp[i][j] = 0

            elif(num1[i-1] == num2[j-1]):
                dp[i][j] = dp[i-1][j-1] + 1

            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]


# with open('examples/BubbleSortV1.java', 'r') as f1:
#     method1 = f1.read()

# with open('examples/BubbleSortV2.java', 'r') as f2:
#     method2 = f2.read()

# identifier_scope_m1 = dataFlowGenerator(method1, ["num", "flag", "temp"])

# identifier_scope_m2 = dataFlowGenerator(method2, ["num", "flag", "temp"])

# num1, num2 = [], []
# for value in identifier_scope_m1['num']:
#     num1.append(str(value[0]) + value[1])

# for value in identifier_scope_m2['num']:
#     num2.append(str(value[0]) + value[1])

# print(num1)
# print(num2)
# # Three variables : num, flag, temp

# lcs_length = lcs(num1, num2, len(num1), len(num2))

# similarity = lcs_length/max(len(num1), len(num2))

# if(similarity >= threshold):
#     print("Clones")
# else:
#     print("Not Clones")
