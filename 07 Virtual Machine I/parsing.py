from util import remove_comment
from collections import namedtuple
from symbol_table import *


Command = namedtuple('Command', ['type', 'arg1', 'arg2'])


def parser(raw_lines):
    cmds = []
    
    for line in raw_lines:
        clean_line = remove_comment(line).strip() # 删掉注释
        
        if len(clean_line)>0: # 非空行命令
            arr = clean_line.split()
            if len(arr)==1:
                if arr[0] in ArithmeticOps:
                    cmd = Command(type=CommandType.C_ARITHMETIC, arg1=arr[0], arg2=None)
                    cmds.append(cmd)
                    
            elif len(arr)==3:
                if arr[0]==ST.push:
                    segment = arr[1]
                    assert segment in PushPopArgs and arr[2].isdigit(), \
                        "[{}] : wrong args after push and pop".format(arr)
                    idx = int(arr[2])
                    cmd = Command(type=CommandType.C_PUSH,
                                  arg1=segment, arg2=idx)
                    cmds.append(cmd)
                
                elif arr[0] == ST.pop:
                    segment = arr[1]
                    assert segment in PushPopArgs and arr[2].isdigit(), \
                        "[{}] : wrong args after push and pop".format(arr)
                    idx = int(arr[2])
                    cmd = Command(type=CommandType.C_POP,
                                  arg1=segment, arg2=idx)
                    cmds.append(cmd)
            
                    
    return cmds