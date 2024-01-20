import os
import sys
import glob
from parsing import *
from coding import *

'''

different from part I
    TODO 输入需要支持整个dir下的所有vm, 输出为一个可以执行的asm

'''

def vm_translator(infile):
    # initilization
    static_domain = os.path.basename(infile)[:-3] # 文件名构成的域, 用于static segment
    print("\nstatic domain: ",static_domain)

    with open(infile, 'r') as f:
        raw_lines = f.readlines()
    
    print("******** parser ********")
    cmds = parser(raw_lines)
    
    print("Valid Commands")
    for i in range(len(cmds)):
        print("L{} : {}".format(i, cmds[i]))
    
    codes = coder(cmds, static_domain)
    return codes


def get_dir_vm_files(dirpath):
    files = []
    base = dirpath + '*.vm'
    for f in glob.glob(base):
        files.append(f)
    return files

def prepare_input_files(in_path):
    # in_path is (single vm file) or (dir with vms)
    if in_path[-3:]=='.vm':
        vms = [in_path]
        out_path = in_path[:-2] + 'asm'
    else:
        vms = get_dir_vm_files(in_path)
        last_folder = os.path.basename(os.path.normpath(in_path))
        out_path = os.path.join( in_path, last_folder+'.asm')
    
    return vms, out_path

def main():
    if len(sys.argv) == 1:
        print("输入文件名参数\n\tpython vm_translator.py filepath")
        return
    input_path = sys.argv[1]
    # 0、input path预处理
    vm_file_list, out_file_path = prepare_input_files(input_path)
    print('input vms: {}\noutput asm: {}'.format(vm_file_list, out_file_path))
    assert len(vm_file_list)>0, "输入路径下，没有.vm文件"
    
    # 1、VM 翻译过程
    codes = [] 
    if len(vm_file_list) > 1:
        codes += bootstrap_code() # 系统引导asm code, 默认含有Sys.vm

    for vm_file in vm_file_list:    
        codes += vm_translator(vm_file) # 各文件asm code
    
    # 2、output assembly language
    codes = [line+"\n" for line in codes]
    with open(out_file_path, 'w') as f:
        f.writelines(codes)


if __name__ == '__main__':
    main()

# python .\vm_translator.py .\MemoryAccess\BasicTest\BasicTest.vm