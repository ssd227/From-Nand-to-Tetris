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
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=0)
//D=0
@0
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_POP: 3>, arg1='that', arg2=0)
//tmp_var: RAM[SP] = base+idx
//D=base
@THAT
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
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=1)
//D=1
@1
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_POP: 3>, arg1='that', arg2=1)
//tmp_var: RAM[SP] = base+idx
//D=base
@THAT
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
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=2)
//D=2
@2
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
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
//Command(type=<CommandType.C_POP: 3>, arg1='argument', arg2=0)
//tmp_var: RAM[SP] = base+idx
//D=base
@ARG
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
//Command(type=<CommandType.C_LABEL: 4>, arg1='LOOP', arg2=None)
(LOOP)
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
//Command(type=<CommandType.C_IF: 6>, arg1='COMPUTE_ELEMENT', arg2=None)
//SP--
@SP
M=M-1
//D=RAM[SP-1]
A=M
D=M
//Jump on condition D
@COMPUTE_ELEMENT
D;JNE
//Command(type=<CommandType.C_GOTO: 5>, arg1='END', arg2=None)
//jump
@END
0;JMP
//Command(type=<CommandType.C_LABEL: 4>, arg1='COMPUTE_ELEMENT', arg2=None)
(COMPUTE_ELEMENT)
//Command(type=<CommandType.C_PUSH: 2>, arg1='that', arg2=0)
//D=base
@THAT
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
//Command(type=<CommandType.C_PUSH: 2>, arg1='that', arg2=1)
//D=base
@THAT
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
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=1)
//D=1
@1
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
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=1)
//D=1
@1
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
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
//Command(type=<CommandType.C_POP: 3>, arg1='argument', arg2=0)
//tmp_var: RAM[SP] = base+idx
//D=base
@ARG
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
//Command(type=<CommandType.C_GOTO: 5>, arg1='LOOP', arg2=None)
//jump
@LOOP
0;JMP
//Command(type=<CommandType.C_LABEL: 4>, arg1='END', arg2=None)
(END)
