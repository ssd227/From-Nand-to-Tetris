from util import remove_comment, ParseRawLineError
from symbol_table import *


###### arithmetic ops ######
def parse_arithmetic(tokens):
    return Command(type=CommandType.C_ARITHMETIC, arg1=tokens[0], arg2=None)

###### push、pop ######
def parse_pop(tokens):
    segment = tokens[1]
    assert segment in PushPopArgs and tokens[2].isdigit(), \
        "[{}] : wrong args after push and pop".format(tokens)
    idx = int(tokens[2])
    return Command(type=CommandType.C_POP,
                    arg1=segment, arg2=idx)

def parser_push(tokens):
    segment = tokens[1]
    assert segment in PushPopArgs and tokens[2].isdigit(), \
        "[{}] : wrong args after push and pop".format(tokens)
    idx = int(tokens[2])
    return Command(type=CommandType.C_PUSH,
                    arg1=segment, arg2=idx)

###### control ######
def parse_label(tokens):
    return Command(type=CommandType.C_LABEL, arg1=tokens[1], arg2=None)

def parse_goto(tokens):
    return Command(type=CommandType.C_GOTO, arg1=tokens[1], arg2=None)

def parse_if_goto(tokens):
    return Command(type=CommandType.C_IF, arg1=tokens[1], arg2=None)

###### function ######
def parse_call(tokens):
    func_name = tokens[1]
    assert tokens[2].isdigit(), "[{}] : wrong args in call cmd".format(tokens)
    n_args = int(tokens[2])
    return Command(type=CommandType.C_CALL, arg1=func_name, arg2=n_args)

def parse_function(tokens):
    func_name = tokens[1]
    assert tokens[2].isdigit(), "[{}] : wrong args in function cmd".format(tokens)
    n_vars = int(tokens[2])
    return Command(type=CommandType.C_FUNCTION, arg1=func_name, arg2=n_vars)

def parse_return():
    return Command(type=CommandType.C_RETURN, arg1=None, arg2=None)

####### 主流程 #######
def parser(raw_lines):
    cmds = []
    for line in raw_lines:
        # 预处理-删掉注释
        clean_line = remove_comment(line).strip()
        
        if len(clean_line)>0:
            arr = clean_line.split() # 非空-有效命令
            # 1 word cmd
            if len(arr)==1:
                if arr[0] in ArithmeticOps:
                    cmds.append(parse_arithmetic(arr))
                elif ST.cmd_return == arr[0]:
                    cmds.append(parse_return())
            # 2 words cmd      
            elif len(arr)==2:
                if ST.cmd_label == arr[0]:
                    cmds.append(parse_label(arr))
                elif ST.cmd_goto == arr[0]:
                    cmds.append(parse_goto(arr))
                elif ST.cmd_if_goto == arr[0]:
                    cmds.append(parse_if_goto(arr))
            # 3 words cmd
            elif 3 == len(arr):
                if ST.cmd_push == arr[0]: 
                    cmds.append(parser_push(arr))
                elif ST.cmd_pop == arr[0]:
                    cmds.append(parse_pop(arr))
                elif ST.cmd_call == arr[0]:
                    cmds.append(parse_call(arr))
                elif ST.cmd_function == arr[0]:
                    cmds.append(parse_function(arr))
            else:
                raise ParseRawLineError(arr)
    return cmds