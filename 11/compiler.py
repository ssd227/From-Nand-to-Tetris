import os
import sys
from utils import list_dir_jack_files
from tokenizer import Tokenizer
from iparser import Parser
from generator import Generator


# 输出Xxx.vm文件
def persistence(infile, vmcodes):
    out_path = infile[:-4]+'vm'

    vmcodes = [line+"\n" for line in vmcodes] # 加入换行
    with open(out_path, 'w') as f:
        f.writelines(vmcodes)
    print('write[{}] done'.format(out_path))


def syntax_analyzer(infile):
    tokenizer = Tokenizer(infile)
    tokenizer.persistence()
    
    parser = Parser(infile, tokenizer)
    parser.persistence()
    
    return tokenizer, parser

def compiler(infile):
    print("******** syntax analyzer ********")
    tokenizer, parser =  syntax_analyzer(infile)

    print("******** code generate ********")
    generator = Generator(parse_tree_root=parser.root)
    vmcodes =  generator.codes

    # output vm files
    persistence(infile, vmcodes)    

def prepare_input_files(in_path):
    # in_path is (single vm file) or (dir with vms)
    if in_path[-5:]=='.jack':
        jacks = [in_path]
    else:
        jacks = list_dir_jack_files(in_path)
    return jacks

def main():
    if len(sys.argv) == 1:
        print("输入参数\n\tpython compiler.py XXX_dir_path")
        return

    input_path = sys.argv[1]
    # 0、input path预处理
    # in_path is dir_path with files(.jack)
    jack_file_list =  prepare_input_files(input_path)
    print('input jacks: {}\n'.format(jack_file_list))
    assert len(jack_file_list) > 0, "输入路径下没有.jack文件"
    
    # 1、编译
    for vm_file in jack_file_list:
        compiler(vm_file)

if __name__ == '__main__':
    main()