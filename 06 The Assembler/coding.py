''' 编码字段
    ops 查表编码为01字符串
'''
from util import OpsError

def code_A_instruction(integer):
    # 数字 to 01
    binary_str = format(integer, f'0{15}b') # TODO 暂不处理溢出问题
    return  '0' + binary_str


def code_C_instruction(comp, dest, jump, st):
    if comp in st['COMP']:
        binary_comp = st['COMP'][comp]
    else:
        raise OpsError('unsuppost comp: {}'.format(comp))
    
    if dest in st['DEST']:
        binary_dest = st['DEST'][dest]
    else:
        raise OpsError('unsuppost dest: {}'.format(dest))
    
    if jump in st['JUMP']:
        binary_jump = st['JUMP'][jump]
    else:
        raise OpsError('unsuppost jump: {}'.format(jump))
    
    return '111' + binary_comp + binary_dest + binary_jump