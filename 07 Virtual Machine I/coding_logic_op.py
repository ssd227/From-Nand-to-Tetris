from symbol_table import *
from util import PushPopPointerError



def codeArithmetic(cmd):
    global CompareLabelCount
    global LogicLabelCount
    op = cmd.arg1
    
    if op == ST.op_add or op == ST.op_sub:
        op_str = "+" if op == ST.op_add else '-'
        # SP-1 -> y, SP-2 -> x, add 操作本身不压栈
        asm_codes = [
            '//op add|sub: {}'.format(op_str),
            
            '//D=RAM[SP-1]',
            '@SP',
            'A=M-1', # SP-1
            'D=M',
            
            '//SP--', # 已指向操作后的位置
            '@SP',
            'M=M-1',
            
            '//RAM[SP-2] {} RAM[SP-1]'.format(op_str),
            'A=M-1', # SP-2
            'M=M{}D'.format(op_str),
        ]
        
    elif op == ST.op_neg:
        asm_codes = [
            '//op neg',
            '//M = -RAM[SP-1]',
            '@SP',
            'A=M-1', # SP-1
            'M=-M',
        ]
    
    elif op == ST.op_eq or op == ST.op_gt or op == ST.op_lt :
        
        CompareLabelCount += 1
        cur_label = 'COMP_LABEL_{}'.format(CompareLabelCount) # 全局变量控制 lebel差异化 TODO 封装
        
        if op == ST.op_eq:
            jump_str = 'JEQ' 
        elif op == ST.op_gt:
            jump_str = 'JGT' 
        else:
            jump_str = 'JLT' 
        
        asm_codes = [
            '// compare ops eq|gt|lt',
            
            '//D=RAM[SP-1]',
            '@SP',
            'A=M-1',    # SP-1
            'D=M',      # y
            
            '//SP--', # 已指向操作后的位置
            '@SP',
            'M=M-1',
            
            '//RAM[SP-2] - RAM[SP-1]',
            'A=M-1', # SP-2
            'D=M-D',
            
            '// RAM[SP-2] = 1111 1111 1111 1111',
            'M=-1',
            
            # 判断jump 决定是否跳过 赋0操作
            '@{}'.format(cur_label), # jump to @label
            'D;{}'.format(jump_str), # (x-y) >|<|==0
                
            # 需要跳过的赋0操作            
            '//RAM[SP-2] = 0',
            '@SP',
            'A=M-1', # SP-2
            'M=0',
            
            '({})'.format(cur_label), # (label)
        ]
    
    # 两个if, 表达式非完全判定
    elif op == ST.op_and:
        
        LogicLabelCount += 1
        cur_label = 'LOGIC_LABEL_{}'.format(LogicLabelCount)
        
        asm_codes = [
            '// logic ops and',
            
            '//SP--',
            '@SP',
            'M=M-1',
            
            '//D=RAM[SP-2]',
            'A=M-1',    # SP-2
            'D=M',      # D=x
            
            # 预设bool值 0 
            '//RAM[SP-2]=0',
            'M=0', 
            
            # if x == 0: jump
            '@{}'.format(cur_label), # jump to @label
            'D;JEQ',    # x == 0
            
            # 取y值
            '// D = RAM[SP-1]',
            '@SP',
            'A=M',  # SP-1
            'D=M',  # D=y
            
            # if y ==0: jump
            '@{}'.format(cur_label), # jump to @label
            'D;JEQ',    # y == 0

            # 需跳过的赋1操作            
            '// RAM[SP-2] = 1111 1111 1111 1111',
            '@SP',
            'A=M-1', # SP-2
            'M=-1',
            
            '({})'.format(cur_label), # (label)
            ]

    elif op == ST.op_or:
        LogicLabelCount += 1
        cur_label = 'LOGIC_LABEL_{}'.format(LogicLabelCount)
        
        asm_codes = [
            '// logic ops or',
            
            '//SP--',
            '@SP',
            'M=M-1',
            
            '//D=RAM[SP-2]',
            'A=M-1',    # SP-2
            'D=M',      # D=x
            
            # 预设bool值 1
            '//RAM[SP-2]=1111 1111 1111 1111',
            'M=-1', 
            
            # if x==0: jump
            '@{}'.format(cur_label), # jump to @label
            'D;JNE',    # x!=0
            
            # 取y值
            '// D = RAM[SP-1]',
            '@SP',
            'A=M',  # SP-1
            'D=M',  # D=y
            
            # if y==0: jump
            '@{}'.format(cur_label), # jump to @label
            'D;JNE',    # y!=0

            # 需跳过的赋1操作            
            '// RAM[SP-2] = 0',
            '@SP',
            'A=M-1', # SP-2
            'M=0',
            
            '({})'.format(cur_label), # (label)
            ]
        
    # 直接判断是否是0, 然后跳转即可
    elif op == ST.op_not :
        LogicLabelCount += 1
        cur_label = 'LOGIC_LABEL_{}'.format(LogicLabelCount)
        
        asm_codes = [
            '// logic ops not',
            
            '//D=RAM[SP-1]',
            '@SP',
            'A=M-1',    # SP-1
            'D=M',      # y
            
            '// RAM[SP-1] = 1111 1111 1111 1111',
            '@SP',
            'A=M-1',    # SP-1
            'M=-1',

            # 判断jump 决定是否跳过 赋0操作
            '@{}'.format(cur_label),    # jump to @label
            'D;JEQ',
                
            # 需要跳过的赋0操作            
            '// RAM[SP-1] = 0',
            '@SP',
            'A=M-1', # SP-1
            'M=0',
            
            '({})'.format(cur_label),   # (label)
            ]

    else:
        asm_codes = [
            '// error! undefine op-[{}]'.format(op),
            ]

    return ['//{}'.format(cmd)]+asm_codes

def codePush(cmd, static_domain):
    cmd_type, segment, idx = cmd
      
    if segment == ST.constant:
        asm_codes = [
            
            '//D={}'.format(idx),
            '@{}'.format(idx),
            'D=A',
            
            '//RAM[SP]=D',
            '@SP',
            'A=M',
            'M=D',
            
            '// SP++',
            '@SP',
            'M=M+1',
        ]
        
    elif segment in {ST.local, ST.argument, ST.this, ST.that}:
        baseAddr = Segment2Addr[segment]
        asm_codes = [
            '//D=base',
            '@{}'.format(baseAddr),
            'D=M', # base
            
            '//A=base+idx',
            '@{}'.format(idx),
            'A=D+A' # base + idx

            '//RAM[SP]=RAM[base+idx]',
            'D=M',
            '@SP',
            'A=M',
            'M=D',

            '//SP++',
            '@SP',
            'M=M+1',
        ]
    
    elif segment == ST.static:
        AsmVar = '{}.{}'.format(static_domain, idx)
        asm_codes = [
            '//push static i = push XXX.i',

            '//RAM[SP]=RAM[XXX.i]',
            '@{}'.format(AsmVar),
            'D=M',
            '@SP',
            'A=M',
            'M=D',

            '//SP++',
            '@SP',
            'M=M+1',
        ]
        
    elif segment == ST.temp:
        assert 5 <= (5+idx) <= 12, 'overflow: temp默认占用[R5-R12]'
        asm_codes = [
            '//push temp i = push RAM[5+i]',

            '//D=RAM[5+i]',
            '@R{}'.format(5+idx),
            'D=M',

            '//RAM[SP]=D',
            '@SP',
            'A=M',
            'M=D',

            '//SP++',
            '@SP',
            'M=M+1',
        ]
    
    elif segment == ST.pointer:
        if idx ==0:
            addr = 'THIS'
        elif idx==1:
            addr = 'THAT'
        else:
            raise PushPopPointerError()
        asm_codes = [
            '// push THIS|THAT',
            
            '// D=RAM[THIS|THAT]',
            '@{}'.format(addr),
            'D=M',

            '//RAM[SP]=D',
            '@SP',
            'A=M',
            'M=D',

            '//SP++',
            '@SP',
            'M=M+1',
        ]

    return ['//{}'.format(cmd)]+asm_codes

def codePop(cmd, static_domain):
    cmd_type, segment, idx = cmd
    
    if segment in {ST.local, ST.argument, ST.this, ST.that}:
        baseAddr = Segment2Addr[segment]
        asm_codes = [
            '//tmp_var: RAM[SP] = base+idx',
            
            '//D=base',
            '@{}'.format(baseAddr),
            'D=M', # base
            
            '//A=base+idx',
            '@{}'.format(idx),
            'D=D+A' # base + idx

            '//save to RAM[SP]',
            '@SP',
            'A=M',      # RAM[SP]
            'M=D'

            '//SP--',
            '@SP',
            'M=M-1',

            '//RAM[base+idx]=RAM[SP]',
            '//D=RAM[SP-1]',
            '@SP',
            'A=M',
            'D=M',      # 'D=RAM[SP-1]'

            '//RAM[base+idx]=D',
            '@SP',
            'A=M+1',    # M = RAM[SP]
            'A=M',      # M = RAM[base+idx]
            'M=D',      # RAM[base+idx]=D
        ]

    elif segment == ST.static:
        AsmVar = '{}.{}'.format(static_domain, idx)
        asm_codes = [
            '//pop static i; pop XXX.i',
            
            '//SP--',
            '@SP',
            'M=M-1',

            '//RAM[XXX.i]=RAM[SP]',
            '@SP',
            'A=M',
            'D=M',
            '@{}'.format(AsmVar),
            'M=D',
        ]  
        
    elif segment == ST.temp:
        assert 5 <= (5+idx) <= 12, 'overflow: temp默认占用[R5-R12]'
        asm_codes = [
            '//pop temp i ; pop RAM[5+i]',
            
            '//SP--',
            '@SP',
            'M=M-1',

            '//D=RAM[SP]',
            '@SP',
            'A=M',
            'D=M',

            '// RAM[5+i]=D',
            '@R{}'.format(5+idx), 
            'M=D',  
        ]
    
    elif segment == ST.pointer:
        if idx ==0:
            addr = 'THIS'
        elif idx==1:
            addr = "THAT"
        else:
            raise PushPopPointerError()
        asm_codes = [
            '// pop THIS or THAT',

            '//SP--',
            '@SP',
            'M=M-1',
            
            '//Ram[THIS]=RAM[SP]',
            '@SP',
            'A=M',
            'D=M',
            '@{}'.format(addr),
            'M=D',
        ]
          
    return ['//{}'.format(cmd)]+asm_codes

def coder(commands, static_domain):
    codes = []
    for cmd in commands:
        if cmd.type == CommandType.C_ARITHMETIC:
            tmp_codes = codeArithmetic(cmd)
            codes += tmp_codes
        elif cmd.type == CommandType.C_PUSH:
            tmp_codes = codePush(cmd, static_domain)
            codes += tmp_codes
        elif cmd.type == CommandType.C_POP:
            tmp_codes = codePop(cmd, static_domain)
            codes += tmp_codes
    return codes