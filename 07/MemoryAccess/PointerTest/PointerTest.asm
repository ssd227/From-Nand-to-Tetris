//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=3030)
//D=3030
@3030
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_POP: 3>, arg1='pointer', arg2=0)
// pop THIS or THAT
//SP--
@SP
M=M-1
//Ram[THIS]=RAM[SP]
@SP
A=M
D=M
@THIS
M=D
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=3040)
//D=3040
@3040
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_POP: 3>, arg1='pointer', arg2=1)
// pop THIS or THAT
//SP--
@SP
M=M-1
//Ram[THIS]=RAM[SP]
@SP
A=M
D=M
@THAT
M=D
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=32)
//D=32
@32
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_POP: 3>, arg1='this', arg2=2)
//tmp_var: RAM[SP] = base+idx
//D=base
@THIS
D=M
//A=base+idx
@2
D=D+A//save to RAM[SP]
@SP
A=M
M=D//SP--
@SP
M=M-1
//RAM[base+idx]=RAM[SP]
//D=RAM[SP-1]
@SP
A=M
D=M
//RAM[base+idx]=D
@SP
A=M+1
A=M
M=D
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=46)
//D=46
@46
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_POP: 3>, arg1='that', arg2=6)
//tmp_var: RAM[SP] = base+idx
//D=base
@THAT
D=M
//A=base+idx
@6
D=D+A//save to RAM[SP]
@SP
A=M
M=D//SP--
@SP
M=M-1
//RAM[base+idx]=RAM[SP]
//D=RAM[SP-1]
@SP
A=M
D=M
//RAM[base+idx]=D
@SP
A=M+1
A=M
M=D
//Command(type=<CommandType.C_PUSH: 2>, arg1='pointer', arg2=0)
// push THIS|THAT
// D=RAM[THIS|THAT]
@THIS
D=M
//RAM[SP]=D
@SP
A=M
M=D
//SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='pointer', arg2=1)
// push THIS|THAT
// D=RAM[THIS|THAT]
@THAT
D=M
//RAM[SP]=D
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
//Command(type=<CommandType.C_PUSH: 2>, arg1='this', arg2=2)
//D=base
@THIS
D=M
//A=base+idx
@2
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
//Command(type=<CommandType.C_PUSH: 2>, arg1='that', arg2=6)
//D=base
@THAT
D=M
//A=base+idx
@6
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
