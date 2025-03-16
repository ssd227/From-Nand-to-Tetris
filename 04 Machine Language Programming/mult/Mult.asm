// ram[2] = ram[0]*ram[1]
// x*0的情况, 能保证不循环，或者循环加上的是0

    // i=0
    @i
    M=0
    // R2=0
    @R2
    M=0
(LOOP)
    // if(i >= R1) goto STOP 
    @i
    D=M
    @R1
    D=D-M
    @STOP
    D;JGE
    // R2 = R2 + R0
    @R2
    D=M
    @R0
    D=D+M
    @R2
    M=D
    // i=i+1
    @i
    M=M+1
    // goto LOOP
    @LOOP
    0;JMP
(STOP)
(END)
    @END
    0;JMP
