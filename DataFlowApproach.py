import Mapping
import ControlElementsMapping
import ParenthesisBalancing
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def stringMatching(str1, str2):
    # str1, str2 = "", ""

    # for ele in num1:
    #     str1 += ele
    # for ele in num2:
    #     str2 += ele

    similarity = fuzz.ratio(str1, str2)
    print(str1, str2, similarity)
    return similarity


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


def getSimilarity(m1_v_scope=[], m1_mc_scope=[], m2_v_scope=[], m2_mc_scope=[]):
    print(m1_v_scope, m2_v_scope)
    threshold = 0.7
    clone_count_variables, total_count_variables = 0, max(
        len(m1_v_scope), len(m2_v_scope))
    clone_count_method_calls, total_count_method_calls = 0, max(
        len(m1_mc_scope), len(m2_mc_scope))

    comparison_len_variables = min(len(m1_v_scope), len(m2_v_scope))
    comparison_len_method_calls = min(len(m1_mc_scope), len(m2_mc_scope))

    print(comparison_len_variables, comparison_len_method_calls)

    for i in range(comparison_len_variables):
        v_len1 = len(m1_v_scope[i][1].split())
        v_len2 = len(m2_v_scope[i][1].split())

        if min(v_len1, v_len2) / max(v_len1, v_len2) >= threshold:
            # v1_scope_str, v2_scope_str = [], []

            # for scope in m1_v_scope[i][1]:
            #     v1_scope_list.append(str(scope[0]) + str(scope[1]))

            # for scope in m2_v_scope[i][1]:
            #     v2_scope_list.append(str(scope[0]) + str(scope[1]))

            # lcs_length = lcs(v1_scope_list, v2_scope_list,
            #                  len(v1_scope_list), len(v2_scope_list))
            # # [["num1", [[1, "I"], [2, "S"]]], ["num2", [[1]]]]
            # similarity = lcs_length/max(v_len1, v_len2)

            print(m1_v_scope[i][0], m2_v_scope[i][0])
            similarity = stringMatching(m1_v_scope[i][1], m2_v_scope[i][1])

            if(similarity >= threshold):
                clone_count_variables += 1

    for i in range(comparison_len_method_calls):
        mc_len1 = len(m1_mc_scope[i][1].split())
        mc_len2 = len(m2_mc_scope[i][1].split())

        if min(mc_len1, mc_len2) / max(mc_len1, mc_len2) >= threshold:
            # mc1_scope_list, mc2_scope_list = [], []

            # for scope in m1_mc_scope[i][1]:
            #     mc1_scope_list.append(str(scope[0]) + str(scope[1]))

            # for scope in m2_mc_scope[i][1]:
            #     mc2_scope_list.append(str(scope[0]) + str(scope[1]))

            # lcs_length = lcs(mc1_scope_list, mc2_scope_list,
            #                  len(mc1_scope_list), len(mc2_scope_list))

            # similarity = lcs_length/max(mc_len1, mc_len2)

            print(m1_mc_scope[i][0], m2_mc_scope[i][0])
            similarity = stringMatching(m1_mc_scope[i][1], m2_mc_scope[i][1])

            if similarity >= threshold:
                clone_count_method_calls += 1

    print(clone_count_variables / total_count_variables,
          clone_count_method_calls / total_count_method_calls)

    return clone_count_variables / total_count_variables, clone_count_method_calls / total_count_method_calls


def dataFlowGenerator(method_lines, identifiers, method_calls):
    identifier_scope = [[] for _ in range(len(identifiers))]
    method_calls_scope = [[] for _ in range(len(method_calls))]

    print(identifiers)
    print(method_calls)

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
                    index = identifiers.index(identifier)

                    if(len(identifier_scope[index]) == 0):
                        identifier_scope[index].append(identifier)
                        identifier_scope[index].append(str(level) + scope)

                    else:
                        identifier_scope[index][1] = identifier_scope[index][1] + \
                            " " + str(level) + scope

            for method_call in method_calls:
                if(method_call == unit):
                    index = method_calls.index(method_call)

                    if(len(method_calls_scope[index]) == 0):
                        method_calls_scope[index].append(method_call)
                        method_calls_scope[index].append(str(level) + scope)

                    else:
                        method_calls_scope[index][1] = method_calls_scope[index][1] + " " + str(
                            level) + scope

    return identifier_scope, method_calls_scope
