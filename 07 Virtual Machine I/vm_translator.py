import os
import sys
from parsing import *
from coding import *

def vm_translator(infile):
    # initilization
    static_domain = os.path.basename(infile)[:-3] # 文件名构成的域, 用于static segment
    print("static domain",static_domain)

    with open(infile, 'r') as f:
        raw_lines = f.readlines()
    
    print("\n******** parser ********")
    cmds = parser(raw_lines)
    
    print("\nValid Commands")
    for i in range(len(cmds)):
        print("L{} : {}".format(i, cmds[i]))
    
    codes = coder(cmds, static_domain)
    
    return codes

def main():
    if len(sys.argv) == 1:
        print("输入文件名参数\n\tpython vm_translator.py filepath")
        return
    
    # input vm Language
    vm_file_path = sys.argv[1]
    
    
    # VM 翻译过程
    codes = vm_translator(vm_file_path)
    
    # output assembly language
    out_file_path = vm_file_path[:-2] + 'asm'
    codes = [line+"\n" for line in codes]
    with open(out_file_path, 'w') as f:
        f.writelines(codes)


if __name__ == '__main__':
    main()
    
    
# python .\vm_translator.py .\MemoryAccess\BasicTest\BasicTest.vm