//bootstrap_code
//SP=256
@256
D=A
@SP
M=D
//call Sys.init
@5
D=A
@SP
M=M+D//goto functionName
@Sys.init
0;JMP
//Command(type=<CommandType.C_FUNCTION: 7>, arg1='Main.fibonacci', arg2=0)
//function's entry point
(Main.fibonacci)
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
@COMP_LABEL_1
D;JLT
//RAM[SP-2] = 0
@SP
A=M-1
M=0
(COMP_LABEL_1)
//Command(type=<CommandType.C_IF: 6>, arg1='N_LT_2', arg2=None)
//SP--
@SP
M=M-1
//D=RAM[SP-1]
A=M
D=M
//Jump on condition D
@N_LT_2
D;JNE
//Command(type=<CommandType.C_GOTO: 5>, arg1='N_GE_2', arg2=None)
//jump
@N_GE_2
0;JMP
//Command(type=<CommandType.C_LABEL: 4>, arg1='N_LT_2', arg2=None)
(N_LT_2)
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
//Command(type=<CommandType.C_LABEL: 4>, arg1='N_GE_2', arg2=None)
(N_GE_2)
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
//Command(type=<CommandType.C_CALL: 9>, arg1='Main.fibonacci', arg2=1)
// save return address
@Main.fibonacci$1$Ret.1
D=A
@SP
A=M
M=D
//SP++
@SP
M=M+1
//save LCL
@LCL
D=M
@SP
A=M
M=D
//SP++
@SP
M=M+1
//save ARG
@ARG
D=M
@SP
A=M
M=D
//SP++
@SP
M=M+1
//save THIS
@THIS
D=M
@SP
A=M
M=D
//SP++
@SP
M=M+1
//save THAT
@THAT
D=M
@SP
A=M
M=D
//SP++
@SP
M=M+1
//Reposition ARG (ARG = SP-5-nArgs)
@SP
D=M
@6
D=D-A
@ARG
M=D
//Reposition LCL (LCL=SP)
@SP
D=M
@LCL
M=D
//goto functionName
@Main.fibonacci
0;JMP
//retAddrLabel
(Main.fibonacci$1$Ret.1)
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
//Command(type=<CommandType.C_CALL: 9>, arg1='Main.fibonacci', arg2=1)
// save return address
@Main.fibonacci$1$Ret.2
D=A
@SP
A=M
M=D
//SP++
@SP
M=M+1
//save LCL
@LCL
D=M
@SP
A=M
M=D
//SP++
@SP
M=M+1
//save ARG
@ARG
D=M
@SP
A=M
M=D
//SP++
@SP
M=M+1
//save THIS
@THIS
D=M
@SP
A=M
M=D
//SP++
@SP
M=M+1
//save THAT
@THAT
D=M
@SP
A=M
M=D
//SP++
@SP
M=M+1
//Reposition ARG (ARG = SP-5-nArgs)
@SP
D=M
@6
D=D-A
@ARG
M=D
//Reposition LCL (LCL=SP)
@SP
D=M
@LCL
M=D
//goto functionName
@Main.fibonacci
0;JMP
//retAddrLabel
(Main.fibonacci$1$Ret.2)
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
//Command(type=<CommandType.C_FUNCTION: 7>, arg1='Sys.init', arg2=0)
//function's entry point
(Sys.init)
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=4)
//D=4
@4
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_CALL: 9>, arg1='Main.fibonacci', arg2=1)
// save return address
@Main.fibonacci$1$Ret.3
D=A
@SP
A=M
M=D
//SP++
@SP
M=M+1
//save LCL
@LCL
D=M
@SP
A=M
M=D
//SP++
@SP
M=M+1
//save ARG
@ARG
D=M
@SP
A=M
M=D
//SP++
@SP
M=M+1
//save THIS
@THIS
D=M
@SP
A=M
M=D
//SP++
@SP
M=M+1
//save THAT
@THAT
D=M
@SP
A=M
M=D
//SP++
@SP
M=M+1
//Reposition ARG (ARG = SP-5-nArgs)
@SP
D=M
@6
D=D-A
@ARG
M=D
//Reposition LCL (LCL=SP)
@SP
D=M
@LCL
M=D
//goto functionName
@Main.fibonacci
0;JMP
//retAddrLabel
(Main.fibonacci$1$Ret.3)
//Command(type=<CommandType.C_LABEL: 4>, arg1='END', arg2=None)
(END)
//Command(type=<CommandType.C_GOTO: 5>, arg1='END', arg2=None)
//jump
@END
0;JMP
