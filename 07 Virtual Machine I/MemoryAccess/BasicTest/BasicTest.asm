//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=10)
//D=10
@10
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_POP: 3>, arg1='local', arg2=0)
//tmp_var: RAM[SP] = base+idx
//D=base
@LCL
D=M
//A=base+idx
@0
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
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=21)
//D=21
@21
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=22)
//D=22
@22
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_POP: 3>, arg1='argument', arg2=2)
//tmp_var: RAM[SP] = base+idx
//D=base
@ARG
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
//Command(type=<CommandType.C_POP: 3>, arg1='argument', arg2=1)
//tmp_var: RAM[SP] = base+idx
//D=base
@ARG
D=M
//A=base+idx
@1
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
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=36)
//D=36
@36
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_POP: 3>, arg1='this', arg2=6)
//tmp_var: RAM[SP] = base+idx
//D=base
@THIS
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
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=42)
//D=42
@42
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=45)
//D=45
@45
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_POP: 3>, arg1='that', arg2=5)
//tmp_var: RAM[SP] = base+idx
//D=base
@THAT
D=M
//A=base+idx
@5
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
//Command(type=<CommandType.C_POP: 3>, arg1='that', arg2=2)
//tmp_var: RAM[SP] = base+idx
//D=base
@THAT
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
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=510)
//D=510
@510
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_POP: 3>, arg1='temp', arg2=6)
//pop temp i ; pop RAM[5+i]
//SP--
@SP
M=M-1
//D=RAM[SP]
@SP
A=M
D=M
// RAM[5+i]=D
@R11
M=D
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
//Command(type=<CommandType.C_PUSH: 2>, arg1='that', arg2=5)
//D=base
@THAT
D=M
//A=base+idx
@5
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
//Command(type=<CommandType.C_PUSH: 2>, arg1='this', arg2=6)
//D=base
@THIS
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
//Command(type=<CommandType.C_PUSH: 2>, arg1='this', arg2=6)
//D=base
@THIS
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
//Command(type=<CommandType.C_PUSH: 2>, arg1='temp', arg2=6)
//push temp i = push RAM[5+i]
//D=RAM[5+i]
@R11
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
