//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=17)
//D=17
@17
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=17)
//D=17
@17
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_ARITHMETIC: 1>, arg1='eq', arg2=None)
// compare ops eq|gt|lt
//D=RAM[SP-1]
@SP
A=M-1
D=M
//SP--
@SP
M=M-1
//RAM[SP-2] - RAM[SP-1]
A=M-1
D=M-D
// RAM[SP-2] = 1111 1111 1111 1111
M=-1
@COMP_LABEL_1
D;JEQ
//RAM[SP-2] = 0
@SP
A=M-1
M=0
(COMP_LABEL_1)
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=17)
//D=17
@17
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=16)
//D=16
@16
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_ARITHMETIC: 1>, arg1='eq', arg2=None)
// compare ops eq|gt|lt
//D=RAM[SP-1]
@SP
A=M-1
D=M
//SP--
@SP
M=M-1
//RAM[SP-2] - RAM[SP-1]
A=M-1
D=M-D
// RAM[SP-2] = 1111 1111 1111 1111
M=-1
@COMP_LABEL_2
D;JEQ
//RAM[SP-2] = 0
@SP
A=M-1
M=0
(COMP_LABEL_2)
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=16)
//D=16
@16
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=17)
//D=17
@17
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_ARITHMETIC: 1>, arg1='eq', arg2=None)
// compare ops eq|gt|lt
//D=RAM[SP-1]
@SP
A=M-1
D=M
//SP--
@SP
M=M-1
//RAM[SP-2] - RAM[SP-1]
A=M-1
D=M-D
// RAM[SP-2] = 1111 1111 1111 1111
M=-1
@COMP_LABEL_3
D;JEQ
//RAM[SP-2] = 0
@SP
A=M-1
M=0
(COMP_LABEL_3)
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=892)
//D=892
@892
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=891)
//D=891
@891
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_ARITHMETIC: 1>, arg1='lt', arg2=None)
// compare ops eq|gt|lt
//D=RAM[SP-1]
@SP
A=M-1
D=M
//SP--
@SP
M=M-1
//RAM[SP-2] - RAM[SP-1]
A=M-1
D=M-D
// RAM[SP-2] = 1111 1111 1111 1111
M=-1
@COMP_LABEL_4
D;JLT
//RAM[SP-2] = 0
@SP
A=M-1
M=0
(COMP_LABEL_4)
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=891)
//D=891
@891
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=892)
//D=892
@892
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_ARITHMETIC: 1>, arg1='lt', arg2=None)
// compare ops eq|gt|lt
//D=RAM[SP-1]
@SP
A=M-1
D=M
//SP--
@SP
M=M-1
//RAM[SP-2] - RAM[SP-1]
A=M-1
D=M-D
// RAM[SP-2] = 1111 1111 1111 1111
M=-1
@COMP_LABEL_5
D;JLT
//RAM[SP-2] = 0
@SP
A=M-1
M=0
(COMP_LABEL_5)
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=891)
//D=891
@891
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=891)
//D=891
@891
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_ARITHMETIC: 1>, arg1='lt', arg2=None)
// compare ops eq|gt|lt
//D=RAM[SP-1]
@SP
A=M-1
D=M
//SP--
@SP
M=M-1
//RAM[SP-2] - RAM[SP-1]
A=M-1
D=M-D
// RAM[SP-2] = 1111 1111 1111 1111
M=-1
@COMP_LABEL_6
D;JLT
//RAM[SP-2] = 0
@SP
A=M-1
M=0
(COMP_LABEL_6)
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=32767)
//D=32767
@32767
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=32766)
//D=32766
@32766
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_ARITHMETIC: 1>, arg1='gt', arg2=None)
// compare ops eq|gt|lt
//D=RAM[SP-1]
@SP
A=M-1
D=M
//SP--
@SP
M=M-1
//RAM[SP-2] - RAM[SP-1]
A=M-1
D=M-D
// RAM[SP-2] = 1111 1111 1111 1111
M=-1
@COMP_LABEL_7
D;JGT
//RAM[SP-2] = 0
@SP
A=M-1
M=0
(COMP_LABEL_7)
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=32766)
//D=32766
@32766
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=32767)
//D=32767
@32767
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_ARITHMETIC: 1>, arg1='gt', arg2=None)
// compare ops eq|gt|lt
//D=RAM[SP-1]
@SP
A=M-1
D=M
//SP--
@SP
M=M-1
//RAM[SP-2] - RAM[SP-1]
A=M-1
D=M-D
// RAM[SP-2] = 1111 1111 1111 1111
M=-1
@COMP_LABEL_8
D;JGT
//RAM[SP-2] = 0
@SP
A=M-1
M=0
(COMP_LABEL_8)
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=32766)
//D=32766
@32766
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=32766)
//D=32766
@32766
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_ARITHMETIC: 1>, arg1='gt', arg2=None)
// compare ops eq|gt|lt
//D=RAM[SP-1]
@SP
A=M-1
D=M
//SP--
@SP
M=M-1
//RAM[SP-2] - RAM[SP-1]
A=M-1
D=M-D
// RAM[SP-2] = 1111 1111 1111 1111
M=-1
@COMP_LABEL_9
D;JGT
//RAM[SP-2] = 0
@SP
A=M-1
M=0
(COMP_LABEL_9)
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=57)
//D=57
@57
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=31)
//D=31
@31
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=53)
//D=53
@53
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
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=112)
//D=112
@112
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
//Command(type=<CommandType.C_ARITHMETIC: 1>, arg1='neg', arg2=None)
//op neg
//M = -RAM[SP-1]
@SP
A=M-1
M=-M
//Command(type=<CommandType.C_ARITHMETIC: 1>, arg1='and', arg2=None)
// logic ops and
//SP--
@SP
M=M-1
//D=RAM[SP-1]
@SP
A=M
D=M
//RAM[SP-2]=D & RAM[SP-2]
@SP
A=M-1
M=D&M
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=82)
//D=82
@82
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_ARITHMETIC: 1>, arg1='or', arg2=None)
// logic ops or
//SP--
@SP
M=M-1
//D=RAM[SP-1]
@SP
A=M
D=M
//RAM[SP-2]=D|RAM[SP-2]
@SP
A=M-1
M=D|M
//Command(type=<CommandType.C_ARITHMETIC: 1>, arg1='not', arg2=None)
// logic ops not
//D=RAM[SP-1]
@SP
A=M-1
M=!M
