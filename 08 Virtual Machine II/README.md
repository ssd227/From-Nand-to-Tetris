## 项目8 VM Translator P2 说明

### 简述
    使用函数调用的代码风格，复杂的parse、code逻辑都单独封装成一个函数。
    没有对asm_codes的生成函数做过多的抽象与精简，便于直接阅读汇编代码。call、return两个命令稍复杂，使用了内部函数进行精简。

### 运行
    run1 - python vm_translator.py XXX.vm
    run2 - python vm_translator.py dir_path

    注意：
        由于多文件编译都包含Sys.vm, bootstrap代码会在vm_file_list大于2的时候自动添加
    
        对于单vm文件编译，请使用run1 (虽然使用dir_path也可以通过测试
        对于多vm文件编译，请使用run2 (输入文件夹路径即可

### 程序结构

    主程序:vm_translator.py
        解析vm命令：parsing.py
        生成汇编：coding.py
    
    ST: symbol_table.py
    辅助代码: util.py


### 测试相关问题

1、添加breakpoint

    为了方便VM虚拟机和CPU虚拟机执行指令同步，方便排查问题。
    每个待翻译的vm command前添加如下asm_codes，
    并在cpu模拟器中设置RAM[7777]为breakpoint。
        '@7777'
        'M=0'
        'M=1'
    由于RAM[7777]并不会被程序占用, 修改后的汇编代码逻辑不会改变。
    

2、bootstrap的写法的trick

    由于Sys.init没有返回的必要，与call相关的变量设置都可以置为0。
    伪代码：
        SP=256
        SP += 5 //retAddr、LCL、ARG、THIS、THAT 共五项设置
        goto functionName  

3、特别需要注意 call functionName 0

    由于
        nArgs=0,
        ARG = SP-5-nArgs = SP-5
    所以
        ARG指向的RAM位置 == retAddr保存的RAM位置
    又因为
        return默认replace一个返回值到ARG指向的RAM位置
    这会导致retAddr被错误的覆写。

    本项目中单独处理了nArgs=0的情况, SP++保留一个return回写的位置

