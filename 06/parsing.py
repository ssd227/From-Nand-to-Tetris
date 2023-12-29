from util import *
from collections import namedtuple

Res1 = namedtuple('Res1', ['is_valid_instruction', 'have_label', 'label', 'instruction'])


########################### for pass1 ####################################
def parse_label(input_string):
    if input_string[0] == "(" and input_string[-1] == ")":
        if len(input_string[1:-1]) > 0:
            return True, input_string[1:-1]
    return False, None


def parse_comment_and_label(str_line):
    # 处理字符串
    str_line = replace_whitespace(str_line)  # 替换掉所有空字符
    str_line = remove_comment(str_line)  # 删掉注释部分

    # 空指令
    if str_line == "":
        return Res1(is_valid_instruction=False, have_label=False, label=None, instruction=None)

    # 非空指令
    else:
        ok, label = parse_label(str_line)  # parse label (XXX)
        if ok:
            return Res1(is_valid_instruction=False, have_label=True, label=label, instruction=None)
        else:
            # a、c指令
            return Res1(is_valid_instruction=True, have_label=False, label=None, instruction=str_line)


########################### for pass2 ####################################
def parse_A_instruction(raw_instr, st) -> int:
    ''' 
        解析str中的数字
        新变量需要自增
    '''
    suffix_s = raw_instr[1:]
    # 数字字符
    if suffix_s.isdigit():
        assert  0<= int(suffix_s) < int(2**16) , "@x, x最大取值为 0b 111 1111 1111 1111"
        return int(suffix_s)
    else:
        # 变量查表
        if suffix_s not in st:                  # TODO 会发生使用保留字符的问题。暂不处理
            st[suffix_s] = st['cvar_mem_id']    # TODO 这种实现方式也很丑
            st['cvar_mem_id'] = st[suffix_s]+1
        return st[suffix_s]

def parse_C_instruction(raw_instr):
    if '=' in raw_instr:
        dest, c23 = raw_instr.split('=')
    else:
        dest = 'NULL'
        c23 = raw_instr
    
    if ';' in c23: 
        comp, jump = c23.split(";")
    else:
        comp, jump = c23, 'NULL'
    return comp, dest, jump
