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
//Command(type=<CommandType.C_FUNCTION: 7>, arg1='Class1.set', arg2=0)
//function's entry point
(Class1.set)
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
//Command(type=<CommandType.C_POP: 3>, arg1='static', arg2=0)
//pop static i; pop XXX.i
//SP--
@SP
M=M-1
//RAM[XXX.i]=RAM[SP]
@SP
A=M
D=M
@Class1.0
M=D
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
//Command(type=<CommandType.C_POP: 3>, arg1='static', arg2=1)
//pop static i; pop XXX.i
//SP--
@SP
M=M-1
//RAM[XXX.i]=RAM[SP]
@SP
A=M
D=M
@Class1.1
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
//Command(type=<CommandType.C_FUNCTION: 7>, arg1='Class1.get', arg2=0)
//function's entry point
(Class1.get)
//Command(type=<CommandType.C_PUSH: 2>, arg1='static', arg2=0)
//push static i = push XXX.i
//RAM[SP]=RAM[XXX.i]
@Class1.0
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
@Class1.1
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
//Command(type=<CommandType.C_FUNCTION: 7>, arg1='Class2.set', arg2=0)
//function's entry point
(Class2.set)
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
//Command(type=<CommandType.C_POP: 3>, arg1='static', arg2=0)
//pop static i; pop XXX.i
//SP--
@SP
M=M-1
//RAM[XXX.i]=RAM[SP]
@SP
A=M
D=M
@Class2.0
M=D
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
//Command(type=<CommandType.C_POP: 3>, arg1='static', arg2=1)
//pop static i; pop XXX.i
//SP--
@SP
M=M-1
//RAM[XXX.i]=RAM[SP]
@SP
A=M
D=M
@Class2.1
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
//Command(type=<CommandType.C_FUNCTION: 7>, arg1='Class2.get', arg2=0)
//function's entry point
(Class2.get)
//Command(type=<CommandType.C_PUSH: 2>, arg1='static', arg2=0)
//push static i = push XXX.i
//RAM[SP]=RAM[XXX.i]
@Class2.0
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
@Class2.1
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
//Command(type=<CommandType.C_FUNCTION: 7>, arg1='Sys.init', arg2=0)
//function's entry point
(Sys.init)
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=6)
//D=6
@6
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
//Command(type=<CommandType.C_CALL: 9>, arg1='Class1.set', arg2=2)
// save return address
@Class1.set$2$Ret.1
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
@7
D=D-A
@ARG
M=D
//Reposition LCL (LCL=SP)
@SP
D=M
@LCL
M=D
//goto functionName
@Class1.set
0;JMP
//retAddrLabel
(Class1.set$2$Ret.1)
//Command(type=<CommandType.C_POP: 3>, arg1='temp', arg2=0)
//pop temp i ; pop RAM[5+i]
//SP--
@SP
M=M-1
//D=RAM[SP]
@SP
A=M
D=M
// RAM[5+i]=D
@R5
M=D
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=23)
//D=23
@23
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_PUSH: 2>, arg1='constant', arg2=15)
//D=15
@15
D=A
//RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//Command(type=<CommandType.C_CALL: 9>, arg1='Class2.set', arg2=2)
// save return address
@Class2.set$2$Ret.2
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
@7
D=D-A
@ARG
M=D
//Reposition LCL (LCL=SP)
@SP
D=M
@LCL
M=D
//goto functionName
@Class2.set
0;JMP
//retAddrLabel
(Class2.set$2$Ret.2)
//Command(type=<CommandType.C_POP: 3>, arg1='temp', arg2=0)
//pop temp i ; pop RAM[5+i]
//SP--
@SP
M=M-1
//D=RAM[SP]
@SP
A=M
D=M
// RAM[5+i]=D
@R5
M=D
//Command(type=<CommandType.C_CALL: 9>, arg1='Class1.get', arg2=0)
//special process for nrags=0//SP++
@SP
M=M+1
// save return address
@Class1.get$0$Ret.3
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
//Reposition ARG (ARG = SP-5-1)
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
@Class1.get
0;JMP
//retAddrLabel
(Class1.get$0$Ret.3)
//Command(type=<CommandType.C_CALL: 9>, arg1='Class2.get', arg2=0)
//special process for nrags=0//SP++
@SP
M=M+1
// save return address
@Class2.get$0$Ret.4
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
//Reposition ARG (ARG = SP-5-1)
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
@Class2.get
0;JMP
//retAddrLabel
(Class2.get$0$Ret.4)
//Command(type=<CommandType.C_LABEL: 4>, arg1='END', arg2=None)
(END)
//Command(type=<CommandType.C_GOTO: 5>, arg1='END', arg2=None)
//jump
@END
0;JMP
