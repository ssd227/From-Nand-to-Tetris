from symbol_table import PreDefinedST
from parsing import *
from coding import *
import sys


def first_pass(incodes, st):
    '''
    # task1: 删掉注释行
    # task2: 删掉Label行(XXX), add (XXX, address) to ST
    '''
    
    codes = []
    label_cache = []

    for i in range(len(incodes)):
        raw_line = incodes[i]
        tmp_res = parse_comment_and_label(raw_line)
        if tmp_res.is_valid_instruction:
            codes.append(tmp_res.instruction)
            
            # add (XXX, address) to st
            if label_cache is not []:
                for lb in label_cache:
                    if lb in st:
                        raise RedefineError("redefine Label:[{}]".format(lb))
                    else:
                        st[lb] = len(codes) - 1
                        print("Address[{}]={}".format(lb, len(codes) - 1))
                label_cache = []  # reset label cache

        elif tmp_res.have_label:
            label_cache.append(tmp_res.label)

    return codes


def do_A_instruction(raw_instr, st):
    '''
        # (parse) @xxx 统一换成数字 
        # (code) 再把数字处理成标准01字符串 
    '''
    address_integer = parse_A_instruction(raw_instr, st)
    binary_str = code_A_instruction(address_integer)
    return binary_str


def do_C_instruction(raw_instr, st):
    '''
        # (parse) C指令解析为 comp, dest, jump 
        # (code) 对应字段查表映射到01表示 
    '''
    comp, dest, jump = parse_C_instruction(raw_instr)
    binary_str = code_C_instruction(comp, dest, jump, st) # TODO map 暂时全塞到st中，保留字段误写概率很高
    return binary_str


def second_pass(raw_instructions, st):
    # memory idx starts from 16 for new variable
    st['cvar_mem_id'] = 16
    codes = []
    
    for i in range(len(raw_instructions)):
        raw_instr = raw_instructions[i]
        
        # a_instruction
        if raw_instr[0] == '@':
            cur_code = do_A_instruction(raw_instr, st)
        else:
            cur_code = do_C_instruction(raw_instr, st)
        print('Instr[{}]: [{}] -> [{}]'.format(i, raw_instr, cur_code))
        codes.append(cur_code)
    return codes


def assembler(infile):
    # initilization
    ST = PreDefinedST  # Label symbol table (XXX)格式的数据，记录有效的机器码idx方便跳转
    with open(infile, 'r') as f:
        raw_codes = f.readlines()

    print("\n****first pass****")
    codes_1 = first_pass(raw_codes, ST)
    print("\nValid Instructions")
    for i in range(len(codes_1)):
        print("L{} : {}".format(i, codes_1[i]))

    print("\n****second pass****")
    codes_2 = second_pass(codes_1, ST)
    for i in range(len(codes_2)):
        print("L{} \t: {}".format(i, codes_2[i]))
        
    return codes_2


def main():
    # input Assembly Language
    asm_file_path = sys.argv[1]
    
    # 汇编过程
    codes = assembler(asm_file_path)
    
    # output Machine Language
    out_file_path = asm_file_path[:-3] + 'hack'
    codes = [line+"\n" for line in codes]
    with open(out_file_path, 'w') as f:
        f.writelines(codes)


if __name__ == '__main__':
    main()

'''
run command
    python .\assembler.py .\pong\Pong.asm
'''
