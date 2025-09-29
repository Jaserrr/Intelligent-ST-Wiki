ST: MOV SCON, #00H
    MOV A, #80H
LP2: MOV R0, #8
     CLR P1.0
     SETB P1.0
LP1: MOV SBUF, A
     JNB TI, $
     CLR TI
     DJNZ R0, LP1
     LCALL DELAY2S
     RR A
     SJMP LP2

DELAY2S:   
    MOV R7,#7FH
DL3:
    MOV R6,#0EBH
DL2:
    MOV R5,#20H
    DJNZ R5,$
    DJNZ R6,DL2
    DJNZ R7,DL3
    NOP
    RET

END

    
