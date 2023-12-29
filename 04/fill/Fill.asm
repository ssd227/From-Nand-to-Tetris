// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.

//// Replace this comment with your code.

// flag = 0
@flag
M=0
// n = 8192
@8192
D=A
@n
M=D

(LOOP)
    // i=0 准备像素扫描循环
    @i
    M=0

    // if(M[KBD]==0) goto BRANCH_WHITE
        @KBD
        D=M
        @BRANCH_WHITE
        D;JEQ

        (BRANCH_BALCK) // 分支1
        // if(flag==1) goto BALCK_END  // 不需要循环设置
        @flag
        D=M-1
        @BALCK_END 
        D;JEQ

        // if(i >= n) goto BALCK_END 
        @i
        D=M
        @n
        D=D-M
        @BALCK_END
        D;JGE
            // SCREEN[i]=-1  // base+i
            @i
            D=M
            @SCREEN
            A=A+D
            M=-1
            // i=i+1
            @i
            M=M+1
            // goto BRANCH_BALCK
            @BRANCH_BALCK
            0;JMP
            
        (BALCK_END) // screen 设置结束
        // falg=0
        @flag
        M=1

        // goto LOOP // 分支black结束，外循环
        @LOOP
        0;JMP

        
        (BRANCH_WHITE) // 分支0
        // if(flag==0) goto WHITE_END // 不需要循环设置
        @flag
        D=M
        @WHITE_END
        D;JEQ

        // if(i >= N) goto WHITE_END
        @i
        D=M
        @n
        D=D-M
        @WHITE_END
        D;JGE
            // SCREEN[i]=0  // base+i
            @i
            D=M
            @SCREEN
            A=A+D
            M=0
            // i=i+1
            @i
            M=M+1
            // goto BRANCH_WHITE
            @BRANCH_WHITE
            0;JMP
        (WHITE_END)
        // falg=0
        @flag
        M=0

        // goto LOOP // 分支white结束，外循环
        @LOOP
        0;JMP

(STOP) // 执行不到

(END)
@END
0;JMP