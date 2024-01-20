from symbol_table import *
from util import PushPopPointerError
from parsing import parser

def codeArithmetic(cmd):
    global CompareLabelCount
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
        cur_label = 'COMP_LABEL_{}'.format(CompareLabelCount) # lebel_global_id
        
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
        asm_codes = [
            '// logic ops and',

            '//SP--',
            '@SP',
            'M=M-1',
            
            '//D=RAM[SP-1]',
            '@SP',
            'A=M',  # SP-1
            'D=M',  # D=y
            
            '//RAM[SP-2]=D & RAM[SP-2]',
            '@SP',
            'A=M-1', # SP-2
            'M=D&M',
            ]

    elif op == ST.op_or:
        asm_codes = [
            '// logic ops or',

            '//SP--',
            '@SP',
            'M=M-1',
            
            '//D=RAM[SP-1]',
            '@SP',
            'A=M',  # SP-1
            'D=M',  # D=y
            
            '//RAM[SP-2]=D|RAM[SP-2]',
            '@SP',
            'A=M-1', # SP-2
            'M=D|M',
            ]
        
    # 直接判断是否是0, 然后跳转即可
    elif op == ST.op_not :
        
        asm_codes = [
            '// logic ops not',
            
            '//D=RAM[SP-1]',
            '@SP',
            'A=M-1',    # SP-1
            'M=!M',      # y
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

def codeLabel(cmd):
    label = cmd.arg1
    asm_codes = [
        '({})'.format(label),
    ]
    return ['//{}'.format(cmd)]+asm_codes

def codeGoto(cmd):
    label = cmd.arg1
    asm_codes = [
        '//jump',
        '@{}'.format(label),
        '0;JMP',
        ]
    return ['//{}'.format(cmd)]+asm_codes
     
def codeIf(cmd):
    label = cmd.arg1
    asm_codes = [ 
        '//SP--',
        '@SP',
        'M=M-1',
        
        '//D=RAM[SP-1]',
        'A=M',
        'D=M', # RAM[SP-1]
        
        '//Jump on condition D',
        '@{}'.format(label),
        'D;JNE',
        ]
    return ['//{}'.format(cmd)]+asm_codes
        
def codeCall(cmd):
    global ReturnLabelCount
    cmd_type, functionName, nargs = cmd

    ReturnLabelCount += 1
    returnAddrLabel = functionName + '${}$Ret.{}'.format(nargs, ReturnLabelCount)
    
    def storeDAndIncrementStack():
        return ['@SP', # RAM[SP]=D
                'A=M',
                'M=D',
                '//SP++', #SP++
                '@SP',
                'M=M+1',
                ]
        
    def saveXXX(xxx):
        return ['//save {}'.format(xxx),
                '@{}'.format(xxx),
                'D=M',
                *storeDAndIncrementStack(),
                ]

    # ！！！如果nargs=0, 需要预留一个位置给返回。并把ARG指向该位置。
    # ！！！否则ARG指向SP-5-0的位置，会把return address的值给覆盖掉
    if nargs==0:
        asm_codes = [
            '//special process for nrags=0'
            '//SP++', #SP++
            '@SP',
            'M=M+1',
            
            '// save return address',
            '@{}'.format(returnAddrLabel),
            'D=A',
            *storeDAndIncrementStack(),

            *saveXXX('LCL'),
            *saveXXX('ARG'),
            *saveXXX('THIS'),
            *saveXXX('THAT'),

            '//Reposition ARG (ARG = SP-5-1)',
            '@SP',
            'D=M',
            '@{}'.format(5+1),
            'D=D-A',
            '@ARG',
            'M=D',
            
            '//Reposition LCL (LCL=SP)',
            '@SP',
            'D=M',
            '@LCL',
            'M=D',
            
            '//goto functionName',
            '@{}'.format(functionName),
            '0;JMP',
            
            '//retAddrLabel',
            '({})'.format(returnAddrLabel),
            
            # 测试集里居然不手动dump掉返回这，为了测试SP指针正确需要手动SP--
            # '//SP--',
            # '@SP',
            # 'M=M-1',
        ]
    else:
        asm_codes = [
            '// save return address',
            '@{}'.format(returnAddrLabel),
            'D=A',
            *storeDAndIncrementStack(),

            *saveXXX('LCL'),
            *saveXXX('ARG'),
            *saveXXX('THIS'),
            *saveXXX('THAT'),

            '//Reposition ARG (ARG = SP-5-nArgs)',
            '@SP',
            'D=M',
            '@{}'.format(5+nargs),
            'D=D-A',
            '@ARG',
            'M=D',
            
            '//Reposition LCL (LCL=SP)',
            '@SP',
            'D=M',
            '@LCL',
            'M=D',
            
            '//goto functionName',
            '@{}'.format(functionName),
            '0;JMP',
            
            '//retAddrLabel',
            '({})'.format(returnAddrLabel),
            
        ]
    return ['//{}'.format(cmd)]+asm_codes

def codeFunction(cmd):
    cmd_type, functionName, nvars = cmd
    
    def init_local_vars(n):
        asm_codes = []
        for i in range(n):
            asm_codes += [
                # push 0; sp++
                '// init var[{}]'.format(i),
                
                '//RAM[SP]=0',
                '@SP',
                'A=M',
                'M=0',
                
                '//SP++',
                '@SP',
                'M=M+1',
                ]
        return asm_codes

    asm_codes =[
        # function functionName nVars
        '//function\'s entry point',
        '({})'.format(functionName),
        
        # push nVars 0 values (initializes the local variables to 0)
        * init_local_vars(nvars),
        ]
    return ['//{}'.format(cmd)]+asm_codes

def codeReturn(cmd):
    
    def restoresXXX(idx):
        assert 1 <= idx <= 5
        idxmap=['THAT','THIS','ARG','LCL', 'R13'] # R13 tmp var for retaddr
        segmentName = idxmap[idx-1]
        
        return [
            '// resotre {}'.format(segmentName),
            '//{} = *(endFrame - {})'.format(segmentName, idx),
            
            '@{}'.format(idx),
            'D=A',
            '@LCL',
            'A=M-D',    # A=endFrame-idx
            'D=M',      # D=RAM[endFrame-idx]
            
            '//{}=D'.format(segmentName),
            '@{}'.format(segmentName),
            'M=D',
            ]
   
    asm_codes =[
        '//1.replace return value. RAM[ARG]=RAM[SP-1]',
        '//D=RAM[SP-1]',
        '@SP',
        'A=M-1',
        'D=M',
        '//RAM[ARG]=D',
        '@ARG',
        'A=M',
        'M=D',
        
        '//2.Recycle the memory used by the callee. SP=ARG+1',
        '@ARG',
        'D=M+1',
        '@SP',
        'M=D',
        
        '//3.Reinstate the caller\'s segment pointers',
        # retAddr(R13) = *(endFrame – 5)
        *restoresXXX(5),
        # THAT = *(endFrame – 1)
        *restoresXXX(1),
        # THIS = *(endFrame – 2)
        *restoresXXX(2),
        # ARG = *(endFrame – 3)
        *restoresXXX(3),
        # LCL = *(endFrame – 4)
        *restoresXXX(4),
        
        '//4.Jump to the return address',
        '@R13',
        'A=M', # rerAddr           
        '0;JMP',
        ]
    return ['//{}'.format(cmd)]+asm_codes

def bootstrap_code():
    functionName = 'Sys.init'
    
    asm_codes =[
        '//SP=256',
        '@256',
        'D=A',
        '@SP',
        'M=D',

        '//call Sys.init',
        # '// save return address',
        # *saveXXX('LCL'),
        # *saveXXX('ARG'),
        # *saveXXX('THIS'),
        # *saveXXX('THAT'),
        # '//Reposition ARG (ARG = SP-5-1)',
        
        # trick: set all zero
        '@5',
        'D=A',
        '@SP',
        'M=M+D'
        
        '//goto functionName',
        '@{}'.format(functionName),
        '0;JMP',
        
    ]
    return ['//bootstrap_code',] + asm_codes

def breakPoint():
    return [
        '@7777',
        'M=0',
        'M=1',
        ]

def coder(commands, static_domain):
    codes = []
    for cmd in commands:
        if cmd.type == CommandType.C_ARITHMETIC:
            tmp_codes = codeArithmetic(cmd)

        elif cmd.type == CommandType.C_PUSH:
            tmp_codes = codePush(cmd, static_domain)
           
        elif cmd.type == CommandType.C_POP:
            tmp_codes = codePop(cmd, static_domain)
            
        elif cmd.type == CommandType.C_LABEL:
            tmp_codes = codeLabel(cmd)
        
        elif cmd.type == CommandType.C_GOTO:
            tmp_codes = codeGoto(cmd)
        
        elif cmd.type == CommandType.C_IF:
            tmp_codes = codeIf(cmd)
        
        elif cmd.type == CommandType.C_CALL:
            tmp_codes = codeCall(cmd)
        
        elif cmd.type == CommandType.C_FUNCTION:
            tmp_codes = codeFunction(cmd)
            
        elif cmd.type == CommandType.C_RETURN:
            tmp_codes = codeReturn(cmd)
        
        # 是否添加断点辅助排查
        if False:
            codes += breakPoint()
        
        codes += tmp_codes
            
    return codes