//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=111)
//D=111
@111
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=333)
//D=333
@333
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=888)
//D=888
@888
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_POP: 3>, arg1='static', arg2=8)
//pop static i; pop XXX.i
//SP--
@SP
M=M-1
//RAM[XXX.i]=RAM[SP]
@SP
A=M
D=M
@StaticTest.8
M=D
//Command(type=<CommandType.C_POP: 3>, arg1='static', arg2=3)
//pop static i; pop XXX.i
//SP--
@SP
M=M-1
//RAM[XXX.i]=RAM[SP]
@SP
A=M
D=M
@StaticTest.3
M=D
//Command(type=<CommandType.C_POP: 3>, arg1='static', arg2=1)
//pop static i; pop XXX.i
//SP--
@SP
M=M-1
//RAM[XXX.i]=RAM[SP]
@SP
A=M
D=M
@StaticTest.1
M=D
//Command(type=<CommandType.C_PUSH: 2>, arg1='static', arg2=3)
//push static i = push XXX.i
//RAM[SP]=RAM[XXX.i]
@StaticTest.3
D=M
@SP
A=M
M=D
//SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='static', arg2=1)
//push static i = push XXX.i
//RAM[SP]=RAM[XXX.i]
@StaticTest.1
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
//Command(type=<CommandType.C_PUSH: 2>, arg1='static', arg2=8)
//push static i = push XXX.i
//RAM[SP]=RAM[XXX.i]
@StaticTest.8
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
