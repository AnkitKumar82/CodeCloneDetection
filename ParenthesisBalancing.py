import ControlElementsMapping


def checkForParenthesis(method_lines, lst_line, i):
    assert(len(method_lines) > 0)
    if '{' in lst_line:
        return method_lines

    else:
        k = i+1
        for next_line in method_lines[i+1:]:
            next_line = next_line.strip()
            #print(k, next_line)
            if(len(next_line) > 0):
                if '{' == next_line[0]:
                    return method_lines
                else:
                    #print(next_line, "++++++" + next_line[-1] + "+++++")
                    if ';' == next_line[-1]:
                        #print("========", next_line, method_lines[k])
                        method_lines[k] = method_lines[k] + " } "
                        method_lines[i] = method_lines[i] + " { "
                        return method_lines
            k += 1
    return method_lines


def parenthesisBalancer(method_lines):
    for i, line in enumerate(method_lines):
        # print(line)
        lst_line = line.split()

        for j, unit in enumerate(lst_line):
            if unit in ControlElementsMapping.keywords:
                #print(j, unit)
                method_lines = checkForParenthesis(
                    method_lines, lst_line, i)
                # print(method_lines)

    # for line in method_lines:
    #     print(line)
    return method_lines


# with open('examples/test.java', 'r') as f1:
#     method = f1.read()
#     new_method = parenthesisBalancer(method)

#     method_lines = method.split('\n')
#     #new_method_lines = new_method.split('\n')

#     print(new_method)
#     print("=========================================================")
#     # for line in new_method_lines:
#     #     print(line)
