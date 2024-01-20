//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=7)
//D=7
@7
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=8)
//D=8
@8
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
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
