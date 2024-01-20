//Command(type=<CommandType.C_FUNCTION: 7>, arg1='SimpleFunction.test', arg2=2)
//function's entry point
(SimpleFunction.test)
// init var[0]
//RAM[SP]=0
@SP
A=M
M=0
//SP++
@SP
M=M+1
// init var[1]
//RAM[SP]=0
@SP
A=M
M=0
//SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='local', arg2=0)
//D=base
@LCL
D=M
//A=base+idx
@0
A=D+A//RAM[SP]=RAM[base+idx]
D=M
@SP
A=M
M=D
//SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='local', arg2=1)
//D=base
@LCL
D=M
//A=base+idx
@1
A=D+A//RAM[SP]=RAM[base+idx]
D=M
@SP
A=M
M=D
//SP++
@SP
M=M+1
//Command(type=<CommandType.C_ARITHMETIC: 1>, arg1='add', arg2=None)
//op add|sub: +
//D=RAM[SP-1]
@SP
A=M-1
D=M
//SP--
@SP
M=M-1
//RAM[SP-2] + RAM[SP-1]
A=M-1
M=M+D
//Command(type=<CommandType.C_ARITHMETIC: 1>, arg1='not', arg2=None)
// logic ops not
//D=RAM[SP-1]
@SP
A=M-1
M=!M
//Command(type=<CommandType.C_PUSH: 2>, arg1='argument', arg2=0)
//D=base
@ARG
D=M
//A=base+idx
@0
A=D+A//RAM[SP]=RAM[base+idx]
D=M
@SP
A=M
M=D
//SP++
@SP
M=M+1
//Command(type=<CommandType.C_ARITHMETIC: 1>, arg1='add', arg2=None)
//op add|sub: +
//D=RAM[SP-1]
@SP
A=M-1
D=M
//SP--
@SP
M=M-1
//RAM[SP-2] + RAM[SP-1]
A=M-1
M=M+D
//Command(type=<CommandType.C_PUSH: 2>, arg1='argument', arg2=1)
//D=base
@ARG
D=M
//A=base+idx
@1
A=D+A//RAM[SP]=RAM[base+idx]
D=M
@SP
A=M
M=D
//SP++
@SP
M=M+1
//Command(type=<CommandType.C_ARITHMETIC: 1>, arg1='sub', arg2=None)
//op add|sub: -
//D=RAM[SP-1]
@SP
A=M-1
D=M
//SP--
@SP
M=M-1
//RAM[SP-2] - RAM[SP-1]
A=M-1
M=M-D
//Command(type=<CommandType.C_RETURN: 8>, arg1=None, arg2=None)
//1.replace return value. RAM[ARG]=RAM[SP-1]
//D=RAM[SP-1]
@SP
A=M-1
D=M
//RAM[ARG]=D
@ARG
A=M
M=D
//2.Recycle the memory used by the callee. SP=ARG+1
@ARG
D=M+1
@SP
M=D
//3.Reinstate the caller's segment pointers
// resotre R13
//R13 = *(endFrame - 5)
@5
D=A
@LCL
A=M-D
D=M
//R13=D
@R13
M=D
// resotre THAT
//THAT = *(endFrame - 1)
@1
D=A
@LCL
A=M-D
D=M
//THAT=D
@THAT
M=D
// resotre THIS
//THIS = *(endFrame - 2)
@2
D=A
@LCL
A=M-D
D=M
//THIS=D
@THIS
M=D
// resotre ARG
//ARG = *(endFrame - 3)
@3
D=A
@LCL
A=M-D
D=M
//ARG=D
@ARG
M=D
// resotre LCL
//LCL = *(endFrame - 4)
@4
D=A
@LCL
A=M-D
D=M
//LCL=D
@LCL
M=D
//4.Jump to the return address
@R13
A=M
0;JMP
